from django.contrib import admin
from django.urls import path, include



# تابع نمایش صفحه اصلی

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('accounts.urls'))
  
]
