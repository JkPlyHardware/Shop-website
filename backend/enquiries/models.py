from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField(max_length=3000)
    idempotency_key = models.CharField(max_length=80, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Contact from {self.name}"

class CustomerEnquiry(models.Model):
    STATUS = [("new", "New"), ("contacted", "Contacted"), ("in_progress", "In progress"), ("closed", "Closed")]
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    product = models.ForeignKey("products.Product", on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=180, blank=True)
    message = models.TextField(max_length=3000, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="new")
    idempotency_key = models.CharField(max_length=80, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Quote: {self.customer_name} ({self.phone})"
