from rest_framework import viewsets

from wall.models import Profile, Post, Hashtag
from wall.serializers import ProfileSerializer, PostSerializer, HashtagSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.prefetch_related("follow")
    serializer_class = ProfileSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.prefetch_related("hashtags")
    serializer_class = PostSerializer


class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
