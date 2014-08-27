# -*- coding: utf-8 -*-
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from rest_fias.management.commands.fias import fetch_version_info


@transaction.commit_on_success
def update_fias(request):

    call_command('fias', update=True, really=True, skip=True)

    return HttpResponse(u'FIAS Updated!')


def update_info(request):

    fetch_version_info(True)

    index_path = reverse('admin:index')
    return HttpResponseRedirect(index_path)