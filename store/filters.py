from django_filters.rest_framework import FilterSet

from . import models

class ProductFilter(FilterSet):
    class meta:
        model = models.Product
        fields = {
            'inventory': ['lt', 'gt'],
        }