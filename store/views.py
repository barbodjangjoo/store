from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import models
from . import serializers

@api_view()
def category_detail(request, pk):
    category = get_object_or_404(models.Category, pk=pk)
    serializer = serializers.CategorySerializers(category, context={'request':request})
    return Response(serializer.data)

@api_view()
def product_list(request):
    queryset = models.Product.objects.select_related('category').all()
    serializer = serializers.ProductSerializer(queryset, many=True, context={'request':request})
    return Response(serializer.data)

@api_view()
def product_detail(request, pk):
    product = get_object_or_404(
        models.Product.objects.select_related('category'),
         pk=pk)
    serializer = serializers.ProductSerializer(product)
    return Response(serializer.data)

