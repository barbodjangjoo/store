from decimal import Decimal
from rest_framework import serializers

DOLLARS_TO_RIALS = 500000

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length = 255)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    inventory = serializers.IntegerField()
    tax_price = serializers.SerializerMethodField()
    price_rials = serializers.SerializerMethodField() 

    def get_price_rials(self, product):
        return int(product.unit_price * DOLLARS_TO_RIALS )
    
    def get_tax_price(self, product):
        return round(product.unit_price * Decimal(1.09), 2)
