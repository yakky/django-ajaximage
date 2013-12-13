# -*- coding: utf-8 -*-
from django.conf import settings


PREPEND_MEDIA_URL = getattr(settings, 'AJAXIMAGE_PREPEND_MEDIA_URL', True)
UPLOAD_PATH = getattr(settings, 'AJAXIMAGE_UPLOAD_PATH', 'ajaximage/')
