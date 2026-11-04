from django.urls import path
from .views import AdminSummary
urlpatterns = [path("admin/summary/", AdminSummary.as_view(), name="admin-summary")]
