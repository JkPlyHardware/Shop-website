from django.contrib import admin
from .models import ContactMessage, CustomerEnquiry
@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "email", "created_at"]
    search_fields = ["name", "phone", "email", "message"]
    readonly_fields = ["created_at"]
@admin.register(CustomerEnquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ["customer_name", "phone", "product_name", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["customer_name", "phone", "product_name", "message"]
