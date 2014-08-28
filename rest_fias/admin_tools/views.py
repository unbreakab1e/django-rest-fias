# -*- coding: utf-8 -*-
import threading
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from fias.models import Version
from rest_fias.management.commands.fias import fetch_version_info


@transaction.commit_on_success
def update_fias(request):
    try:
        v = Version.objects.get(pk=-1)
        return HttpResponse(u'Update process already started %s' % v.complete_xml_url)
    except Version.DoesNotExist:
        # нет такой записи - отлично, значит обновления нет
        t = threading.Thread(target=call_command,
                             args=('fias', ),
                             kwargs=dict(update=True, really=True, skip=True))
        t.setDaemon(True)
        t.start()

        return HttpResponse(u'FIAS update started')


def update_info(request):

    fetch_version_info(True)

    index_path = reverse('admin:index')
    return HttpResponseRedirect(index_path)