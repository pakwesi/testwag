from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(4vm3f@@9sg_opu)-l&6e$4_hj*%%oe+b)#*rjbt187b!3jz$a'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['67.205.181.146','*',]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS = INSTALLED_APPS + [
    'wagtail.contrib.styleguide',
]

try:
    from .local import *
except ImportError:
    pass
