from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import models
from .serializers import ProductSerializer

@api_view()
def product_list(request):
    queryset = models.Product.objects.all()
    serializer = ProductSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view()
def product_detail(request, pk):
    product = get_object_or_404(models.Product, pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

