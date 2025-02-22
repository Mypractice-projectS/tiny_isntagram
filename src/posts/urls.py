from django.urls import path
from .views import postView,exploreView

urlpatterns = [
    path("mypost/" , postView.as_view() , name='post'),
    path("explore/" , exploreView.as_view() , name='post'),
]