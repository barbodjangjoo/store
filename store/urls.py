from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register('categories', views.CategoryViewSet, basename='category')
router.register('carts', views.CartViewSet, basename='cart')
router.register('customers', views.CustomerViewSet)
router.register('order', views.OrderViewSet,basename='order')

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('comments', views.CommentViewSet, basename='product-comment')

cart_items_router = routers.NestedDefaultRouter(router, 'carts', lookup = 'cart')
cart_items_router.register('items', views.CartItemViewSet, basename='cart-items')


urlpatterns = router.urls + product_router.urls + cart_items_router.urls


# urlpatterns = [
#     path('category/', views.CategoryList.as_view(), name='category-list'),
#     path('category/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
#     path('product/', views.ProductList.as_view(), name='product-list'),
#     path('product/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
# ]

