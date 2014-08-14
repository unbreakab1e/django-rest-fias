# -*- coding: utf-8 -*-
from rest_framework import routers
from rest_framework_extensions.routers import ExtendedRouterMixin


class AddressRouter(ExtendedRouterMixin,
                    routers.DefaultRouter):

    def get_lookup_regex(self, viewset, lookup_prefix=''):
        if hasattr(viewset, 'get_lookup_format') and callable(viewset.get_lookup_format):
            lookup_format = viewset.get_lookup_format(router=self, lookup_prefix=lookup_prefix)
        else:
            if self.trailing_slash:
                lookup_format = '[^/]+'
            else:
                # Don't consume `.json` style suffixes
                lookup_format = '[^/.]+'
        base_regex = '(?P<{lookup_prefix}{lookup_field}>{lookup_format})'
        lookup_field = getattr(viewset, 'lookup_field', 'pk')
        return base_regex.format(lookup_field=lookup_field,
                                 lookup_prefix=lookup_prefix,
                                 lookup_format=lookup_format)