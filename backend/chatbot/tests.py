from django.test import TestCase
from rest_framework.test import APIClient
from .models import ChatFAQ
class FAQChatTests(TestCase):
    def test_faq_answer_does_not_need_provider_api_key(self):
        ChatFAQ.objects.create(question="Contact", answer="Call +91 96613 82988", keywords="call,phone")
        response=APIClient().post("/api/chatbot/", {"message":"What is your phone number?"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["mode"], "faq")
