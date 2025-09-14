import os

# Pour bien interpréter une variable d'environnement numérique comme une valeur numérique et non une chaine de caractères
def env_int(k):
    return int(os.getenv(k))

# Pour bien interpréter une variable d'environnement booléenne comme une valeur booléenne et non une chaine de caractères
def env_bool(k, default="False"):
    return str(os.getenv(k)).strip().lower() in {"1","true","yes","on"}