from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from .models import ContactMessage, CustomerEnquiry
from .serializers import ContactMessageSerializer, CustomerEnquirySerializer

class ContactCreate(generics.CreateAPIView):
    serializer_class = ContactMessageSerializer; permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]; throttle_scope = "contact"
    def create(self, request, *args, **kwargs):
        key = request.headers.get("Idempotency-Key", "")[:80]
        if key:
            existing = ContactMessage.objects.filter(idempotency_key=key).first()
            if existing: return Response({"message": "Your message was already received.", "id": existing.id}, status=200)
        serializer = self.get_serializer(data=request.data); serializer.is_valid(raise_exception=True)
        obj = serializer.save(idempotency_key=key or None)
        return Response({"message": "Thank you. Your message has been received.", "id": obj.id}, status=status.HTTP_201_CREATED)

class QuoteCreate(generics.CreateAPIView):
    serializer_class = CustomerEnquirySerializer; permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]; throttle_scope = "quote"
    def create(self, request, *args, **kwargs):
        key = request.headers.get("Idempotency-Key", "")[:80]
        if key:
            existing = CustomerEnquiry.objects.filter(idempotency_key=key).first()
            if existing: return Response({"message": "Your quote request was already received.", "id": existing.id}, status=200)
        serializer = self.get_serializer(data=request.data); serializer.is_valid(raise_exception=True)
        obj = serializer.save(idempotency_key=key or None)
        return Response({"message": "Your quote request has been received.", "id": obj.id}, status=status.HTTP_201_CREATED)
