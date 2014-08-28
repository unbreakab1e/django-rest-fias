# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function
import copy
import os
import sys
from optparse import make_option
import datetime
import StringIO

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connections, router, reset_queries
from django.utils.translation import activate
from django.db.models import sql

from fias.importer.commands import load_complete_xml, load_delta_xml
from fias.management.utils.weights import rewrite_weights
from fias.models import Status, Version, AddrObj
from fias.importer import bulk
from fias.importer.loader import house
from south.creator import changes, actions, freezer
from south.creator.actions import AddIndex, AddUnique
from south.migration import Migrations
from south.orm import FakeORM
from south.v2 import SchemaMigration
from south.db import db
from suds.client import Client


originalBulkCreate = bulk.BulkCreate
originalHouseLoader = house.Loader


# kirov
class CopyInsertBulkCreate(originalBulkCreate):

    def _copy_insert(self):
        cursor = connections[router.db_for_write(self.model)].cursor()
        data = StringIO.StringIO()
        fields = self.model._meta.local_fields
        query = sql.InsertQuery(self.model)
        query.insert_values(fields, self.objects, raw=False)
        compiler = query.get_compiler(using=router.db_for_write(self.model))
        compiler.return_id = False
        fields = compiler.query.fields
        qn = compiler.connection.ops.quote_name
        columns = [qn(f.column) for f in fields]
        len_cols = len(columns)
        len_objs = len(self.objects)
        r = lambda x: x.replace('\\', '\\\\').replace('\t', '') \
            if isinstance(x, basestring) else '\\N' if x is None else x
        body = '\n'.join(['\t'.join(['%s']*len_cols)]*len_objs)
        for sqls, params in compiler.as_sql():
            data.write(body % tuple(map(r, params)))
            data.seek(0)
            cursor.copy_from(data, self.model._meta.db_table, columns=columns)

    def _create(self):
        if connections[router.db_for_write(self.model)].vendor == 'postgresql':
            self._copy_insert()
            self.objects = []
            if settings.DEBUG:
                reset_queries()
        else:
            super(CopyInsertBulkCreate, self)._create()


bulk.BulkCreate = CopyInsertBulkCreate


class SilentHouseLoader(originalHouseLoader):

    def _init(self):
        super(SilentHouseLoader, self)._init()
        self._addrobj_cache = set(AddrObj.objects.values_list('aoguid', flat=True))

    def process_row(self, row):
        if row.tag == 'House':
            end_date = self._str_to_date(row.attrib['ENDDATE'])
            if end_date < self._today:
                #print ('Out of date entry. Skipping...')
                return

            start_date = self._str_to_date(row.attrib['STARTDATE'])
            if start_date > self._today:
                print ('Date in future - skipping...')
                return

            related_attrs = dict()
            # kirov
            if not row.attrib['AOGUID'] in self._addrobj_cache:
                print ('AddrObj with GUID `{0}` not found. Skipping house...'.format(row.attrib['AOGUID']))
                return
            aoguid_id = row.attrib['AOGUID']
            del row.attrib['AOGUID']
            related_attrs['aoguid_id'] = aoguid_id

            # try:
            #     related_attrs['aoguid'] = AddrObj.objects.get(pk=row.attrib['AOGUID'])
            # except AddrObj.DoesNotExist:
            #     print ('AddrObj with GUID `{0}` not found. Skipping house...'.format(row.attrib['AOGUID']))
            #     return

            self._bulk.push(row, related_attrs=related_attrs)


house.Loader = SilentHouseLoader


