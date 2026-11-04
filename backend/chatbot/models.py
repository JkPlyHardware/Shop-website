from django.db import models
class ChatFAQ(models.Model):
    question = models.CharField(max_length=250)
    answer = models.TextField()
    keywords = models.CharField(max_length=500, help_text="Comma-separated words or phrases")
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.question
class AIUsage(models.Model):
    PROVIDERS = [("mock", "Mock"), ("gemini", "Gemini"), ("sarvam", "Sarvam")]
    STATUS = [("reserved", "Reserved"), ("success", "Success"), ("failed", "Failed"), ("faq", "FAQ response"), ("blocked", "Budget blocked")]
    provider = models.CharField(max_length=20, choices=PROVIDERS)
    input_tokens = models.PositiveIntegerField(default=0)
    output_tokens = models.PositiveIntegerField(default=0)
    estimated_cost = models.DecimalField(max_digits=12, decimal_places=6, default=0)
    status = models.CharField(max_length=12, choices=STATUS, default="reserved")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    def __str__(self): return f"{self.provider} / {self.status} / {self.created_at:%Y-%m-%d}"


class AIBudgetMutex(models.Model):
    """Singleton row locked during token/spend reservations (effective on PostgreSQL)."""
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return "AI budget reservation lock"
