from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='products_store-index'),
    path('tools/', views.tools, name='products_store-tools'),
]