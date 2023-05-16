from rest_framework import serializers
from .models import User,UserFollow,BlockUser

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id','first_name','last_name','username','email','password','bio','profile_picture')
        extra_kwargs = {'password':{'write_only':True}}
    def create(self, validated_data):
        password = validated_data['password']
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
class ProfileSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    followings = serializers.SerializerMethodField()
    blocked_users = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id','first_name','last_name','username','email','password','bio','profile_picture','followers','followings','blocked_users')
        extra_kwargs = {'password':{'write_only':True}}
    def get_followers(self,obj):
        followers = UserFollow.objects.filter(following_user=obj).values('follower_user')
        return followers
    def get_followings(self,obj):
        followings = UserFollow.objects.filter(follower_user=obj).values('following_user')
        return followings
    def get_blocked_users(self,obj):
        blocked_users = BlockUser.objects.filter(blocked_by=obj).values('blocked_user')
        return blocked_users