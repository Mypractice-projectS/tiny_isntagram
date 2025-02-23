from django.shortcuts import render
from django.urls import path
from django.views.generic import TemplateView

class PostView(TemplateView):
    template_name = 'mypost.html'

class ExploreView(TemplateView):
    template_name = 'explore.html'

class FollowingView(TemplateView):
    template_name = 'following.html'

class FollowerView(TemplateView):
    template_name = 'follower.html'