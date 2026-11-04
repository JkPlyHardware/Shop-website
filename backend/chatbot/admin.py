from django.contrib import admin
from .models import ChatFAQ, AIUsage
@admin.register(ChatFAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ["question", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["question", "answer", "keywords"]
@admin.register(AIUsage)
class AIUsageAdmin(admin.ModelAdmin):
    list_display = ["provider", "input_tokens", "output_tokens", "estimated_cost", "status", "created_at"]
    list_filter = ["provider", "status", "created_at"]
    readonly_fields = [f.name for f in AIUsage._meta.fields]
    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
