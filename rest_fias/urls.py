# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_fias import views
from rest_fias.router import AddressRouter


router = AddressRouter()
router.register(r'ao', views.AddressObjectViewSet, base_name='ao')\
    .register(r'houses', views.HouseViewSet, base_name='houses',
              parents_query_lookups=['aoguid'])

urlpatterns = patterns('',
    url(r'^v1/', include(router.urls), name='fias-v1'),
)