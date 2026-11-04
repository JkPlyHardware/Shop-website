from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from .models import FestivalBanner
class CampaignModelTests(TestCase):
    def test_end_must_follow_start(self):
        now=timezone.now()
        c=FestivalBanner(title="Test", heading="Test", start_datetime=now, end_datetime=now-timedelta(hours=1))
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError): c.full_clean()
