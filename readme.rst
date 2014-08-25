REST-сервис на django-rest-framework для доступа к базе ФИАС
------------------------------------------------------------

Этот сервис - результат объединения разработок:

* django-rest-framework <http://www.django-rest-framework.org/>
* django-fias <https://github.com/Yuego/django-fias>

Формат сервиса
--------------

Список адресных объектов
========================

::

    GET /fias/v1/ao/

:Параметры:

:aolevel:
    Тип: число или список чисел через запятую. Фильтрация по уровню адресного объекта.

:parentguid:
    Тип: GUID. Фильтрация по родительскому адресному объекту.

:codes:
    Тип: строка символов. Фильтрация адресных объектов по коду КЛАДРа. Фильтруются объекты, у которых код начинается на указанную строку символов.

:code:
    Тип: строка символов или список строк через запятую. Фильтрация адресных объектов по коду КЛАДРа. Фильтруются объекты, у которых код совпадает с одной из строк.

:search:
    Тип: строка символов. Поиск адресного объекта по содержанию строки в наименовании.

:scan:
    Тип: строка символов или список строк через запятую. Полнотекстовый поиск адресного объекта по содержанию строк в полном наименовании. В отличие от *search* может использовать sphinx для быстрого поиска.

:view:
    Тип: строка символов. Режим представления результатов. Принимает значения: *simple*.

:page:
    Тип: число. Страница вывода результатов.

:Результат:
    Тип: application/json. Результаты выводятся по страницам размером в 50 записей. Записи представляются объектами в зависимости от значения параметра *view*.

Представление по-умолчанию:

::

    {
      "count": общее количество записей в результате,
      "next": ссылка на следующую страницу результатов или null,
      "previous": ссылка на предыдущую страницу результатов или null,
      "results": список записей [
          {
            "code": код КЛАДРа,
            "fullname": полное наименование вместе с наименованием родительских объектов,
            "offname": официальное наименование,
            "aolevel": уровень объекта,
            "formalname": наименование,
            "shortname": сокращение,
            "postalcode": почтовый индекс,
            "parentguid": идентификатор родительского объекта,
            "aoguid": идентификатор объекта
          }
      ]
    }


Представление *simple*:

::

    {
      "count": общее количество записей в результате,
      "next": ссылка на следующую страницу результатов или null,
      "previous": ссылка на предыдущую страницу результатов или null,
      "results": список записей [
          {
            "code": код КЛАДРа,
            "aolevel": уровень объекта,
            "formalname": наименование,
            "shortname": сокращение,
            "parentguid": идентификатор родительского объекта,
            "aoguid": идентификатор объекта
          }
      ]
    }


:Примеры:
        
::

    GET /fias/v1/ao/?aolevel=1,4,6&view=simple

    {
      "count":197445,
      "next":"http://localhost:8000/fias/v1/ao/?aolevel=1%2C4%2C6&page=2&view=simple",
      "previous":null,
      "results":[
          {
            "aoguid":"63ed1a35-4be6-4564-a1ec-0c51f7383314",
            "parentguid":null,
            "formalname":"Байконур",
            "shortname":"г",
            "aolevel":1,
            "code":"9900000000000"
          },
          {
            "aoguid":"6fdecb78-893a-4e3f-a5ba-aa062459463b",
            "parentguid":null,
            "formalname":"Севастополь",
            "shortname":"г",
            "aolevel":1,
            "code":"9200000000000"
          },
      ...
      ]
    }

::

    GET /fias/v1/ao/?aolevel=7&parentguid=63ed1a35-4be6-4564-a1ec-0c51f7383314

    {
      "count":47,
      "next":null,
      "previous":null,
      "results":[
          {
            "aoguid":"f4fa8b47-77fb-4781-aa03-f0d52ca439bf",
            "parentguid":"63ed1a35-4be6-4564-a1ec-0c51f7383314",
            "formalname":"им Космонавта Г.С.Титова",
            "offname":"им Космонавта Г.С.Титова",
            "shortname":"ул",
            "aolevel":7,
            "code":"99000000000001400",
            "fullname":"Байконур г, ул им Космонавта Г.С.Титова",
            "postalcode":468320
          },
          {
            "aoguid":"aabf3eb1-a5e2-47c9-9095-8e183aaf82ac",
            "parentguid":"63ed1a35-4be6-4564-a1ec-0c51f7383314",
            "formalname":"Ниточкина",
            "offname":"Ниточкина",
            "shortname":"ул",
            "aolevel":7,
            "code":"99000000000002200",
            "fullname":"Байконур г, ул Ниточкина",
            "postalcode":468320
          },
      ...
      ]
    }

