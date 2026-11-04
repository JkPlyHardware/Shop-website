# API

All endpoints are prefixed with `/api/`.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `health/` | API health |
| GET | `categories/` | Public category list |
| GET | `products/` | Public published products; supports `?search=`, `?category=`, `?featured=true` |
| GET | `products/<slug>/` | Product detail |
| GET | `testimonials/` | Published testimonials only |
| POST | `contact/` | Contact message; 3 requests/10 minutes/IP default |
| POST | `quotes/` | Quote request; 5 requests/hour/IP default |
| GET | `campaigns/active/` | Currently scheduled and enabled banners |
| POST | `campaigns/<id>/event/` | Anonymous impression/click/CTA event |
| POST | `chatbot/` | FAQ-first assistant; 5 messages/minute/IP default |
| GET | `admin/summary/` | Admin-only summary |

Contact body: `{ "name": "...", "email": "optional", "phone": "...", "message": "..." }`

Quote body: `{ "customer_name": "...", "phone": "...", "email": "optional", "product_name": "...", "message": "..." }`

Chat body: `{ "message": "...", "history": [{"role":"user|assistant","content":"..."}] }` (maximum 500 characters; history bounded to six entries).
