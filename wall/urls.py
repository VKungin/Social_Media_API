from django.urls import path, include
from rest_framework import routers

from wall.views import ProfileViewSet, PostViewSet, HashtagViewSet

router = routers.DefaultRouter()

router.register("post", viewset=PostViewSet)
router.register("profile", viewset=ProfileViewSet)
router.register("hashtag", viewset=HashtagViewSet)
urlpatterns = [path("", include(router.urls))]
app_name = "wall"
