# -*- coding: utf-8 -*-
from common import *

INSTALLED_APPS += (
    'provider',
    'provider.oauth2',
)

REST_FRAMEWORK.update(
    {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.OAuth2Authentication',
        ),
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.AllowAny',
        ),
    }
)
