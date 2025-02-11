from django.shortcuts import get_object_or_404, render
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins


from .paginations import DefaultPagination
from . import models
from . import serializers
from . import filters

class CategoryViewSet(ModelViewSet):
    serializer_class = serializers.CategorySerializers
    queryset = models.Category.objects.prefetch_related('products').all()

class ProductViewSet(ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    filter_backends = [SearchFilter,DjangoFilterBackend, OrderingFilter]
    Ordering_fields = ['name', 'unit_price', 'inventory ']
    filter_class = filters.ProductFilter
    search_fields = ['name']
    pagination_class = DefaultPagination
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
        



# class CategoryList(ListCreateAPIView):
#     serializer_class = serializers.CategorySerializers
#     queryset = models.Category.objects.prefetch_related('products').all()

# class CategoryDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = serializers.CategorySerializers
#     queryset = models.Category.objects.all()

#     def delete(self, request, pk):
#         category = get_object_or_404(models.Category, pk=pk)
#         if category.products.count() > 0:
#             return Response({'error': 'there is some product in this category'})
#         category.delete()
#         return Response('category were delete', status=status.HTTP_200_OK)
    


# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = serializers.ProductSerializer
#     queryset = models.Product.objects.select_related('category').all()

#     def delete(self, request, pk):
#         product = get_object_or_404(
#         models.Product.objects.select_related('category'),
#         pk=pk)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class ProductList(APIView):
#     def get(self, request):
#         queryset = models.Product.objects.select_related('category').all()
#         serializer = serializers.ProductSerializer(queryset, many=True, context={'request':request})
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = serializers.ProductSerializer(data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)