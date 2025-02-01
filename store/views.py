from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework import status

from . import models
from . import serializers

class CategoryList(ListCreateAPIView):
    serializer_class = serializers.CategorySerializers
    queryset = models.Category.objects.prefetch_related('products').all()

# class CategoryList(APIView):
#     def get(self, request):
#         queryset = models.Category.objects.prefetch_related('products').all()
#         serializer = serializers.CategorySerializers(queryset, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = serializers.CategorySerializers(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class CategoryDetail(APIView):
    def get(self, request, pk):
        category = get_object_or_404(models.Category, pk=pk)
        serializer = serializers.CategorySerializers(category, context={'request':request})
        return Response(serializer.data)
    def put(self, request, pk):
        category = get_object_or_404(models.Category, pk=pk)
        serializer = serializers.CategorySerializers(category ,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def delete(self, request, pk):
        category = get_object_or_404(models.Category, pk=pk)
        if category.products.count() > 0:
            return Response({'error': 'there is some product in this category'})
        category.delete()
        return Response('category were delete', status=status.HTTP_200_OK)
    
class ProductList(ListCreateAPIView):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.select_related('category').all()

    def get_serializer_context(self):
        return {'request': self.request}

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

class ProductDetail(APIView):
    def get(self, request, pk):
        product = get_object_or_404(
        models.Product.objects.select_related('category'),
        pk=pk)
        serializer = serializers.ProductSerializer(product, context={'request':request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        product = get_object_or_404(
        models.Product.objects.select_related('category'),
        pk=pk)
        serializer = serializers.ProductSerializer(product ,data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk):
        product = get_object_or_404(
        models.Product.objects.select_related('category'),
        pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
