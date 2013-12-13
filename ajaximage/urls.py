try:# pre 1.6
    from django.conf.urls.defaults import url, patterns
except ImportError:
    from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required, user_passes_test

from .views import (ajaximage, ajaxgeneric, ajaxgeneric_auth, ajaximage_auth,
                    ajaxgeneric_staff, ajaximage_staff)
from .forms import FileForm


urlpatterns = patterns('',
    url('^upload/image/(?P<upload_to>.*)/(?P<max_width>\d+)/(?P<max_height>\d+)/(?P<crop>\d+)',
        ajaximage, {
            'form_class': FileForm,
        }, name='ajaximage'),
    url('^upload/file/(?P<upload_to>.*)',
        ajaxgeneric, {
            'form_class': FileForm,
        }, name='ajaxfile'),
    url('^upload/auth/image/(?P<upload_to>.*)/(?P<max_width>\d+)/(?P<max_height>\d+)/(?P<crop>\d+)',
        ajaximage_auth, {
            'form_class': FileForm,
        }, name='ajaximage_auth'),
    url('^upload/auth/file/(?P<upload_to>.*)',
        ajaxgeneric_auth, {
            'form_class': FileForm,
        }, name='ajaxfile_auth'),
    url('^upload/staff/image/(?P<upload_to>.*)/(?P<max_width>\d+)/(?P<max_height>\d+)/(?P<crop>\d+)',
        ajaximage_staff, {
            'form_class': FileForm,
        }, name='ajaximage_staff'),
    url('^upload/staff/file/(?P<upload_to>.*)',
        ajaxgeneric_staff, {
            'form_class': FileForm,
        }, name='ajaxfile_staff'),
)
