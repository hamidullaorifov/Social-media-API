from rest_framework import serializers
from taggit.serializers import TaggitSerializer,TagListSerializerField
from .models import Post,Comment
from users.models import User
from users.serializers import UserSerializer

class PostCreateUpdateSerializer(TaggitSerializer,serializers.ModelSerializer):
    tags = TagListSerializerField()
    class Meta:
        model = Post
        fields = ('content','tags')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id','owner','text','created')
        extra_kwargs = {'owner':{'read_only':True}}

class PostSerializer(TaggitSerializer,serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    tags = TagListSerializerField()
    comments = CommentSerializer(many=True)
    class Meta:
        model = Post
        fields = ('id','owner','content','updated','created','tags','likes','comments')
        extra_kwargs = {
            'likes':{'read_only':True},
        }
    

# class CommentCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ('id','post','owner','text','created')
# class CommentSerializer(serializers.ModelSerializer):
#     post = PostSerializer()
#     owner = UserSerializer()
#     class Meta:
#         model = Comment
#         fields = ('id','post','owner','text','created')
    