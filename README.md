# JK Ply Hardware & Furniture Workshop — Local Website

A locally runnable business catalogue and enquiry platform built with React/Vite/Tailwind and Django REST Framework. It includes a responsive glassmorphism mobile menu, light/dark themes, product catalogue, quote/contact forms, festival campaign banners, admin management, FAQ-first chatbot, and optional Gemini/Sarvam AI adapters.

## Business information included

Only details already supplied in the project brief/screenshot are prefilled: JK Ply Hardware & Furniture Workshop, Patna, Bihar; phone `+91 96613 82988`; wooden doors, tables, beds, bed tables, custom furniture, plywood, laminates and hardware; own workshop; made-to-measure work; and written price confirmation before work starts. No street address, opening hours, product prices or customer reviews are fabricated.

## Requirements

- Node.js 20+ and npm
- Python 3.10+
- Optional: PostgreSQL/Supabase and Redis for production-like local testing

## Start locally

### 1. Backend

```bash
cd backend
python -m venv venv
# Windows PowerShell: .\venv\Scripts\Activate.ps1
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env   # Windows CMD; on macOS/Linux use: cp .env.example .env
python manage.py makemigrations products enquiries campaigns chatbot analytics
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

API: `http://127.0.0.1:8000/api/`  
Admin: `http://127.0.0.1:8000/admin/`

### 2. Frontend (new terminal)

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open the Vite URL printed by the terminal (normally `http://localhost:5173`).

## Local defaults

- SQLite is used unless `DATABASE_URL` is supplied.
- `AI_PROVIDER=mock` means the chatbot uses FAQ answers and a safe demo response. No paid API is called.
- Product list starts empty except when you run `python manage.py seed_demo`.
- The public site does not show unverified reviews, made-up prices, opening hours or street addresses.
- Festival campaigns are created from Django admin and only shown between their start and end dates while enabled and complete.

## Supabase PostgreSQL

Set `DATABASE_URL` in `backend/.env` to your Supabase PostgreSQL connection string, for example the pooler connection string supplied by your Supabase project. Ensure the password is URL-encoded. Run migrations after setting it. Keep database credentials only in the backend environment.

## Optional AI configuration

Set `AI_PROVIDER=gemini` with `GEMINI_API_KEY`, or `AI_PROVIDER=sarvam` with `SARVAM_API_KEY`. The backend supports only the configured provider and never fails over to another paid provider. The provider call is disabled by default (`mock`). Keep keys out of frontend environment variables. Configure limits in `.env`; review the AI usage records in Django admin.

Sarvam uses its Chat Completion API (`POST https://api.sarvam.ai/v1/chat/completions`, `api-subscription-key` header). Gemini uses the Generative Language `generateContent` REST endpoint. Provider pricing changes; set cost-per-million-token values from your own provider billing page instead of assuming the defaults are current.

## Important implementation notes

- Request throttles are enforced on the backend. The default local cache is process-local and is not distributed production protection. Set `REDIS_URL` to use Redis-backed cache.
- Contact/quote submissions accept an `Idempotency-Key` header to reduce duplicate submissions. This does not replace backend validation or throttling.
- Admin login has a configurable IP guard (5 attempts per 15 minutes by default); use Redis for shared production enforcement.
- Chatbot has separate 5-per-minute and 30-per-day throttles.
- Django admin permissions protect campaign, product, enquiry and AI usage management.
- The campaign event endpoint stores anonymous event type and campaign reference only; it does not collect visitor names or email addresses.
- Image upload validation checks extension, MIME type, size and decoded image content via Pillow.
- Configure `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`, HTTPS and secrets before any public deployment. This project is intentionally not deployed.

## Tests and checks

```bash
cd backend
python manage.py check
python manage.py test
cd ../frontend
npm run lint
npm run build
```

The generated project has not been run in your local environment. Run these commands after installation and treat their output as the real test result.

## Responsive verification checklist

Check the navbar/menu and page at 320, 375, 425, 768, 1024 and 1440 pixels. Automated browser/device testing is not included in this source package.