::

    GET /fias/v1/ao/?aolevel=7&parentguid=63ed1a35-4be6-4564-a1ec-0c51f7383314&search=гага

    {
      "count":2,
      "next":null,
      "previous":null,
      "results":[
          {
            "aoguid":"8bbdbc9c-4435-4c82-8989-0b84d8480866",
            "parentguid":"63ed1a35-4be6-4564-a1ec-0c51f7383314",
            "formalname":"Гагарина",
            "offname":"Гагарина",
            "shortname":"ул",
            "aolevel":7,
            "code":"99000000000000800",
            "fullname":"Байконур г, ул Гагарина",
            "postalcode":468320
          }
      ]
    }

::

    GET /fias/v1/ao/?aolevel=7&scan=гагарина,байконур

    {
      "count":2,
      "next":null,
      "previous":null,
      "results":[
          {
            "aoguid":"8bbdbc9c-4435-4c82-8989-0b84d8480866",
            "parentguid":"63ed1a35-4be6-4564-a1ec-0c51f7383314",
            "formalname":"Гагарина",
            "offname":"Гагарина",
            "shortname":"ул",
            "aolevel":7,
            "code":"99000000000000800",
            "fullname":"Байконур г, ул Гагарина",
            "postalcode":468320
          },
          {
            "aoguid":"e5fa051f-d46e-4d07-9cfe-ebda2756b76a",
            "parentguid":"7220a42c-e12f-492d-8a1e-9e2af7b65b5f",
            "formalname":"Гагарина",
            "offname":"Гагарина",
            "shortname":"ул",
            "aolevel":7,
            "code":"99000000002000500",
            "fullname":"Байконур г, п Тюра-Там, ул Гагарина",
            "postalcode":468320
          }
      ]
    }

::

    GET /fias/v1/ao/?scan=Алексинский,Авангард,Комсомольская

    {
      "count":1,
      "next":null,
      "previous":null,
      "results":[
          {
            "aoguid":"d65e264b-c7b9-41c6-9cb0-ffb9b8f5375b",
            "parentguid":"144fa92f-399f-4c3b-a94b-191140e58e6c",
            "formalname":"Комсомольская",
            "offname":"Комсомольская",
            "shortname":"ул",
            "aolevel":7,
            "code":"71002000003000100",
            "fullname":"Тульская обл, р-н Алексинский, п Авангард, ул Комсомольская",
            "postalcode":301349
          }
      ]
    }

::

    GET /fias/v1/ao/?codes=71002000003000

    {
      "count":9,
      "next":null,
      "previous":null,
      "results":[
          {
            "aoguid":"ba98cdd2-6df4-4b14-ad9b-a05ec2ff82ae",
            "parentguid":"144fa92f-399f-4c3b-a94b-191140e58e6c",
            "formalname":"Школьная",
            "offname":"Школьная",
            "shortname":"ул",
            "aolevel":7,
            "code":"71002000003000900",
            "fullname":"Тульская обл, р-н Алексинский, п Авангард, ул Школьная",
            "postalcode":301349
          },
          {
            "aoguid":"870f5e9e-446e-4481-9d36-c0ce1b6459c0",
            "parentguid":"144fa92f-399f-4c3b-a94b-191140e58e6c",
            "formalname":"Советская",
            "offname":"Советская",
            "shortname":"ул",
            "aolevel":7,
            "code":"71002000003000800",
            "fullname":"Тульская обл, р-н Алексинский, п Авангард, ул Советская",
            "postalcode":301349
          },
          ...
      ]
    }

    GET /fias/v1/ao/?code=1800000200000,1800000200300&view=simple

    {
      "count":2,
      "next":null,
      "previous":null,
      "results":[
          {
            "aoguid":"e69a280f-9064-490e-bae0-8bd39527872f",
            "parentguid":"52618b9c-bcbb-47e7-8957-95c63f0b17cc",
            "formalname":"Сарапул",
            "shortname":"г",
            "aolevel":4,
            "code":"1800000200000"
          },
          {
            "aoguid":"a79b17aa-372a-4ea7-bc32-623016149529",
            "parentguid":"e69a280f-9064-490e-bae0-8bd39527872f",
            "formalname":"Кирпичный Завод",
            "shortname":"п",
            "aolevel":6,
            "code":"1800000200300"
          }
      ]
    }

