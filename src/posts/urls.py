from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('follower/', TemplateView.as_view(template_name='follower.html'), name='follower'),
    path('following/', TemplateView.as_view(template_name='following.html'), name='following'),
    path('users-list/', views.UserListView.as_view()),
    path('request/', views.RequestView.as_view()),
    path('requests-list/', views.RequestListView.as_view()),
    path('accept/', views.AcceptView.as_view()),
    path('friends/', views.FriendListView.as_view()),
    path('post/', views.PostView.as_view(), name='post'),
    path('post/<int:post_pk>/', views.PostView.as_view(), name='post'),
    path('post_update/<int:post_pk>/', views.PostUpdateView.as_view(), name='post_update'),
    path('post_delete/<int:post_pk>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post_list/', views.PostListView.as_view(), name='post_list'),
    path('post/<int:post_pk>/comments/', views.CommentView.as_view(), name='comment'),
    path('post/<int:post_pk>/likes/', views.LikeView.as_view(), name='like')

]



