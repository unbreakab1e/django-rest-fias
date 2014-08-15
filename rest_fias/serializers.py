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
            'aolevel', 'code', 'fullname', 'postalcode',
        )


class AddrObjSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField(method_name='get_fullname')

    def get_fullname(self, obj):
        return obj.full_name(depth=5)

    class Meta:
        model = AddrObj
        fields = (
            'aoguid', 'parentguid', 'aoid', 'previd', 'nextid',
            'ifnsfl', 'terrifnsfl', 'ifnsul', 'terrifnsul',
            'okato', 'oktmo', 'postalcode',
            'formalname', 'offname', 'shortname', 'aolevel',
            'regioncode', 'autocode', 'areacode', 'citycode',
            'ctarcode', 'placecode', 'streetcode', 'extrcode', 'sextcode',
            'code', 'plaincode', 'actstatus', 'centstatus',
            'operstatus', 'currstatus', 'livestatus', 'fullname',
            'updatedate', 'startdate', 'enddate', 'normdoc',
        )


class HouseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = (
            'houseguid', 'houseid', 'aoguid', 'housenum',
            'buildnum', 'strucnum'
        )


class HouseSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField(method_name='get_address')

    def get_address(self, obj):
        addr_str = u'{index}, {fullname}'
        index = obj.postalcode if obj.postalcode else obj.aoguid.postalcode
        if obj.housenum:
            addr_str += u', д {housenum}'
        if obj.buildnum:
            addr_str += u' ст {buildnum}'
        if obj.strucnum:
            addr_str += u' к {strucnum}'
        return addr_str.format(
            index=index,
            fullname=obj.aoguid.full_name(depth=5),
            housenum=obj.housenum,
            buildnum=obj.buildnum,
            strucnum=obj.strucnum,
        )

    class Meta:
        model = House
        fields = (
            'houseguid', 'houseid', 'aoguid',
            'ifnsfl', 'terrifnsfl', 'ifnsul', 'terrifnsul',
            'okato', 'oktmo', 'postalcode',
            'housenum', 'address',
            'eststatus', 'buildnum', 'strucnum', 'strstatus', 'statstatus', 'counter',
            'updatedate', 'startdate', 'enddate', 'normdoc',
        )