class Command(BaseCommand):
    help = 'Fill or update FIAS database'
    usage_str = 'Usage: ./manage.py fias [--file <filename>|--remote-file|'\
                '--indexes <remove|restore>]'\
                ' [--force-replace] [--really-replace] [--update [--skip]]'\
                ' [--fill-weights]'

    option_list = BaseCommand.option_list + (
        make_option('--file', action='store', dest='file', default=None,
                    help='Load file into DB'),
        make_option('--remote-file', action='store_true', dest='remote', default=False,
                    help='Download full archive and load it into DB'),
        make_option('--force-replace', action='store_true', dest='force', default=False,
                    help='Force replace database'),
        make_option('--really-replace', action='store_true', dest='really', default=False,
                    help='If data exist in any table, you should confirm their removal and replacement'
                         ', as this may result in the removal of related data from other tables!'),
        make_option('--update', action='store_true', dest='update', default=False,
                    help='Fetch `ver` and load into db'),
        make_option('--fill-weights', action='store_true', dest='weights', default=False,
                    help='Fill default weights'),
        make_option('--skip', action='store_true', dest='skip', default=False,
                    help='Skip the bad delta files when upgrading'),
        # kirov
        make_option('--indexes', action='store', dest='indexes', default=None,
                    type='choice', choices=['remove', 'restore'],
                    help='Remove or restore FIAS table indexes'),
        make_option('--file-version', action='store', dest='version', default=None,
                    help='File version number'),
    )

    def handle(self, *args, **options):
        # создадим или обновить признак обновления
        try:
            v = Version.objects.get(pk=-1)
            v.date = datetime.date.today()
            v.complete_xml_url = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            v.save()
        except Version.DoesNotExist:
            Version.objects.create(
                ver=-1,
                dumpdate=datetime.date.min,
                date=datetime.date.today(),
                complete_xml_url=datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            )
        remote = options.pop('remote')
        force = options.pop('force')
        really = options.pop('really')
        update = options.pop('update')
        skip = options.pop('skip')
        weights = options.pop('weights')
        indexes = options.pop('indexes')  # kirov
        file_version = options.pop('version')  # kirov

        path = options.pop('file') if not remote else None

        if path is None and not remote and not update and not weights and not indexes:  # kirov
            self.error(self.usage_str)

        if (path or remote) and Status.objects.count() > 0 and not really:
            self.error('One of the tables contains data. Truncate all FIAS tables manually '
                       'or enter key --really-replace, to clear the table by means of Django ORM')

        truncate = False
        if remote or not file_version:  # kirov
            print ('Fetch version info...')
            fetch_version_info(update_all=True)
        else:  # kirov
            if not Version.objects.filter(ver=file_version or 0).count():  # kirov
                Version.objects.create(ver=file_version or 0, dumpdate=datetime.date.min)  # kirov

        # Force Russian language for internationalized projects
        if settings.USE_I18N:
            activate('ru')

        if path or remote:
            if force:
                truncate = True
                Status.objects.all().delete()
            print ('Total database updating...')
            load_complete_xml(path=path, truncate=truncate)

        if update:
            print ('Database updating...')
            load_delta_xml(skip=skip)

        if weights:
            print ('Rewriting weights')
            rewrite_weights()

        # kirov
        if indexes == 'remove':
            self.remove_indexes()
        # kirov
        if indexes == 'restore':
            self.restore_indexes()
        print ('Finish')

        # сбросим признак
        Version.objects.filter(ver=-1).delete()

    def error(self, message, code=1):
        print(message)
        sys.exit(code)

    # kirov
    def get_indexes(self):
        # TODO: не удаляются индексы у внешних ключей и добавочные
        # _like-индексы к ним. Например у House
        migration = Migrations('fias', force_creation=True)
        # получим текущее состояние базы
        new_defs = dict(
            (k, v) for k, v in freezer.freeze_apps([migration.app_label()]).items()
            if k.split(".")[0] == migration.app_label()
        )
        # скопируем и удалим все индексы
        old_defs = copy.deepcopy(new_defs)
        for table in old_defs.values():
            for key, value in table.items():
                # удалим 'index_together'
                if key == 'Meta' and 'index_together' in value:
                    del value['index_together']
                if isinstance(value, tuple):
                    # удалим 'unique'
                    if 'unique' in value[2]:
                        value[2]['unique'] = False
                    # удалим 'db_index'
                    if 'db_index' in value[2]:
                        value[2]['db_index'] = False

        class InitialMigration(SchemaMigration):
            def forwards(self, orm):
                pass

            def backwards(self, orm):
                pass

            models = old_defs
            complete_apps = ['fias']

        initial_orm = FakeORM(InitialMigration, "fias")

        # получим все изменения, т.е. список индексов
        change_source = changes.AutoChanges(
            migrations=migration,
            old_defs=old_defs,
            old_orm=initial_orm,
            new_defs=new_defs,
        )

        for action_name, params in change_source.get_changes():
            try:
                action_class = getattr(actions, action_name)
            except AttributeError:
                raise ValueError("Invalid action name from source: %s" % action_name)
            else:
                if issubclass(action_class, AddUnique):
                    yield action_class, params

    #kirov
    def remove_indexes(self):
        db.start_transaction()
        for action_class, index in self.get_indexes():
            if issubclass(action_class, AddIndex):
                # если поле уникальное, то индекс не надо удалять - надо удалять ограничение
                if len(index['fields']) == 1 and index['fields'][0].unique:
                    pass
                else:
                    db.delete_index(index['model']._meta.db_table,
                                    [field.column for field in index['fields']])
                # если поле одно и имеет тип varchar или text
                # то для postgresql должен быть еще один индекс с суффиксом _like
                # http://south.aeracode.org/ticket/1214
                if len(index['fields']) == 1 and db._get_connection().vendor == 'postgresql':
                    db_type = index['fields'][0].db_type(connection=db._get_connection())
                    if (db_type.startswith('varchar') or db_type == 'uuid'):
                        self.delete_index(db, index['model']._meta.db_table,
                                          [field.column for field in index['fields']])

            elif issubclass(action_class, AddUnique):
                db.delete_unique(index['model']._meta.db_table,
                                 [field.column for field in index['fields']])

        db.commit_transaction()

    # kirov
    def restore_indexes(self):
        db.start_transaction()
        for action_class, index in self.get_indexes():
            if issubclass(action_class, AddIndex):
                # если поле уникальное, то индекс не надо - надо создать ограничение
                if len(index['fields']) == 1 and index['fields'][0].unique:
                    pass
                else:
                    db.create_index(index['model']._meta.db_table,
                                    [field.column for field in index['fields']])
                # если поле одно и имеет тип varchar или text
                # то для postgresql должен быть еще один индекс с суффиксом _like
                # http://south.aeracode.org/ticket/1214
                if len(index['fields']) == 1 and db._get_connection().vendor == 'postgresql':
                    db_type = index['fields'][0].db_type(connection=db._get_connection())
                    if (db_type.startswith('varchar') or db_type == 'uuid'):
                        self.create_index(db, index['model']._meta.db_table,
                                          [field.column for field in index['fields']],
                                          unique=not issubclass(action_class, AddIndex))

            elif issubclass(action_class, AddUnique):
                db.create_unique(index['model']._meta.db_table,
                                 [field.column for field in index['fields']])

        db.commit_transaction()

    def create_index(self, db, table_name, column_names, unique=False, db_tablespace=''):
        sql = db.create_index_sql(table_name, column_names, unique, db_tablespace)
        index_name = db.create_index_name(table_name, column_names)
        sql = sql.replace(index_name, index_name + '_like').replace(')', ' varchar_pattern_ops)')
        db.execute(sql)

    def delete_index(self, db, table_name, column_names, db_tablespace=''):
        name = db.create_index_name(table_name, column_names) + '_like'
        sql = db.drop_index_string % {
            "index_name": db.quote_name(name),
            "table_name": db.quote_name(table_name),
        }
        db.execute(sql)


