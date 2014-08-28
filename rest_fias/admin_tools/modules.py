# -*- coding: utf-8 -*-
from admin_tools.utils import get_admin_site_name
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from admin_tools.dashboard import modules
from fias.models import Version, Status


class FiasDashboardModule(modules.DashboardModule):
    deletable = False
    title = _(u'Информация о БД ФИАС')
    template = 'admin_tools/fias_info.html'
    table_names = {
        'addrobj': u'Адресные объекты',
        'house': u'Дома',
        'houseint': u'Интервалы домов',
        'normdoc': u'Документы',
        'socrbase': u'Сокращения',
    }

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        ver_info = self.get_version_info()
        self.children.extend([
            {
                'title': _(u'Доступная версия'),
                'value': ver_info.get('last_ver'),
                'date': ver_info.get('last_date'),
            },
            {
                'title': _(u'Текущая версия'),
                'value': ver_info.get('current_state'),
            },
        ])
        self.children.extend([
            {
                'title': item['name'],
                'value': item['ver'],
                'date': item['date'],
            } for item in ver_info['current']
        ])
        self.bottom = []
        self.bottom.append({'url': reverse('%s:update_fias_info' % site_name),
                            'name': u'Проверить доступную версию'})
        self.bottom.append({'url': reverse('%s:update_fias' % site_name),
                            'name': u'Обновить базу ФИАС (долго)'})

    def get_version_info(self):
        result = {}
        try:
            latest_version = Version.objects.latest('dumpdate')
            result['last_ver'] = latest_version.ver
            result['last_date'] = latest_version.dumpdate
        except Version.DoesNotExist:
            pass
        # проверим признак обновления
        try:
            v = Version.objects.get(pk=-1)
            result['current_state'] = u'обновляется с %s' % v.complete_xml_url
        except Version.DoesNotExist:
            result['current_state'] = ''
        result['current'] = []
        for status in Status.objects.all():
            result['current'].append({
                'name': self.table_names.get(status.table, status.table),
                'ver': status.ver_id,
                'date': status.ver.dumpdate,
            })
        return result