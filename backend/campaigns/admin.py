from django.contrib import admin
from .models import FestivalBanner, CampaignEvent
@admin.register(FestivalBanner)
class FestivalBannerAdmin(admin.ModelAdmin):
    list_display = ["title", "festival_type", "start_datetime", "end_datetime", "priority", "is_active"]
    list_filter = ["festival_type", "is_active", "display_location"]
    search_fields = ["title", "heading", "description"]
    readonly_fields = ["created_at", "updated_at"]
    actions = ["duplicate_campaign"]
    @admin.action(description="Duplicate selected campaigns as disabled drafts")
    def duplicate_campaign(self, request, queryset):
        for campaign in queryset:
            campaign.pk = None; campaign.title = f"{campaign.title} (copy)"; campaign.is_active = False; campaign.save()
@admin.register(CampaignEvent)
class CampaignEventAdmin(admin.ModelAdmin):
    list_display = ["campaign", "event_type", "created_at"]
    list_filter = ["event_type", "created_at"]
    readonly_fields = ["campaign", "event_type", "created_at"]
