from django.db.models import Q,Count,Sum
from django.shortcuts import get_object_or_404
from rest_framework import viewsets,status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

from .serializers import UserSerializer,ProfileSerializer
from .permissions import IsOwnerOrReadOnly
from .models import User,UserFollow
from posts.serializers import PostSerializer
from posts.models import Post


# Create your views here.


class UserApiViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    class Meta:
        model = User

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ProfileSerializer
        return UserSerializer

query = openapi.Parameter('query',openapi.IN_QUERY,type=openapi.TYPE_STRING)
@method_decorator(name='get',decorator=swagger_auto_schema(manual_parameters=[query]))
class UserSearchView(ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        queryset = User.objects.all()
        query = self.request.query_params.get('query',None)
        query_filter = Q(username__icontains=query) | Q(email__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
        if query:
            queryset = queryset.filter(query_filter)
        return queryset
action_parameter = openapi.Parameter(
                name='action',
                in_=openapi.IN_PATH,
                description='Action to perform (follow or unfollow)',
                required=True,
                type=openapi.TYPE_STRING,
                enum=['follow', 'unfollow'],
                default='follow',
            )
@method_decorator(name='post',decorator=swagger_auto_schema(manual_parameters=[action_parameter]))
class UserFollowView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,*args,**kwargs):
        user_id = kwargs.get('user_id')
        action = kwargs.get('action')
        user = User.objects.filter(pk=user_id).first()
        if user:
            current_user = request.user
            if action == 'follow':
                UserFollow.objects.get_or_create(following_user=user,follower_user=current_user)
            elif action == 'unfollow':
                UserFollow.objects.filter(following_user=user,follower_user=current_user).delete()
            else:
                return Response({'message':'Invalid action'},status=400)
            return Response({'message': f'You successfully {action}ed'},status=200)
        else:
            return Response({'message':'User not found'},status=404)

        

class UserPostsView(ListAPIView):
    '''Get posts posted by specific user'''
    serializer_class = PostSerializer
    def get_queryset(self):
        kwargs = self.kwargs
        user_id = kwargs.get('user_id')
        queryset = Post.objects.filter(owner__pk=user_id)
        return queryset


class UserSuggestionsView(APIView):
    def get(self, request):
        most_following_users = User.objects.annotate(num_followers=Count('following')).order_by('-num_followers')[:5]

        
        most_liked_posts_owners= Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[:5].values('owner')
        most_liked_users = set([get_object_or_404(User,pk=post['owner']) for post in most_liked_posts_owners])


        most_commented_posts_owners= Post.objects.annotate(num_comments=Count('comments')).order_by('-num_comments')[:5].values('owner')
        most_commented_users = set([get_object_or_404(User,pk=post['owner']) for post in most_commented_posts_owners])
        
       

       
        users = set(most_following_users) | most_liked_users | most_commented_users

        
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)