from rest_framework import serializers
from .models import ContactMessage, CustomerEnquiry

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ["id", "name", "email", "phone", "message", "created_at"]
        read_only_fields = ["id", "created_at"]
    def validate(self, attrs):
        if not attrs.get("phone") and not attrs.get("email"):
            raise serializers.ValidationError("Please provide a phone number or email address.")
        return attrs

class CustomerEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerEnquiry
        fields = ["id", "customer_name", "phone", "email", "product", "product_name", "message", "created_at"]
        read_only_fields = ["id", "created_at"]
    def validate_phone(self, value):
        digits = "".join(ch for ch in value if ch.isdigit())
        if len(digits) < 10 or len(digits) > 15: raise serializers.ValidationError("Enter a valid phone number.")
        return value
