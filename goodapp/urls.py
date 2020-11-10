from django.urls import path
from .views import show_catalog, show_good, show_category, show_size

urlpatterns = [

	path(''				, show_catalog, name='show_catalog' ),
    path('<str:slug>/'	, show_good, name='show_good'),
    path('category/<str:cpu_slug>/'	, show_category, name='show_category'),
    path('size/<str:razmer_kpb>/'	, show_size, name='show_size'),
    
]
