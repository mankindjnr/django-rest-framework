from django.urls import path

from . import views

urlpatterns = [
    path('', views.product_list_create_view, name='product_create'),
    path('update/<int:pk>/', views.product_update_api_view, name='product_update'),
    path('delete/<int:pk>/', views.product_destroy_api_view, name='product_delete'),
    path('<int:pk>/', views.product_detail_api_view, name='product_detail'),
]