from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from . import models
from . import serializers

@api_view(['GET', 'POST'])
def category_list(request):
    if request.method == 'GET':
        queryset = models.Category.objects.all()
        serializer = serializers.CategorySerializers(queryset, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = serializers.CategorySerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    category = get_object_or_404(models.Category, pk=pk)
    if request.method == 'GET':
        serializer = serializers.CategorySerializers(category, context={'request':request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = serializers.CategorySerializers(category ,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        category.delete()
        return Response('category were delete', status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET': 
        queryset = models.Product.objects.select_related('category').all()
        serializer = serializers.ProductSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = serializers.ProductSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    product = get_object_or_404(
        models.Product.objects.select_related('category'),
        pk=pk)
    
    if request.method == 'GET':
        serializer = serializers.ProductSerializer(product, context={'request':request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = serializers.ProductSerializer(product ,data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        



        


