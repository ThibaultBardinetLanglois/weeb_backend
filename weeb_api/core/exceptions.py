from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF.

    Extends the default handler to provide clearer, user-friendly error
    messages, including specific handling for expired or invalid JWT tokens.
    """
    response = exception_handler(exc, context)

    if response is not None and isinstance(response.data, dict):
        code = response.data.get("code")

        # Case: SimpleJWT – invalid/expired token
        if code == "token_not_valid":
            response.data["detail"] = "Le jeton fourni n’est pas valide."
            
            messages = []
            for msg in response.data.get("messages", []):
                token_class = msg.get("token_class", "")
                token_type = msg.get("token_type", "")

                traduction = {
                    "token_class": token_class,
                    "token_type": token_type,
                    "message": "Le jeton est expiré ou invalide."
                }

                # Specific case: expired AccessToken
                if token_class == "AccessToken":
                    traduction["message"] = "Le jeton d’accès est expiré. Veuillez vous reconnecter."
                elif token_class == "RefreshToken":
                    traduction["message"] = "Le jeton de rafraîchissement est expiré ou invalide. Veuillez vous reconnecter."

                messages.append(traduction)

            # Fallback generic message if none were provided
            if not messages:
                messages = [
                    {"message": "Le jeton est invalide ou manquant. Veuillez fournir un jeton valide."}
                ]

            response.data["messages"] = messages

        # Other common DRF errors
        if code == "authentication_failed":
            response.data["detail"] = "Échec de l’authentification. Vérifiez vos identifiants."
        elif code == "not_authenticated":
            response.data["detail"] = "Vous devez être connecté pour accéder à cette ressource."
        elif code == "permission_denied":
            response.data["detail"] = "Vous n’avez pas les permissions nécessaires pour accéder à cette ressource."

    return response