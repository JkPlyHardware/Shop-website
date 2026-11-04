from django.utils import timezone
from django.db.models import Sum, Count
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from chatbot.models import AIUsage
from enquiries.models import ContactMessage, CustomerEnquiry
from campaigns.models import FestivalBanner, CampaignEvent
import os

class AdminSummary(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        today = timezone.localdate()
        usage = AIUsage.objects.filter(created_at__date=today)
        month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_usage = AIUsage.objects.filter(created_at__gte=month_start)
        month_tokens = (month_usage.aggregate(v=Sum("input_tokens"))["v"] or 0) + (month_usage.aggregate(v=Sum("output_tokens"))["v"] or 0)
        token_budget = int(os.getenv("AI_MONTHLY_TOKEN_BUDGET", "500000"))
        token_pct = round((month_tokens / token_budget) * 100, 1) if token_budget else 100
        return Response({
            "monthly_ai_tokens": month_tokens,
            "monthly_ai_token_budget": token_budget,
            "monthly_ai_budget_remaining": max(0, token_budget - month_tokens),
            "budget_warning": token_pct >= 80,
            "monthly_ai_budget_used_percent": token_pct,
            "contact_messages": ContactMessage.objects.count(),
            "quote_requests": CustomerEnquiry.objects.count(),
            "active_campaigns": FestivalBanner.objects.filter(is_active=True).count(),
            "today_ai_requests": usage.exclude(status="faq").count(),
            "today_input_tokens": usage.aggregate(v=Sum("input_tokens"))["v"] or 0,
            "today_output_tokens": usage.aggregate(v=Sum("output_tokens"))["v"] or 0,
            "today_ai_estimated_cost": str(usage.aggregate(v=Sum("estimated_cost"))["v"] or 0),
            "campaign_events": CampaignEvent.objects.filter(created_at__date=today).count(),
        })
