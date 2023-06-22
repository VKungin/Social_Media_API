from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from social.models import Profile, Post, Hashtag
from social.serializers import (
    ProfileSerializer,
    PostSerializer,
    HashtagSerializer,
)
from social.permisssion import IsAuthorOrReadOnly
from user.models import User


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.prefetch_related("follow")
    serializer_class = ProfileSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        user = self.request.user
        profile, created = Profile.objects.get_or_create(user=user)
        if created:
            profile.first_name = serializer.validated_data.get("first_name")
            profile.last_name = serializer.validated_data.get("last_name")
            profile.bio = serializer.validated_data.get("bio")
            profile.email = serializer.validated_data.get("email")
            profile.follow.set(serializer.validated_data.get("follow", []))
            profile.save()
        serializer.instance = profile

    @action(detail=True, methods=["post"])
    def follow(self, request, pk=None):
        profile = self.get_object()
        user_to_follow = get_object_or_404(User, pk=pk)
        profile.follow.add(user_to_follow)

        if request.user != user_to_follow:
            profile.follow.add(user_to_follow)
            return Response(
                "User followed successfully.",
                status=status.HTTP_200_OK,
            )
        return Response(
            "You cannot follow yourself.",
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=True, methods=["post"])
    def unfollow(self, request, pk=None):
        profile = self.get_object()
        user = request.user

        profile.follow.remove(user)
        return Response(
            {"detail": "You have successfully unsubscribed from your profile."},
            status=status.HTTP_200_OK,
        )


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

        return queryset.select_related("user").distinct()

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
    permission_classes = (IsAuthenticatedOrReadOnly,)