Адресный объект
===============
::

    GET /fias/v1/ao/{AOGUID}/

:Параметры:

:AOGUID:
    Тип: GUID. Идентификатор адресного объекта (36 символов)

:view:
    Тип: строка символов. Режим представления результатов. Принимает значения: *withparents*.


----

:Результат:
    Тип: application/json. Запись представляется в зависимости от значения параметра *view*.

Представление по-умолчанию:

::

    {
      "aoguid": идентификатор адресного объекта,
      "parentguid": идентификатор родительского адресного объекта,
      "aoid": идентификатор,
      "previd": ,
      "nextid": ,
      "ifnsfl": код ИФНС,
      "terrifnsfl": ,
      "ifnsul": код ИФНС,
      "terrifnsul":,
      "okato": ОКАТО,
      "oktmo": ОКТМО,
      "postalcode": почтовый индес,
      "formalname": наименование,
      "offname": официальное наименоение,
      "shortname": сокращение,
      "aolevel": уровень объекта,
      "regioncode": код региона,
      "autocode": ,
      "areacode": код района,
      "citycode": код города,
      "ctarcode": код территории,
      "placecode": ,
      "streetcode": код улицы,
      "extrcode": ,
      "sextcode": ,
      "code": код КЛАДРа,
      "plaincode": код КЛАДРа,
      "actstatus": признак актуальности,
      "centstatus": ,
      "operstatus": ,
      "currstatus": ,
      "livestatus": статус,
      "fullname": полное наименование,
      "updatedate": дата обновления,
      "startdate": дата начала действия,
      "enddate": дата окончания действия,
      "normdoc": идентификатор нормативного документа
    }


Представление *withparents*:

::

    {
      "aoguid": идентификатор адресного объекта,
      "parentguid": идентификатор родительского адресного объекта,
      "aoid": идентификатор,
      "previd": ,
      "nextid": ,
      "ifnsfl": код ИФНС,
      "terrifnsfl": ,
      "ifnsul": код ИФНС,
      "terrifnsul":,
      "okato": ОКАТО,
      "oktmo": ОКТМО,
      "postalcode": почтовый индес,
      "formalname": наименование,
      "offname": официальное наименоение,
      "shortname": сокращение,
      "aolevel": уровень объекта,
      "regioncode": код региона,
      "autocode": ,
      "areacode": код района,
      "citycode": код города,
      "ctarcode": код территории,
      "placecode": ,
      "streetcode": код улицы,
      "extrcode": ,
      "sextcode": ,
      "code": код КЛАДРа,
      "plaincode": код КЛАДРа,
      "actstatus": признак актуальности,
      "centstatus": ,
      "operstatus": ,
      "currstatus": ,
      "livestatus": статус,
      "fullname": полное наименование,
      "updatedate": дата обновления,
      "startdate": дата начала действия,
      "enddate": дата окончания действия,
      "normdoc": идентификатор нормативного документа,
      "parent": краткое представление родительского объекта {
            "code": код КЛАДРа,
            "aolevel": уровень объекта,
            "formalname": наименование,
            "shortname": сокращение,
            "parentguid": идентификатор родительского объекта,
            "aoguid": идентификатор объекта,
            "parent": краткое представление родительского объекта
          }
      }
    }


:Примеры:
        
