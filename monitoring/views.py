from django.http import JsonResponse

def health_check(request):
    """Une vue simple qui renvoie un statut de succès."""
    return JsonResponse({"status": "ok", "message": "API is healthy"})

def trigger_error(request):
    """Une vue conçue pour créer une erreur 500."""
    division_by_zero = 1 / 0
    return JsonResponse({"this": "will never be returned"})