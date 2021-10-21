from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentsViewSet

post_router = DefaultRouter()
comment_router = DefaultRouter()

post_router.register('', PostViewSet, basename='Post')
post_router.register(r'(?P<post_id>\d+)/comments',
                     CommentsViewSet, basename='Comment')

urlpatterns = [
    path('posts/', include(post_router.urls)),

]