::

    GET /fias/v1/ao/63ed1a35-4be6-4564-a1ec-0c51f7383314/

    {
      "aoguid":"63ed1a35-4be6-4564-a1ec-0c51f7383314",
      "parentguid":null,
      "aoid":"c5b6f41e-3a25-4056-a7f5-7c7a3e625bdc",
      "previd":null,
      "nextid":null,
      "ifnsfl":9900,
      "terrifnsfl":null,
      "ifnsul":9900,
      "terrifnsul":null,
      "okato":55000000000,
      "oktmo":null,
      "postalcode":468320,
      "formalname":"Байконур",
      "offname":"Байконур",
      "shortname":"г",
      "aolevel":1,
      "regioncode":"99",
      "autocode":"0",
      "areacode":"000",
      "citycode":"000",
      "ctarcode":"000",
      "placecode":"000",
      "streetcode":"0000",
      "extrcode":"0000",
      "sextcode":"000",
      "code":"9900000000000",
      "plaincode":"99000000000",
      "actstatus":true,
      "centstatus":0,
      "operstatus":1,
      "currstatus":0,
      "livestatus":true,
      "fullname":"Байконур г",
      "updatedate":"2011-09-13",
      "startdate":"1900-01-01",
      "enddate":"2079-06-06",
      "normdoc":null
    }

::

    GET fias/v1/ao/a79b17aa-372a-4ea7-bc32-623016149529/?view=withparents

    {
      "aoguid":"a79b17aa-372a-4ea7-bc32-623016149529",
      "parentguid":"e69a280f-9064-490e-bae0-8bd39527872f",
      "aoid":"6f79f789-a620-40ca-9b6d-5516cd74e5fc",
      "previd":null,
      "nextid":null,
      "ifnsfl":1838,
      "terrifnsfl":null,
      "ifnsul":1838,
      "terrifnsul":null,
      "okato":94440000000,
      "oktmo":94740000,
      "postalcode":427960,
      "formalname":"Кирпичный Завод",
      "offname":"Кирпичный Завод",
      "shortname":"п",
      "aolevel":6,
      "regioncode":"18",
      "autocode":"0",
      "areacode":"000",
      "citycode":"002",
      "ctarcode":"000",
      "placecode":"003",
      "streetcode":"0000",
      "extrcode":"0000",
      "sextcode":"000",
      "code":"1800000200300",
      "plaincode":"18000002003",
      "actstatus":true,
      "centstatus":0,
      "operstatus":1,
      "currstatus":0,
      "livestatus":true,
      "fullname":"Удмуртская Респ, г Сарапул, п Кирпичный Завод",
      "updatedate":"2011-09-14",
      "startdate":"1900-01-01",
      "enddate":"2079-06-06",
      "normdoc":null,
      "parent":{
            "aoguid":"a79b17aa-372a-4ea7-bc32-623016149529",
            "parentguid":"e69a280f-9064-490e-bae0-8bd39527872f",
            "formalname":"Кирпичный Завод",
            "shortname":"п",
            "aolevel":6,
            "code":"1800000200300",
            "parent":{
                "aoguid":"e69a280f-9064-490e-bae0-8bd39527872f",
                "parentguid":"52618b9c-bcbb-47e7-8957-95c63f0b17cc",
                "formalname":"Сарапул",
                "shortname":"г",
                "aolevel":4,
                "code":"1800000200000",
                "parent":{
                    "aoguid":"52618b9c-bcbb-47e7-8957-95c63f0b17cc",
                    "parentguid":null,
                    "formalname":"Удмуртская",
                    "shortname":"Респ",
                    "aolevel":1,
                    "code":"1800000000000"
                }
            }
      }
    }


Список домов по адресу
======================

::

    GET /fias/v1/ao/{AOGUID}/houses/


:Параметры:

:AOGUID:
    Тип: GUID. Идентификатор адресного объекта (36 символов)

:search:
    Тип: строка символов. Поиск дома по содержанию строки в номере.

:page:
    Тип: число. Страница вывода результатов.
    
----

:Результат:
    Тип: application/json. Результаты выводятся по страницам размером в 50 записей.

