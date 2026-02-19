"""
Production settings for expense tracker project.
Use this configuration for production deployment.
"""

from .settings import *
import os

# SECURITY SETTINGS FOR PRODUCTION
DEBUG = False

# Generate a new secret key for production
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'change-this-to-a-very-long-random-string-in-production')

# Allowed hosts - update with your domain
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# HTTPS Security Settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Database configuration for PostgreSQL (recommended for production)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME', 'expense_tracker'),
#         'USER': os.environ.get('DB_USER', 'postgres'),
#         'PASSWORD': os.environ.get('DB_PASSWORD'),
#         'HOST': os.environ.get('DB_HOST', 'localhost'),
#         'PORT': os.environ.get('DB_PORT', '5432'),
#     }
# }

# Email configuration for production
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.environ.get('EMAIL_HOST')
# EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '/path/to/django/logs/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
