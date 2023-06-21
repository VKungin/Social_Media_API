from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

from wall.models import Profile, Post, Hashtag
from wall.serializers import ProfileSerializer, PostSerializer, HashtagSerializer
from wall.permisssion import IsAuthorOrReadOnly


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.prefetch_related("follow")
    serializer_class = ProfileSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.prefetch_related("hashtags")
    serializer_class = PostSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

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

    # Only for documentation
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "hashtags",
                type=OpenApiTypes.INT,
                description="Filter by hashtags id (ex. ?hashtags=1)",
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