::

    { 
      "count": общее количество записей в результате, 
      "next": ссылка на следующую страницу результатов или null, 
      "previous": ссылка на предыдущую страницу результатов или null, 
      "results": список записей [
          {
            "houseguid": идентификатор дома,
            "houseid": ,
            "aoguid": идентификатор адресного объекта,
            "housenum": номер дома,
            "buildnum": номер строения,
            "strucnum": номер корпуса,
            "postalcode": почтовый индекс
          },
      ]
    }


:Примеры:
        
::

    GET /fias/v1/ao/8bbdbc9c-4435-4c82-8989-0b84d8480866/houses/

    {
      "count":2,
      "next":null,
      "previous":null,
      "results":[
          {
            "houseguid":"4abf7720-fa42-482c-a2ec-cd564d9abc96",
            "houseid":"4abf7720-fa42-482c-a2ec-cd564d9abc96",
            "aoguid":"8bbdbc9c-4435-4c82-8989-0b84d8480866",
            "housenum":"5",
            "buildnum":null,
            "strucnum":null,
            "postalcode":468320
          },
          {
            "houseguid":"d3ea59b6-1e06-4855-a9e8-8e88fb92ae85",
            "houseid":"d3ea59b6-1e06-4855-a9e8-8e88fb92ae85",
            "aoguid":"8bbdbc9c-4435-4c82-8989-0b84d8480866",
            "housenum":"3",
            "buildnum":null,
            "strucnum":null,
            "postalcode":468320
          }
      ]
    }

::

    GET /fias/v1/ao/8bbdbc9c-4435-4c82-8989-0b84d8480866/houses/?search=3

    {
      "count":1,
      "next":null,
      "previous":null,
      "results":[
          {
            "houseguid":"d3ea59b6-1e06-4855-a9e8-8e88fb92ae85",
            "houseid":"d3ea59b6-1e06-4855-a9e8-8e88fb92ae85",
            "aoguid":"8bbdbc9c-4435-4c82-8989-0b84d8480866",
            "housenum":"3",
            "buildnum":null,
            "strucnum":null,
            "postalcode":468320
          }
      ]
    }


Информация о доме
=================

::

    GET /fias/v1/ao/{AOGUID}/houses/{GUID}


:Параметры:

:AOGUID:
    Тип: GUID. Идентификатор адресного объекта (36 символов)
:GUID:
    Тип: GUID. Идентификатор дома (36 символов)

----

:Результат:
    Тип: application/json.

::

    {
      "houseguid": идентификатор дома,
      "houseid": ,
      "aoguid": идентификатор адресного объекта,
      "ifnsfl": код ИФНС,
      "terrifnsfl": ,
      "ifnsul": код ИФНС,
      "terrifnsul": ,
      "okato": ОКАТО,
      "oktmo": ОКТМО,
      "postalcode": почтовый индекс,
      "housenum": номер дома,
      "address": полный адрес дома,
      "eststatus": статус,
      "buildnum": номер строения,
      "strucnum": номер корпуса
      "strstatus": статус корпуса,
      "statstatus": статус,
      "counter": количество,
      "updatedate": дата обновления,
      "startdate": дата начала действия,
      "enddate": дата окончания действия,
      "normdoc": идентификатор нормативного документа
    }


:Примеры:
        
::

    GET /fias/v1/ao/8bbdbc9c-4435-4c82-8989-0b84d8480866/houses/4abf7720-fa42-482c-a2ec-cd564d9abc96/

    {
      "houseguid":"4abf7720-fa42-482c-a2ec-cd564d9abc96",
      "houseid":"4abf7720-fa42-482c-a2ec-cd564d9abc96",
      "aoguid":"8bbdbc9c-4435-4c82-8989-0b84d8480866",
      "ifnsfl":9901,
      "terrifnsfl":null,
      "ifnsul":9901,
      "terrifnsul":null,
      "okato":55000000000,
      "oktmo":null,
      "postalcode":468320,
      "housenum":"5",
      "address":"468320, Байконур г, ул Гагарина, д. 5",
      "eststatus":true,
      "buildnum":null,
      "strucnum":null,
      "strstatus":0,
      "statstatus":26,
      "counter":1,
      "updatedate":"2012-03-23",
      "startdate":"2006-09-11",
      "enddate":"2079-06-06",
      "normdoc":"2c198f92-0ac9-4370-9cf5-087aacc8a8dc"
    }



