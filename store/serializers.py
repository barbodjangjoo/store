from decimal import Decimal
from rest_framework import serializers

from . import models


class CategorySerializers(serializers.Serializer):
    title = serializers.CharField(max_length= 255)
    description = serializers.CharField(max_length=500)


class ProductSerializer(serializers.ModelSerializer):
    tax_price = serializers.SerializerMethodField()
    category = serializers.HyperlinkedRelatedField(
        queryset = models.Category.objects.all(),
        view_name = 'category-detail',
    )
    class Meta:
        model = models.Product
        fields = ['id', 'name', 'unit_price', 'inventory', 'category', 'tax_price']
        # id = serializers.IntegerField()
        # name = serializers.CharField(max_length = 255)
        # unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
        # inventory = serializers.IntegerField()
    # category = CategorySerializers()

    def get_tax_price(self, product):
        return round(product.unit_price * Decimal(1.09), 2)
