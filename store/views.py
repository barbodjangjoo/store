from django.shortcuts import get_object_or_404, render
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Prefetch 


from .paginations import DefaultPagination
from . import models
from . import serializers
from . import filters
from . import permissions

class CategoryViewSet(ModelViewSet):
    serializer_class = serializers.CategorySerializers
    queryset = models.Category.objects.prefetch_related('products').all()
    permission_classes = [permissions.IsAdminOrReadOnly]

class ProductViewSet(ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    filter_backends = [SearchFilter,DjangoFilterBackend, OrderingFilter]
    Ordering_fields = ['name', 'unit_price', 'inventory ']
    filter_class = filters.ProductFilter
    search_fields = ['name']
    pagination_class = DefaultPagination
    permission_classes = [permissions.IsAdminOrReadOnly]
    # filterset_fields = ['category_id', 'inventory]

    # def get_queryset(self):
    #     queryset = models.Product.objects.all()
    #     category_id_parameter = self.request.query_params.get('category_id')
    #     if category_id_parameter is not None:
    #         queryset = queryset.filter(category_id=category_id_parameter)
    #         return queryset

    def get_serializer_context(self):
        return {'request': self.request}
    
class CommentViewSet(ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_pk = self.kwargs['product_pk']
        return models.Comment.objects.filter(product_id=product_pk).all()
    
    def get_serializer_context(self):
        return {'product_pk': self.kwargs['product_pk']} 
    

class CartViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    serializer_class = serializers.CartSerializer
    queryset = models.Cart.objects.prefetch_related('items__product').all()

class CartItemViewSet(ModelViewSet): 
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_queryset(self):
        cart_pk = self.kwargs['cart_pk']
        return models.CartItem.objects.select_related('product').filter(cart_id=cart_pk).all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return serializers.UpdateCartItemSerializer
        return serializers.CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_pk': self.kwargs['cart_pk']}   
    
class CustomerViewSet(ModelViewSet):
    serializer_class = serializers.CustomerSerializer
    queryset = models.Customer.objects.all()
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user_id = request.user.id
        customer= models.Customer.objects.get(user_id=user_id)
        if request.method == 'GET':
            serializer= serializers.CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = serializers.CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
    @action(detail=True, permission_classes=[permissions.SendPrivateEmailToCustomerPermission])
    def send_private_email(self, request, pk):
        return Response(f'Sending Email to customer {pk=}')
    
class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset= models.Order.objects.prefetch_related(
            Prefetch(
                'items',
                queryset=models.OrderItem.objects.select_related('product'),
            )
            ).select_related('customer__user').all()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(customer__user_id=self.request.user.id)
    
    def get_serializer_class(self):

        if self.request.method == 'POST':
            return serializers.OrderCreateSerializer
        
        if self.request.user.is_staff:
            return serializers.OrderForAdminSerializer
        
        return serializers.OrderSerializer
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    
