#coding: utf-8
from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fias/', include('rest_fias.urls')),
    #url(r'^docs/', include('rest_framework_swagger.urls')),
)

if 'provider.oauth2' in settings.INSTALLED_APPS:
    urlpatterns.extend(
        patterns('',
            url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2'))
        )
    )