def fetch_version_info(update_all=False):
    # настройки прокси из окружения
    proxy_settings = dict()
    if os.environ.has_key('http_proxy'):
        proxy_settings['http'] = os.environ['http_proxy'].replace('http://', '')
    elif os.environ.has_key('HTTP_PROXY'):
        proxy_settings['http'] = os.environ['HTTP_PROXY'].replace('http://', '')
    client = Client(url="http://fias.nalog.ru/WebServices/Public/DownloadService.asmx?WSDL",
                    proxy=proxy_settings)
    result = client.service.GetAllDownloadFileInfo()

    for item in result.DownloadFileInfo:
        try:
            ver = Version.objects.get(ver=item['VersionId'])
        except Version.DoesNotExist:
            ver = Version(**{
                'ver': item['VersionId'],
                'dumpdate': datetime.datetime.strptime(item['TextVersion'][-10:], "%d.%m.%Y").date(),
            })
        finally:
            if not ver.pk or update_all:
                setattr(ver, 'complete_xml_url', item['FiasCompleteXmlUrl'])
                if hasattr(item, 'FiasDeltaXmlUrl'):
                    setattr(ver, 'delta_xml_url', item['FiasDeltaXmlUrl'])
                else:
                    setattr(ver, 'delta_xml_url', None)
                ver.save()