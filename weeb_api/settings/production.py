import dj_database_url
from .base import *

# ==============================================================================
# SECURITY
# ==============================================================================

# To avoid exposing the code and especially the configuration we must define DEBUG=False but during this testing phase we prefer to have the choice
# So we choose to let the variable in settings/base.py

# ==============================================================================
# DATABASE
# ==============================================================================

DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        ssl_require=True
    )
}

# ==============================================================================
# STATIC FILES (WHITENOISE)
# ==============================================================================

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# More restrictive CORS, HOST configuration for production
# The authorized origins and domain names used to access the site are read from an environment variable contained in the host's configuration.
# The secret key for signing tokens and cookies follows the same process