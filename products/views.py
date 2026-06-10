from rest_framework import viewsets, generics, permissions
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Product, Category, Brand
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCreateUpdateSerializer,
    CategorySerializer,
    BrandSerializer
)

from .filters import ProductFilter
from core.pagination import ProductPagination


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.filter(
        available=True
    ).select_related(
        "category",
        "brand"
    ).prefetch_related(
        "images",
        "variants"
    )

    pagination_class = ProductPagination

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_class = ProductFilter

    search_fields = [
        "name",
        "description"
    ]

    ordering_fields = [
        "price",
        "created_at"
    ]

    ordering = ["-created_at"]

    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer

        if self.action == "retrieve":
            return ProductDetailSerializer

        return ProductCreateUpdateSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get_object(self):
        if self.action == "retrieve":
            slug = self.kwargs.get("slug")
            return get_object_or_404(Product, slug=slug, available=True)
        return super().get_object()


class CategoryListView(generics.ListAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class BrandListView(generics.ListAPIView):

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.AllowAny]

class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BrandViewSet(ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer