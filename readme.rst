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

:search:
    Тип: строка символов. Поиск адресного объекта по содержанию строки в наименовании.

:scan:
    Тип: строка символов или список строк через запятую. Полнотекстовый поиск адресного объекта по содержанию строк в наименовании. В отличие от *search* может использовать sphinx для быстрого поиска.

:page:
    Тип: число. Страница вывода результатов.  

:Результат:
    Тип: application/json. Результаты выводятся по страницам размером в 50 записей.

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


:Примеры:
        
::

    GET /fias/v1/ao/?aolevel=1,4,6

    {
      "count":197445,
      "next":"http://localhost:8000/fias/v1/ao/?aolevel=1%2C4%2C6&page=2",
      "previous":null,
      "results":[
          {
            "aoguid":"63ed1a35-4be6-4564-a1ec-0c51f7383314",
            "parentguid":null,
            "formalname":"Байконур",
            "offname":"Байконур",
            "shortname":"г",
            "aolevel":1,
            "code":"9900000000000",
            "fullname":"Байконур г",
            "postalcode":468320
          },
          {
            "aoguid":"6fdecb78-893a-4e3f-a5ba-aa062459463b",
            "parentguid":null,
            "formalname":"Севастополь",
            "offname":"Севастополь",
            "shortname":"г",
            "aolevel":1,
            "code":"9200000000000",
            "fullname":"Севастополь г",
            "postalcode":null
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

Адресный объект
===============
::

    GET /fias/v1/ao/{AOGUID}/

:Параметры:

:AOGUID:
    Тип: GUID. Идентификатор адресного объекта (36 символов)

----

:Результат:
    Тип: application/json.

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
            "strucnum": номер корпуса
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
            "strucnum":null
          },
          {
            "houseguid":"d3ea59b6-1e06-4855-a9e8-8e88fb92ae85",
            "houseid":"d3ea59b6-1e06-4855-a9e8-8e88fb92ae85",
            "aoguid":"8bbdbc9c-4435-4c82-8989-0b84d8480866",
            "housenum":"3",
            "buildnum":null,
            "strucnum":null
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
            "strucnum":null
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
      "address":"468320, Байконур г, ул Гагарина, д 5",
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