from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings
from .validators import validate_campaign_image

class FestivalBanner(models.Model):
    FESTIVAL_CHOICES = [(x, x.replace("_", " ").title()) for x in ["diwali","chhath_puja","holi","durga_puja","dussehra","navratri","eid","christmas","new_year","makar_sankranti","raksha_bandhan","wedding_season","shop_promotion","clearance_sale","new_launch","other"]]
    LOCATION_CHOICES = [("home", "Homepage"), ("all", "All pages")]
    title = models.CharField(max_length=150)
    festival_type = models.CharField(max_length=30, choices=FESTIVAL_CHOICES, default="shop_promotion")
    heading = models.CharField(max_length=180)
    description = models.CharField(max_length=500, blank=True)
    offer_text = models.CharField(max_length=180, blank=True)
    desktop_image = models.ImageField(upload_to="campaigns/desktop/", validators=[validate_campaign_image])
    mobile_image = models.ImageField(upload_to="campaigns/mobile/", blank=True, null=True, validators=[validate_campaign_image])
    button_text = models.CharField(max_length=40, blank=True)
    button_url = models.CharField(max_length=500, blank=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    priority = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)
    display_location = models.CharField(max_length=10, choices=LOCATION_CHOICES, default="home")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-priority", "start_datetime"]
        indexes = [models.Index(fields=["is_active", "start_datetime", "end_datetime"])]
    def clean(self):
        if self.end_datetime <= self.start_datetime:
            raise ValidationError({"end_datetime": "End time must be after start time."})
        if self.button_url and not (self.button_url.startswith("/") or self.button_url.startswith("https://")):
            raise ValidationError({"button_url": "Use a local path or a secure https:// URL."})
        if self.button_text and not self.button_url:
            raise ValidationError({"button_url": "Add a destination when a CTA button is configured."})
    @property
    def is_currently_visible(self):
        now = timezone.now()
        return self.is_active and bool(self.desktop_image) and bool(self.heading.strip()) and self.start_datetime <= now <= self.end_datetime
    def __str__(self): return self.title

class CampaignEvent(models.Model):
    EVENT_CHOICES = [("impression", "Impression"), ("click", "Click"), ("cta", "CTA click")]
    campaign = models.ForeignKey(FestivalBanner, on_delete=models.CASCADE, related_name="events")
    event_type = models.CharField(max_length=12, choices=EVENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    class Meta: indexes = [models.Index(fields=["campaign", "event_type", "created_at"])]
    def __str__(self): return f"{self.campaign.title}: {self.event_type}"
