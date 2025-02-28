from django.urls import path
from .views import PostView, ExploreView, FollowingView, FollowerView




urlpatterns = [
    path('post/', PostView.as_view(), name='post'),
    path('explore/', ExploreView.as_view(), name='explore'),
    path('following/', FollowingView.as_view(), name='following'),
    path('follower/', FollowerView.as_view(), name='follower'),
]