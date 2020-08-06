
from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [

	path('catalog/'		, include('goodapp.urls')),
    path('admin/', admin.site.urls),
    
]
