from decimal import Decimal
from rest_framework import serializers

from store.models import Category


class CategorySerializers(serializers.Serializer):
    title = serializers.CharField(max_length= 255)
    description = serializers.CharField(max_length=500)


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length = 255)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    inventory = serializers.IntegerField()
    category = serializers.HyperlinkedRelatedField(
        queryset = Category.objects.all(),
        view_name = 'category-detail',
    )
    tax_price = serializers.SerializerMethodField()

    def get_tax_price(self, product):
        return round(product.unit_price * Decimal(1.09), 2)
