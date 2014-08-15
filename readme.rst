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
            "code": ,
            "fullname": ,
            "offname":,
            "aolevel": ,
            "formalname":,
            "shortname":,
            "parentguid": ,
            "aoguid":
          }
      ]
    }


:Примеры:
        
::

        GET /fias/v1/ao/?aolevel=1

        GET /fias/v1/ao/?aolevel=1,4,6

        GET /fias/v1/ao/?aolevel=7&parentguid=63ed1a35-4be6-4564-a1ec-0c51f7383314

        GET /fias/v1/ao/?aolevel=7&parentguid=63ed1a35-4be6-4564-a1ec-0c51f7383314&search=гага

        GET /fias/v1/ao/?aolevel=7&scan=гагарина,байконур



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
      "aoguid":"63ed1a35-4be6-4564-a1ec-0c51f7383314",
      "parentguid":null,
      "aoid":"c5b6f41e-3a25-4056-a7f5-7c7a3e625bdc",
      "previd":null,
      "nextid":null,
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
      "fullname":"Байконур г"
    }


:Примеры:
        
::

        GET /fias/v1/ao/63ed1a35-4be6-4564-a1ec-0c51f7383314/


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
            "houseguid":"4abf7720-fa42-482c-a2ec-cd564d9abc96",
            "houseid":"4abf7720-fa42-482c-a2ec-cd564d9abc96",
            "aoguid":"8bbdbc9c-4435-4c82-8989-0b84d8480866",
            "housenum":"5",
            "buildnum":null,
            "strucnum":null
          },
      ]
    }


:Примеры:
        
::

        GET /fias/v1/ao/8bbdbc9c-4435-4c82-8989-0b84d8480866/houses/

        GET /fias/v1/ao/8bbdbc9c-4435-4c82-8989-0b84d8480866/houses/?search=3


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
      "houseguid": "4abf7720-fa42-482c-a2ec-cd564d9abc96", 
      "houseid": "4abf7720-fa42-482c-a2ec-cd564d9abc96", 
      "aoguid": "8bbdbc9c-4435-4c82-8989-0b84d8480866", 
      "housenum": "5", 
      "eststatus": true, 
      "buildnum": null, 
      "strucnum": null, 
      "strstatus": 0, 
      "statstatus": 26, 
      "counter": 1
    }


:Примеры:
        
::

    GET /fias/v1/ao/8bbdbc9c-4435-4c82-8989-0b84d8480866/houses/4abf7720-fa42-482c-a2ec-cd564d9abc96/