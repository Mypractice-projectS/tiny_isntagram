from django.contrib import admin
from django.urls import path, include
from accounts.views import home,login


# تابع نمایش صفحه اصلی

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')), 
    path('', home, name='home'), 
    path('login', login, name='login'), 
]
