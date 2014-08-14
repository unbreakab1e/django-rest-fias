# -*- coding: utf-8 -*-
from fias.models import AddrObj, House
from rest_framework import serializers


class AddrObjListSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField(method_name='get_fullname')

    def get_fullname(self, obj):
        return obj.full_name(depth=5)

    class Meta:
        model = AddrObj
        fields = (
            'aoguid', 'parentguid', 'formalname', 'offname', 'shortname',
            'aolevel', 'code', 'fullname',
        )


class AddrObjSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField(method_name='get_fullname')

    def get_fullname(self, obj):
        return obj.full_name(depth=5)

    class Meta:
        model = AddrObj
        fields = (
            'aoguid', 'parentguid', 'aoid', 'previd', 'nextid',
            'formalname', 'offname', 'shortname', 'aolevel',
            'regioncode', 'autocode', 'areacode', 'citycode',
            'ctarcode', 'placecode', 'streetcode', 'extrcode', 'sextcode',
            'code', 'plaincode', 'actstatus', 'centstatus',
            'operstatus', 'currstatus', 'livestatus', 'fullname',
        )


class HouseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = (
            'houseguid', 'houseid', 'aoguid', 'housenum',
            'buildnum', 'strucnum'
        )


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = (
            'houseguid', 'houseid', 'aoguid', 'housenum', 'eststatus', 'buildnum',
            'strucnum', 'strstatus', 'statstatus', 'counter'
        )