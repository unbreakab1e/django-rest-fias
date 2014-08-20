# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import connections
import django_filters
from rest_framework.filters import SearchFilter, DjangoFilterBackend, FilterSet


class ListFilter(django_filters.Filter):
    def filter(self, qs, value):
        return super(ListFilter, self).filter(qs, [value.split(","), 'in'])


class AddrFieldSet(FilterSet):
    aolevel = ListFilter(name='aolevel')
    code = django_filters.CharFilter(name='code', lookup_type='startswith')


class MultiValuesFilterBackend(DjangoFilterBackend):
    default_filter_set = AddrFieldSet


class AddressScanFilter(SearchFilter):
    search_param = 'scan'

    def filter_queryset(self, request, queryset, view):
        if getattr(settings, 'FIAS_SEARCH_ENGINE', None) == 'sphinx':
            return self.sphinx_filter(request, queryset, view)

        if connections[queryset.db].vendor != 'postgresql':
            return super(AddressScanFilter, self).filter_queryset(request, queryset, view)

        # сортируем по длине слова
        terms = sorted(self.get_search_terms(request),
                       key=lambda x: (-len(x), x))

        # Если не найдены объекты, содержащие все слова из фильтра,
        # то выберем все объекты, у которых есть родители с хотя бы
        # одним из указанных слов в официальном наименовании. (sic!)
        search_fields = getattr(view, 'scan_fields', None)

        if not search_fields or len(terms) == 0:
            return queryset

        # sql = '''
        #     WITH RECURSIVE nodes (aoguid, parentguid, formalname, found) AS (
        #       SELECT addr.aoguid, addr.parentguid, addr.formalname,
        #         case when addr.formalname like '%Ижевск%' then ARRAY['Ижевск']
        #              when addr.formalname like '%Союзная%' then ARRAY['Союзная']
        #         end
        #         FROM fias_addrobj addr
        #         WHERE (addr.formalname like '%Ижевск%' or addr.formalname like '%Союзная%')
        #       UNION ALL
        #       SELECT addr.aoguid, addr.parentguid, addr.formalname,
        #         case (when addr.formalname like '%Ижевск%')
        #                and not ('Ижевск' = ANY(nodes.found))
        #               then array_append(nodes.found, 'Ижевск')
        #              (when addr.formalname like '%Союзная%')
        #                and not ('Союзная' = ANY(nodes.found))
        #              then array_append(nodes.found, 'Союзная')
        #              else nodes.found
        #         end
        #         FROM fias_addrobj addr, nodes
        #         WHERE addr.parentguid = nodes.aoguid
        #     )
        #     SELECT aoguid FROM nodes WHERE array_length(found, 1) = 2
        # '''

        sql = u'''
            aoguid in (
            WITH RECURSIVE nodes (aoguid, parentguid, formalname, found) AS (
              SELECT addr.aoguid, addr.parentguid, addr.formalname,
                case {case1}
                end
                FROM fias_addrobj addr
                WHERE {where}
              UNION ALL
              SELECT addr.aoguid, addr.parentguid, addr.formalname,
                case {case2}
                     else nodes.found
                end
                FROM fias_addrobj addr, nodes
                WHERE addr.parentguid = nodes.aoguid
            )
            SELECT aoguid FROM nodes WHERE array_length(found, 1) = {length}
            )
        '''
        case1 = []
        case2 = []
        where = []

        fields = [self.construct_sql_search(unicode(search_field))
                  for search_field in search_fields]

        for search_term in terms:
            search_term = search_term.upper()
            cond = u' OR '.join([u'%s' % search_field for search_field in fields])
            case1.append((u"WHEN %s THEN ARRAY['{value}']" % cond).format(
                value=search_term))
            case2.append((u"WHEN (%s) AND NOT ('{value}' = ANY(nodes.found)) "
                          u"THEN array_append(nodes.found, '{value}')"
                          % cond).format(value=search_term))
            where.append(cond.format(value=search_term))
        sql = sql.format(length=len(terms),
                   case1=u' '.join(case1),
                   case2=u' '.join(case2),
                   where=u' OR '.join(where),
                   )

        return queryset.extra(where=[sql])

    def construct_sql_search(self, field_name):
        return u"UPPER(addr.%s) like '%%%%{value}%%%%'" % field_name

    def sphinx_filter(self, request, queryset, view):
        from fias.sphinxit import search

        page_size = view.get_paginate_by()
        page_query_param = request.QUERY_PARAMS.get(view.page_kwarg)
        page = page_query_param or 1
        try:
            page = int(page)
            if page <= 0:
                page = 1
        except ValueError:
            page = 1

        term = '*,'.join(self.get_search_terms(request))

        query = search().match(term + '*').options(
            field_weights={'formalname': 100, 'fullname': 80}
        ).limit(0, (page + 1) * page_size)  # запросим на 1 страницу больше

        # установим ограничение по родительскому объекту
        parent_filter_param = request.QUERY_PARAMS.get('parentguid')
        if parent_filter_param:
            query = query.match('@parentguid '+parent_filter_param)

        # установим ограничение по уровням
        level_filter_param = request.QUERY_PARAMS.get('aolevel')
        if level_filter_param:
            query = query.filter(aolevel__in=level_filter_param.split(','))

        #Hack to bypass bug in sphixit. https://github.com/semirook/sphinxit/issues/16
        query._nodes.OrderBy.orderings = [u'item_weight DESC']

        result = query.ask()
        items = result['result']['items']

        aoguids = [item['aoguid'] for item in items]

        if len(aoguids):
            return queryset.filter(aoguid__in=aoguids)
        else:
            return super(AddressScanFilter, self).filter_queryset(request, queryset, view)
