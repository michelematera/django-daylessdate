from django.db import models
from .helpers import DaylessDate
from . import forms


class DaylessDateField(models.Field):
    description = "A date without a day, for use in things like billing"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 6
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        if value and isinstance(value, DaylessDate):
            return ''.join(['{:02d}'.format(x) for x in (value.year, value.month)])

    def get_internal_type(self):
        return 'CharField'

    def to_python(self, value):
        if isinstance(value, DaylessDate) or not value:
            return value
        return DaylessDate(value[-2:], value[:4])

    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': forms.DaylessDateField,
            **kwargs,
        })