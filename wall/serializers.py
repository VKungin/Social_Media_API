from rest_framework import serializers

from wall.models import Hashtag, Post, Profile


class HashtagSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Hashtag
        fields = ("id", "name", "posts")


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    hashtags = HashtagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "content", "published", "user", "hashtags")


class ProfileSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    follow = serializers.StringRelatedField(many=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "username",
            "first_name",
            "last_name",
            "bio",
            "email",
            "follow",
            "posts",
        )
