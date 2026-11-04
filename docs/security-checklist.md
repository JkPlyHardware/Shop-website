# Security checklist

- [ ] Replace `DJANGO_SECRET_KEY` with a long random secret.
- [ ] Set `DJANGO_DEBUG=False` for production.
- [ ] Set exact `DJANGO_ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS`.
- [ ] Use HTTPS and secure cookies in production.
- [ ] Keep `.env` and all provider/database keys out of source control.
- [ ] Use Redis for shared production rate limits; local-memory cache is only for development.
- [ ] Review rate-limit values and infrastructure-level protections.
- [ ] Configure database backups and restore tests.
- [ ] Set actual provider token prices in env for estimated-cost reporting.
- [ ] Keep staff/admin accounts protected with strong unique passwords and MFA at the hosting layer where available.
- [ ] Review image upload limits and permitted media origins.
- [ ] Check dependencies for vulnerabilities before deployment.
