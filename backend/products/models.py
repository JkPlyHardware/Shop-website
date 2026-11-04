from django.db import models
from django.utils.text import slugify
from .validators import validate_product_image

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.CharField(max_length=300, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self): return self.name
    class Meta: ordering = ["sort_order", "name"]

class Product(models.Model):
    AVAILABILITY = [("available", "Available"), ("made_to_order", "Made to order"), ("unavailable", "Currently unavailable")]
    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True, validators=[validate_product_image])
    availability = models.CharField(max_length=20, choices=AVAILABILITY, default="made_to_order")
    featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self): return self.name
    class Meta:
        ordering = ["-featured", "-created_at"]
        indexes = [models.Index(fields=["is_published", "featured"]), models.Index(fields=["category", "is_published"])]

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/gallery/", validators=[validate_product_image])
    alt_text = models.CharField(max_length=180, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ["display_order"]
    def __str__(self): return f"Image: {self.product.name}"

class Testimonial(models.Model):
    customer_name = models.CharField(max_length=100)
    feedback = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.customer_name
