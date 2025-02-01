from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.category_list, name='category-list'),
    path('category/<int:pk>/', views.category_detail, name='category-detail'),
    path('product/', views.ProductList.as_view(), name='product-list'),
    path('product/<int:pk>/', views.product_detail, name='product-detail'),
]

