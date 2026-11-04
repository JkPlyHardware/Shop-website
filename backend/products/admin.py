from django.contrib import admin
from .models import Category, Product, ProductImage, Testimonial

class ProductImageInline(admin.TabularInline): model = ProductImage; extra = 1
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "availability", "featured", "is_published", "updated_at"]
    list_filter = ["category", "availability", "featured", "is_published"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]
admin.site.register(Category)
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["customer_name", "rating", "is_published", "created_at"]
    list_filter = ["is_published", "rating"]
