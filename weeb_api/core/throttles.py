from rest_framework.throttling import SimpleRateThrottle, AnonRateThrottle, UserRateThrottle

class _AdminBypassMixin:
    """
    Mixin to bypass throttling for admin users.

    If the user is staff or superuser, throttling is disabled.
    """
    def get_cache_key(self, request, view):
        user = getattr(request, "user", None)
        if user and (user.is_staff or user.is_superuser):
            return None  # => désactive le throttle pour cet utilisateur
        return super().get_cache_key(request, view)

class AdminAwareAnonThrottle(_AdminBypassMixin, AnonRateThrottle):
    """Anonymous throttle that ignores limits for admin users."""
    scope = "anon"

class AdminAwareUserThrottle(_AdminBypassMixin, UserRateThrottle):
    """User throttle that ignores limits for admin users."""
    scope = "user"

class SiteWideIPThrottle(SimpleRateThrottle):
    """
    Global throttle applied per IP address (anti-flood).

    Admin users are exempt by default. Remove the bypass logic if
    you want admin IPs to also be throttled.
    """
    scope = "sitewide_ip"
    def get_cache_key(self, request, view):
        user = getattr(request, "user", None)
        if user and (user.is_staff or user.is_superuser):
            return None  # Remove this line if admin IPs should still be throttled
        return f"throttle_site:{self.get_ident(request)}"
