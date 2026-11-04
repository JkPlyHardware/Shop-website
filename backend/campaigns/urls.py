from django.urls import path
from .views import ActiveCampaignList, CampaignEventCreate
urlpatterns = [path("campaigns/active/", ActiveCampaignList.as_view(), name="active-campaigns"), path("campaigns/<int:campaign_id>/event/", CampaignEventCreate.as_view(), name="campaign-event")]
