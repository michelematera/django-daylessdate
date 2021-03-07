===================
django-daylessdate
===================

Provides a Django model and form fields for dates that do not include days.

Prerequisites
=============

- Django 3.0+
- Python 3.6+

Installation
============

.. code-block:: console

    pip install django-daylessdate

Usage
=====

The package provide fields ``DaylessDateField``.

Add ``djangodaylessdate`` to INSTALLED_APPS::

    INSTALLED_APPS = (
        ...
        'djangodaylessdate',
        ...
    )


DaylessDateField
-----------------

``DaylessDateField`` stores a date without a day: January 2021, for example.

Its default widget consists of one dropdowns and one input, one for a month and one for the year.


Here's an example ``models.py`` that declares a model with a required dayless date::

    from django.db import models
    from djangodaylessdate.models import DaylessDateField
  
    class MyModel(models.Model):
        month = DaylessDateField()

The values of ``DaylessDateField`` on the model instances can be accessed like so:

>>> a = MyModel.objects.get(id=1)
>>> a
<MyModel: August 2021>
>>> a.month.month
8
>>> a.month.year
2021
>>> print a.month
August 2021

They can also be compared or sorted as would be expected, for example:

>>> m = MyModel.objects.all() 
>>> m
[<MyModel: August 2021>, <MyModel: January 2021>]
>>> m[0].month > m[1].month
True
>>> m.order_by('month')
[<MyModel: January 2021>, <MyModel: August 2021>]


In admin.py::

    from djangodaylessdate.filters import DaylessDateFilter

    @admin.register(MyModel)
    class MyModelAdmin(admin.ModelAdmin):
        list_filter = [('month', DaylessDateFilter)]