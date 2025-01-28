from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from . import models
from . import serializers

@api_view(['GET', 'POST'])
def category_detail(request, pk):
    if request.method == 'GET':
        category = get_object_or_404(models.Category, pk=pk)
        serializer = serializers.CategorySerializers(category, context={'request':request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = serializers.CategorySerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

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
    

@api_view()
def product_detail(request, pk):
    product = get_object_or_404(
        models.Product.objects.select_related('category'),
        pk=pk)
    serializer = serializers.ProductSerializer(product, context={'request':request})
    return Response(serializer.data)



        


