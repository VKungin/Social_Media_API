from rest_framework import viewsets

from wall.models import Profile, Post, Hashtag
from wall.serializers import ProfileSerializer, PostSerializer, HashtagSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.prefetch_related("follow")
    serializer_class = ProfileSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.prefetch_related("hashtags")
    serializer_class = PostSerializer

    @staticmethod
    def _params_to_ints(qs):
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        queryset = self.queryset

        hashtags = self.request.query_params.get("hashtags")

        if hashtags:
            hashtags_ids = self._params_to_ints(hashtags)
            queryset = queryset.filter(hashtags__id__in=hashtags_ids)

        return queryset.distinct()


class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
