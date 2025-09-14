from rest_framework.throttling import SimpleRateThrottle, AnonRateThrottle, UserRateThrottle

class _AdminBypassMixin:
    """Si l'utilisateur est admin (staff/superuser), on ne throttle pas."""
    def get_cache_key(self, request, view):
        user = getattr(request, "user", None)
        if user and (user.is_staff or user.is_superuser):
            return None  # => désactive le throttle pour cet utilisateur
        return super().get_cache_key(request, view)

class AdminAwareAnonThrottle(_AdminBypassMixin, AnonRateThrottle):
    scope = "anon"

class AdminAwareUserThrottle(_AdminBypassMixin, UserRateThrottle):
    scope = "user"

class SiteWideIPThrottle(SimpleRateThrottle):
    """Plafond global par IP (filet anti-flood). Admin bypass aussi possible si tu veux."""
    scope = "sitewide_ip"
    def get_cache_key(self, request, view):
        user = getattr(request, "user", None)
        if user and (user.is_staff or user.is_superuser):
            return None  # enlève cette ligne si tu veux que l’IP admin soit quand même plafonnée
        return f"throttle_site:{self.get_ident(request)}"
