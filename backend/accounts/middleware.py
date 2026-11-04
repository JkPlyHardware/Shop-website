from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class AdminLoginRateLimitMiddleware(MiddlewareMixin):
    """Simple IP-based guard for Django admin login POSTs. Use Redis in production."""
    def _key(self, request):
        # Use the transport peer address; do not trust client-supplied X-Forwarded-For.
        # Configure trusted proxy handling at the server layer if deployed behind one.
        ip = request.META.get("REMOTE_ADDR", "unknown")
        return f"jk-admin-login:{ip}"

    def process_request(self, request):
        if request.path == "/admin/login/" and request.method == "POST":
            attempts = cache.get(self._key(request), 0)
            if attempts >= int(getattr(settings, "ADMIN_LOGIN_MAX_ATTEMPTS", 5)):
                return JsonResponse({"detail": "Too many login attempts. Try again after 15 minutes."}, status=429)
        return None

    def process_response(self, request, response):
        if request.path == "/admin/login/" and request.method == "POST":
            key = self._key(request)
            if response.status_code in (301, 302, 303):
                cache.delete(key)
            elif response.status_code == 200:
                context = getattr(response, "context_data", None) or {}
                form = context.get("form")
                failed = bool(getattr(form, "errors", None)) if form is not None else False
                if failed:
                    try: cache.incr(key)
                    except ValueError: cache.set(key, 1, timeout=getattr(settings, "ADMIN_LOGIN_WINDOW_SECONDS", 900))
        return response
