import os
import requests
from decimal import Decimal
from django.conf import settings
from django.db import transaction
from django.db.models import Sum, Count
from django.utils import timezone
from .models import AIUsage, AIBudgetMutex

class BudgetExceeded(Exception): pass

SYSTEM_PROMPT = "You are the JK Ply Hardware & Furniture Workshop website assistant in Patna, Bihar. Answer briefly and politely. Never invent product prices, availability, opening hours, exact street address, discounts or review claims. For current products, tell the visitor to submit an enquiry or contact +91 96613 82988."

def _estimate_tokens(text): return max(1, (len(text) + 3) // 4)

def _reserve(provider, input_tokens):
    """Reserve the configured max output tokens and estimated spend before provider use.

    PostgreSQL row-level locking serializes reservations. SQLite is a development
    fallback and does not provide the same concurrent reservation guarantee.
    """
    now = timezone.now()
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    month_start = day_start.replace(day=1)
    output_reserve = int(os.getenv("AI_MAX_OUTPUT_TOKENS", "250"))
    input_price = Decimal(os.getenv(f"AI_{provider.upper()}_INPUT_COST_PER_MILLION", "0"))
    output_price = Decimal(os.getenv(f"AI_{provider.upper()}_OUTPUT_COST_PER_MILLION", "0"))
    projected_cost = (Decimal(input_tokens) * input_price + Decimal(output_reserve) * output_price) / Decimal(1000000)
    with transaction.atomic():
        AIBudgetMutex.objects.get_or_create(pk=1)
        AIBudgetMutex.objects.select_for_update().get(pk=1)
        day_rows = AIUsage.objects.filter(created_at__gte=day_start).exclude(status__in=["faq", "blocked"])
        month_rows = AIUsage.objects.filter(created_at__gte=month_start).exclude(status__in=["faq", "blocked"])
        day_count = day_rows.count()
        month_count = month_rows.count()
        day_input = day_rows.aggregate(v=Sum("input_tokens"))["v"] or 0
        day_output = day_rows.aggregate(v=Sum("output_tokens"))["v"] or 0
        month_input = month_rows.aggregate(v=Sum("input_tokens"))["v"] or 0
        month_output = month_rows.aggregate(v=Sum("output_tokens"))["v"] or 0
        day_cost = day_rows.aggregate(v=Sum("estimated_cost"))["v"] or Decimal("0")
        month_cost = month_rows.aggregate(v=Sum("estimated_cost"))["v"] or Decimal("0")
        if day_count >= int(os.getenv("AI_DAILY_MESSAGE_LIMIT", "100")) or month_count >= int(os.getenv("AI_MONTHLY_MESSAGE_LIMIT", "2000")):
            raise BudgetExceeded("The assistant has reached its request limit. Please contact the workshop on WhatsApp.")
        if day_input + day_output + input_tokens + output_reserve > int(os.getenv("AI_DAILY_TOKEN_BUDGET", "50000")):
            raise BudgetExceeded("The assistant has reached its daily token budget. Please contact the workshop on WhatsApp.")
        if month_input + month_output + input_tokens + output_reserve > int(os.getenv("AI_MONTHLY_TOKEN_BUDGET", "500000")):
            raise BudgetExceeded("The assistant has reached its monthly token budget. Please contact the workshop on WhatsApp.")
        if day_cost + projected_cost > Decimal(os.getenv("AI_DAILY_SPEND_LIMIT", "10")):
            raise BudgetExceeded("The assistant has reached its daily spending limit. Please contact the workshop on WhatsApp.")
        if month_cost + projected_cost > Decimal(os.getenv("AI_MONTHLY_SPEND_LIMIT", "200")):
            raise BudgetExceeded("The assistant has reached its monthly spending limit. Please contact the workshop on WhatsApp.")
        return AIUsage.objects.create(provider=provider, input_tokens=input_tokens, output_tokens=output_reserve, estimated_cost=projected_cost, status="reserved")

def _provider_reply(provider, message, history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for item in history[-6:]:
        if item.get("role") in {"user", "assistant"} and isinstance(item.get("content"), str):
            messages.append({"role": item["role"], "content": item["content"][:500]})
    messages.append({"role": "user", "content": message})
    if provider == "gemini":
        key = os.getenv("GEMINI_API_KEY")
        if not key: raise RuntimeError("GEMINI_API_KEY is missing.")
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        contents = [{"role": "user" if m["role"] in {"user", "system"} else "model", "parts": [{"text": m["content"]}]} for m in messages]
        response = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
            json={"contents": contents, "generationConfig": {"maxOutputTokens": int(os.getenv("AI_MAX_OUTPUT_TOKENS", "250"))}}, timeout=20)
        response.raise_for_status(); data = response.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        usage = data.get("usageMetadata", {})
        return text, usage.get("promptTokenCount", 0), usage.get("candidatesTokenCount", _estimate_tokens(text))
    if provider == "sarvam":
        key = os.getenv("SARVAM_API_KEY")
        if not key: raise RuntimeError("SARVAM_API_KEY is missing.")
        response = requests.post("https://api.sarvam.ai/v1/chat/completions", headers={"api-subscription-key": key, "Content-Type": "application/json"},
            json={"model": os.getenv("SARVAM_MODEL", "sarvam-105b"), "messages": messages, "max_tokens": int(os.getenv("AI_MAX_OUTPUT_TOKENS", "250")), "reasoning_effort": None}, timeout=20)
        response.raise_for_status(); data = response.json(); text = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})
        return text, usage.get("prompt_tokens", 0), usage.get("completion_tokens", _estimate_tokens(text))
    return "Thanks for reaching JK Ply! For product details or a quote, please call +91 96613 82988 or send us an enquiry. Our team can confirm current availability and pricing.", _estimate_tokens(message), 40

def answer_message(message, history=None):
    message_l = message.lower()
    for faq in __import__("chatbot.models", fromlist=["ChatFAQ"]).ChatFAQ.objects.filter(is_active=True):
        terms = [x.strip().lower() for x in faq.keywords.split(",") if x.strip()]
        if any(term in message_l for term in terms):
            AIUsage.objects.create(provider="mock", status="faq")
            return faq.answer, "faq"
    provider = os.getenv("AI_PROVIDER", "mock").lower()
    history_text = " ".join(str(item.get("content", ""))[:500] for item in (history or [])[-6:] if item.get("role") in {"user", "assistant"})
    input_tokens = _estimate_tokens(message + SYSTEM_PROMPT + history_text)
    if input_tokens > int(os.getenv("AI_MAX_INPUT_TOKENS", "1500")):
        raise BudgetExceeded("Please shorten your message and try again.")
    usage = _reserve(provider, input_tokens)
    try:
        reply, actual_in, actual_out = _provider_reply(provider, message, history or [])
        usage.input_tokens = actual_in or input_tokens
        usage.output_tokens = actual_out or _estimate_tokens(reply)
        usage.status = "success"
        input_cost = Decimal(os.getenv(f"AI_{provider.upper()}_INPUT_COST_PER_MILLION", "0"))
        output_cost = Decimal(os.getenv(f"AI_{provider.upper()}_OUTPUT_COST_PER_MILLION", "0"))
        usage.estimated_cost = (Decimal(usage.input_tokens) * input_cost + Decimal(usage.output_tokens) * output_cost) / Decimal(1000000)
        usage.save(update_fields=["input_tokens", "output_tokens", "status", "estimated_cost"])
        return reply[:4000], provider
    except Exception:
        usage.status = "failed"; usage.save(update_fields=["status"])
        raise
