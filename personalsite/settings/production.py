from .base import *

DEBUG = False

ALLOWED_HOSTS = ['67.205.181.146']

try:
    from .local import *
except ImportError:
    pass
