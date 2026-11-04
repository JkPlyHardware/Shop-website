from rest_framework import serializers
from .models import FestivalBanner
class FestivalBannerSerializer(serializers.ModelSerializer):
    desktop_image_url = serializers.SerializerMethodField()
    mobile_image_url = serializers.SerializerMethodField()
    class Meta:
        model = FestivalBanner
        fields = ["id", "title", "festival_type", "heading", "description", "offer_text", "desktop_image_url", "mobile_image_url", "button_text", "button_url", "start_datetime", "end_datetime", "priority"]
    def get_desktop_image_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.desktop_image.url) if request and obj.desktop_image else (obj.desktop_image.url if obj.desktop_image else None)
    def get_mobile_image_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.mobile_image.url) if request and obj.mobile_image else (obj.mobile_image.url if obj.mobile_image else None)
