from django.urls import path, include
from rest_framework import routers

from social.views import ProfileViewSet, PostViewSet, HashtagViewSet

router = routers.DefaultRouter()

router.register("post", viewset=PostViewSet)
router.register("profile", viewset=ProfileViewSet)
router.register("hashtag", viewset=HashtagViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path(
        "<int:pk>/follow/",
        ProfileViewSet.as_view({"post": "follow"}),
        name="profile-follow",
    ),
    path(
        "<int:pk>/unfollow/",
        ProfileViewSet.as_view({"post": "unfollow"}),
        name="profile-unfollow",
    ),
]
app_name = "social"