Установка
---------

Установка Sphinx <http://sphinxsearch.com/docs/2.1.9/installation.html>

Первоначальна загрузка данных
=============================

(на основе <https://github.com/Yuego/django-fias>)

В settings.py проекта обязательно должны быть подключены модули 'south', 'fias', 'rest_fias'
(желательно в этом же порядке, чтобы использовалась оптимизированная команда загрузки данных):

::

    INSTALLED_APPS = (
        'south',
        ...
        'fias',
        ...
        'rest_fias',
    )

Также должна быть указана БД (если не указана, то будет использоваться БД с псевдонимом 'fias') и загружаемые таблицы:

::

    FIAS_DATABASE_ALIAS = 'default'
    FIAS_TABLES = ('house',)


Скачать файл полной БД ФИАС в формате XML <http://fias.nalog.ru/Public/DownloadPage.aspx>
(файл будет называться *fias_xml.rar*)

Синхронизировать структуру базы:

::

    python manage.py syncdb
    python manage.py migrate

Запустить загрузку данных:

::

    python manage.py fias --file ./fias_xml.rar --really-replace --force-replace

Будет идти долго - у меня шло около 8 часов (при загрузке таблицы 'house').


Настрока полнотекстового поиска
===============================

(пути указаны для ubuntu/debian)

Отредактировать пример файла настройки demo_service/sphinx.conf или сформировать новый файл:

::

    python manage.py fias_sphinx --path=/var/lib/sphinxsearch/data/ > sphinx.conf

-- path - путь хранения базы sphinx

Скопировать файл sphix.conf в папку sphinx.

::

    cp ./sphinx.conf /etc/sphinxsearch/

Запустить создание индекса:

::

    indexer -c /etc/sphinxsearch/sphinx.conf --all

Запустить sphinx:

::

    /etc/init.d/sphinxsearch start


В settings.py проекта включить поиск 'sphinx':

::

    FIAS_SEARCH_ENGINE = 'sphinx'



Настройка аутентификации OAuth2
-------------------------------

Установить пакет OAuth2

::

    pip install django-oauth2-provider


Настроить приложение (settings.py)

::

    INSTALLED_APPS = (
        ...
        'provider',
        'provider.oauth2',
        ...
    )

    REST_FRAMEWORK = {
        ...
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.OAuth2Authentication',
        ),
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        ),
    }

Добавить обрабатываемые адреса (urls.py)

::

    urlpatterns = patterns('',
        ...
        url(r'^oauth2/', include('provider.oauth2.urls', namespace = 'oauth2')),
        ...
    )


Выполнить миграцию базы

::

    python manage.py syncdb
    python manage.py migrate


Регистрация клиентского приложения
==================================

Заходим в django-admin /admin

В разделе Auth создаем пользователя от имени которого будут выполняться запросы.
(Можно всех клиентов привязать к одному пользователю, они всё-равно будут отличаться номером клиента)

В разделе Oauth2 создаем клиента,
* выбираем пользователя
* указываем Url и Redirect uri приложения
* Client type указываем *Confidencial*
* сохраняем клиента
* Копируем Client id и Client secret и передаем для настройки клиентского приложения


Обращение к сервису из клиентского приложения
=============================================

1. Получение токена

Для получения токена нужно выполнить POST-запрос:

  POST /oauth2/access_token/

:Параметры:

:client_id:
    Тип: строка символов. Идентификатор клиентского приложения

:client_secret:
    Тип: строка символов. Секретный ключ клиентского приложения

:grant_type:
    Тип: строка символов. Тип идентификации клиента. Доступные значения: *password*

:username:
    Тип: строка символов. Имя пользователя, которому выдается токен

:password:
    Тип: строка символов. Пароль пользователя

----

:Результат:
    Тип: application/json.

::

    {
        "access_token": токен для доступа к сервису,
        "token_type": "Bearer",
        "expires_in": время жизни токена в секундах,
        "refresh_token": токен для обновления,
        "scope": "read"
    }


2. Запрос данных

После получения токена его нужно указать в заголовке запроса к сервису:

::
    Authorization: Bearer <токен>
