from decimal import Decimal
from rest_framework import serializers
from django.utils.text import slugify

from . import models


class CategorySerializers(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    class Meta:
        model = models.Category
        fields = ['id' ,'title', 'description', 'product_count']
    # title = serializers.CharField(max_length= 255)
    # description = serializers.CharField(max_length=500)
    def get_product_count(self, category):
        return category.products.count()
    
    
    # def validate(self, category):
    #     if category.title < 3:
    #         return 'the category can not be less than 3 characters' 
    #     return super().validate(category)


class ProductSerializer(serializers.ModelSerializer):
    tax_price = serializers.SerializerMethodField()
    category = serializers.HyperlinkedRelatedField(
        queryset = models.Category.objects.all(),
        view_name = 'category-detail',
    )
    class Meta:
        model = models.Product
        fields = ['id', 'name', 'unit_price', 'inventory', 'category', 'tax_price', 'description']
        # id = serializers.IntegerField()
        # name = serializers.CharField(max_length = 255)
        # unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
        # inventory = serializers.IntegerField()
    # category = CategorySerializers()

    def get_tax_price(self, product):
        return round(product.unit_price * Decimal(1.09), 2)
    

    def create(self, validated_data):
        product = models.Product(**validated_data)
        product.slug = slugify(product.name)
        product.save()
        return product
    
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        fields = ['id', 'name', 'body']
    
    def create(self, validated_data):
        product_id = self.context['product_pk']
        return super().create(validated_data)
    
class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['id', 'name', 'unit_price']
class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()
    item_total = serializers.SerializerMethodField()
    class Meta:
        model = models.CartItem
        fields = ['id', 'product', 'quantity', 'item_total']

    def get_item_total(self, cart_item):
        return cart_item.quantity * cart_item.product.unit_price 



class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only = True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = models.Cart
        fields = ['id', 'items', 'total_price']
        read_only_fields = ['id']
        # "id": 434bf227-613d-4413-b186-ea7500817034
    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

