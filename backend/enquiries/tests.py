from django.test import TestCase
from rest_framework.test import APIClient
class EnquiryAPITests(TestCase):
    def test_contact_requires_a_contact_method(self):
        response = APIClient().post("/api/contact/", {"name": "Test", "message": "Hello"}, format="json")
        self.assertEqual(response.status_code, 400)
    def test_contact_accepts_phone(self):
        response = APIClient().post("/api/contact/", {"name": "Test", "phone": "9999999999", "message": "Hello"}, format="json", HTTP_IDEMPOTENCY_KEY="test-key-1")
        self.assertEqual(response.status_code, 201)
    def test_duplicate_key_returns_existing_record(self):
        client=APIClient(); data={"name":"Test","phone":"9999999999","message":"Hello"}
        first=client.post("/api/contact/", data, format="json", HTTP_IDEMPOTENCY_KEY="repeat-key")
        second=client.post("/api/contact/", data, format="json", HTTP_IDEMPOTENCY_KEY="repeat-key")
        self.assertEqual(first.status_code, 201); self.assertEqual(second.status_code, 200)
