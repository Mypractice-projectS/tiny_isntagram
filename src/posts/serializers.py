from rest_framework import serializers
from accounts.models import User, Profile
from posts.models import Post,Comment,Like





class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user','caption','is_active','is_public']
        extra_kwargs = {
            'user': {'read_only': True},
        }



#   Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('post', 'user', 'text')
        extra_kwargs = {
            'post': {'read_only': True},
            'user': {'read_only': True}
        }



#    Like

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('post', 'user', 'is_liked')
        extra_kwargs = {
            'post': {'read_only': True},
            'user': {'read_only': True},
            'is_liked': {'required': False}
        }
        
        
class UserListSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')

    def get_avatar(self, instance):
        if hasattr(instance, 'profile') and instance.profile.avatar:
            return instance.profile.avatar.url
        return ''


