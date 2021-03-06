# -*- coding: utf-8 -*-
from fias.models import AddrObj, House
from rest_framework import viewsets
from rest_framework import filters
from rest_framework_extensions.mixins import DetailSerializerMixin, NestedViewSetMixin
from rest_fias import serializers
from rest_fias.filters import AddressScanFilter, MultiValuesFilterBackend


class DetailSerializerSwitcherMixin(DetailSerializerMixin):
    """
    Add custom serializer for view by switcher
    """
    serializer_switcher_param = 'view'

    def get_serializer_class(self):
        switcher = self.get_switch_param(self.request)
        if isinstance(self.serializer_detail_class, dict) and \
                getattr(self, 'object', None):
            return self.serializer_detail_class.get(
                switcher,
                self.serializer_detail_class[None]
            )
        elif isinstance(self.serializer_class, dict) and \
                not getattr(self, 'object', None):
            return self.serializer_class.get(
                switcher,
                self.serializer_class[None]
            )
        return super(DetailSerializerSwitcherMixin, self).get_serializer_class()

    def get_switch_param(self, request):
        return request.QUERY_PARAMS.get(self.serializer_switcher_param, None)


class DetailSerializerNestedViewMixin(DetailSerializerSwitcherMixin,
                                      NestedViewSetMixin):
    def get_queryset(self, is_for_detail=False):
        return self.filter_queryset_by_parents_lookups(
            super(DetailSerializerNestedViewMixin, self).get_queryset(is_for_detail)
        )


class AddressObjectViewSet(DetailSerializerNestedViewMixin,
                           viewsets.ReadOnlyModelViewSet):
    u"""
    Адресные объекты
    """
    model = AddrObj
    serializer_class = {
        None: serializers.AddrObjListSerializer,
        'simple': serializers.SimpleAddrObjListSerializer
    }
    serializer_detail_class = {
        None: serializers.AddrObjSerializer,
        'withparents': serializers.AddrObjWithParentsSerializer,
    }
    paginate_by = 50
    filter_backends = (MultiValuesFilterBackend,
                       filters.SearchFilter,
                       AddressScanFilter)
    filter_fields = ('aolevel', 'code', 'parentguid')
    search_fields = ('formalname', 'shortname')
    scan_fields = ('formalname',)

    @classmethod
    def get_lookup_format(cls, router, lookup_prefix=''):
        if router.trailing_slash:
            lookup_format = '[0-9a-fA-F\-^/]{36}'
        else:
            lookup_format = '[0-9a-fA-F\-^/.]{36}'
        return lookup_format

    def list(self, request, *args, **kwargs):
        u"""
        Список адресных объектов
        """
        return super(AddressObjectViewSet, self).list(request, *args, **kwargs)


    def retrieve(self, request, *args, **kwargs):
        u"""
        Адресный объект
        """
        return super(AddressObjectViewSet, self).retrieve(request, *args, **kwargs)


class HouseViewSet(DetailSerializerNestedViewMixin,
                   viewsets.ReadOnlyModelViewSet):
    u"""
    Список домов в адресном объекте
    """
    model = House
    serializer_class = serializers.HouseListSerializer
    serializer_detail_class = serializers.HouseSerializer
    paginate_by = 50
    filter_backends = (filters.DjangoFilterBackend,
                       filters.SearchFilter)
    search_fields = ('housenum',)

    def retrieve(self, request, *args, **kwargs):
        u"""
        Дом
        """
        return super(HouseViewSet, self).retrieve(request, *args, **kwargs)

