# Architecture

```text
Browser (React + Vite)
  ├── Public catalogue API ── Django REST Framework ── products/categories
  ├── Contact and quote APIs ── enquiries
  ├── Campaign API ── campaigns / timed visibility
  └── FAQ/chat endpoint ── chatbot ── optional Gemini OR Sarvam provider
                                         └── AIUsage records and configured budgets
Django ORM ── SQLite (local default) OR Supabase PostgreSQL (DATABASE_URL)
Django Admin ── products, enquiries, campaigns, FAQs, AI usage
```

Django owns business logic and admin permissions. The browser never receives AI keys or database credentials. The project is a catalogue/enquiry platform, not a payment checkout.
