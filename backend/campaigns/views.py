from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import ScopedRateThrottle
from .models import FestivalBanner, CampaignEvent
from .serializers import FestivalBannerSerializer

class ActiveCampaignList(generics.ListAPIView):
    serializer_class = FestivalBannerSerializer; permission_classes = [AllowAny]
    def get_queryset(self):
        now = timezone.now()
        return FestivalBanner.objects.filter(is_active=True, start_datetime__lte=now, end_datetime__gte=now, display_location__in=["home", "all"]).exclude(desktop_image="").order_by("-priority", "start_datetime")[:5]

class CampaignEventCreate(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]; throttle_scope = "banner_event"
    def post(self, request, campaign_id):
        event_type = request.data.get("event_type")
        if event_type not in {"impression", "click", "cta"}:
            return Response({"error": "Invalid event type."}, status=400)
        user_agent = request.META.get("HTTP_USER_AGENT", "").lower()
        if any(token in user_agent for token in ["bot", "crawler", "spider", "preview", "facebookexternalhit"]):
            return Response({"recorded": False, "reason": "automated client"}, status=202)
        campaign = FestivalBanner.objects.filter(pk=campaign_id, is_active=True).first()
        if not campaign: return Response({"error": "Campaign not found."}, status=404)
        CampaignEvent.objects.create(campaign=campaign, event_type=event_type)
        return Response({"recorded": True}, status=status.HTTP_201_CREATED)
