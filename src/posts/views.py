from django.shortcuts import render
from django.views import View
#Create your views here.
class postView(View):
    def get(self, request):
        return render(request, "mypost.html")

class exploreView(View):
    def get(self, request):
        return render(request, "explore.html")