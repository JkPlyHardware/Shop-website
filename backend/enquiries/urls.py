from django.urls import path
from .views import ContactCreate, QuoteCreate
urlpatterns = [path("contact/", ContactCreate.as_view(), name="contact"), path("quotes/", QuoteCreate.as_view(), name="quote")]
