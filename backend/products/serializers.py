from rest_framework import serializers
from .models import Category, Product, ProductImage, Testimonial

class CategorySerializer(serializers.ModelSerializer):
    class Meta: model = Category; fields = ["id", "name", "slug", "description"]

class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta: model = ProductImage; fields = ["id", "image", "alt_text", "display_order"]

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()
    class Meta: model = Product; fields = ["id", "name", "slug", "description", "category", "price", "image", "image_url", "images", "availability", "featured", "created_at"]
    def get_image_url(self, obj):
        request = self.context.get("request")
        if not obj.image: return None
        url = obj.image.url
        return request.build_absolute_uri(url) if request else url

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta: model = Testimonial; fields = ["id", "customer_name", "feedback", "rating", "created_at"]
