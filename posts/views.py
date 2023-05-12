from django.db.models import Count
from rest_framework import viewsets,status,views,permissions
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView,ListAPIView
from .models import Post,Comment
from .serializers import PostSerializer,CommentSerializer,PostCreateUpdateSerializer
from .permissions import IsOwnerOrReadOnly
from users.models import User,UserFollow
from datetime import datetime,timedelta
# Create your views here.

def split_tags(text):
    return [tag.strip() for tag in text.split(',')]

class PostViewSet(viewsets.ModelViewSet):
    
    queryset = Post.objects.all()
    permission_classes = [IsOwnerOrReadOnly,permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return PostSerializer
        return PostCreateUpdateSerializer
    class Meta:
        model = Post
    def update(self, request, *args, **kwargs):
        tags_list = request.data.get('tags')
        content = request.data.get('content')
        post = self.get_object()
        post.content = content
        post.tags.set(tags_list)
        post.save()
        return Response(PostSerializer(post).data,status=status.HTTP_200_OK)
    def create(self, request, *args, **kwargs):
        tags = request.data.get('tags')
        content = request.data.get('content')
        post = Post.objects.create(owner=request.user,content=content)
        post.tags.set(tags)
        return Response(PostSerializer(post).data,status=status.HTTP_201_CREATED)

class LikePostView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,*args,**kwargs):
        user = request.user
        post_id = kwargs.get('post_id')
        post = Post.objects.filter(pk=post_id).first()
        if post:
            if user in post.likes.all():
                post.likes.remove(user)
                message = 'Your like has been removed successfully'
            else:
                post.likes.add(user)
                message = 'You liked this post'
            return Response({'message':message},status=status.HTTP_200_OK)
        return Response({'message':'Post not found'},status=status.HTTP_404_NOT_FOUND)


class CommentListCreateView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def create(self, request, *args, **kwargs):
        text = request.data.get('text')
        owner = request.user
        post_id = kwargs.get('post_id')
        post = Post.objects.filter(pk=post_id).first()
        if post:
            comment = Comment.objects.create(owner=owner,post=post,text=text)
            serializer = CommentSerializer(comment)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({'message':'Post not found'},status=status.HTTP_404_NOT_FOUND)
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.filter(pk=post_id).first()
        queryset = Comment.objects.filter(post=post)
        return queryset


class SimilarPostsView(ListAPIView):
    serializer_class = PostSerializer
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.filter(pk=post_id).first()
        if post:
            queryset = post.tags.similar_objects()
            return queryset
        return []

class PostSuggestionsView(ListAPIView):
    serializer_class = PostSerializer
    def get_queryset(self):
        user = self.request.user
        most_commented_posts = Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:5]
        most_liked_posts = Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[:5]
        queryset = set(most_commented_posts) | set(most_liked_posts)
        if not user.is_anonymous:
            followings = UserFollow.objects.filter(follower_user=user).values('following_user')
            followings_ids = set([value['following_user'] for value in followings])
            followings_posts = Post.objects.filter(owner__pk__in=followings_ids)[:5]
            queryset = queryset | set(followings_posts)
        return queryset


         