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


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = ['id', 'create_at']
