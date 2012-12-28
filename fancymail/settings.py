from django.conf import settings


# Add default settings for backend
EMAIL_BACKEND = getattr(settings,
                    'EMAIL_BACKEND',
                    'django.core.mail.backends.smtp.EmailBackend')
