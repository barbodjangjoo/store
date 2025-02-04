from rest_framework.pagination import PageNumberPagination

class DefaultPagination(PageNumberPagination):
    class Meta:
        page_size = 10