from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle
from .models import Category, Product, Testimonial
from .serializers import CategorySerializer, ProductSerializer, TestimonialSerializer

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all(); serializer_class = CategorySerializer; permission_classes = [AllowAny]

class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer; permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]; throttle_scope = "product_search"
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description", "category__name"]
    ordering_fields = ["created_at", "name"]
    def get_queryset(self):
        qs = Product.objects.filter(is_published=True).select_related("category").prefetch_related("images")
        category = self.request.query_params.get("category")
        featured = self.request.query_params.get("featured")
        if category: qs = qs.filter(category__slug=category)
        if featured == "true": qs = qs.filter(featured=True)
        return qs

class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_published=True).select_related("category").prefetch_related("images")
    serializer_class = ProductSerializer; lookup_field = "slug"; permission_classes = [AllowAny]

class TestimonialList(generics.ListAPIView):
    queryset = Testimonial.objects.filter(is_published=True); serializer_class = TestimonialSerializer; permission_classes = [AllowAny]
