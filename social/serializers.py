from rest_framework import serializers

from social.models import Hashtag, Post, Profile


class HashtagSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Hashtag
        fields = ("id", "name", "posts")


class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.all(), many=False
    )
    hashtags = serializers.PrimaryKeyRelatedField(
        queryset=Hashtag.objects.all(), many=True
    )

    class Meta:
        model = Post
        fields = ("id", "title", "content", "published", "user", "hashtags")


class ProfileSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    follow = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Profile.objects.all()
    )
    user = serializers.StringRelatedField(many=False)

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "first_name",
            "last_name",
            "bio",
            "follow",
            "posts",
        )
