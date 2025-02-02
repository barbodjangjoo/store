from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register('categories', views.CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]


# urlpatterns = [
#     path('category/', views.CategoryList.as_view(), name='category-list'),
#     path('category/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
#     path('product/', views.ProductList.as_view(), name='product-list'),
#     path('product/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
# ]

