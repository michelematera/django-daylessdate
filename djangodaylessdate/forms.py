from django import forms
from django.forms.widgets import MultiWidget
from django.core.validators import ValidationError
from django.forms.widgets import Select, NumberInput
from django.utils.dates import MONTHS

from .helpers import DaylessDate

MONTH_CHOICES = tuple([('', '---------')]) + tuple([(k, v) for k, v in MONTHS.items()])


class DaylessDateSelect(MultiWidget):
    def __init__(self, *args, **kwargs):
        widgets = (
            Select(choices=MONTH_CHOICES),
            NumberInput()
        )
        super().__init__(widgets=widgets, *args, **kwargs)

    def decompress(self, value):
        if not value:
            return [None, None]
        return [value.month, value.year]


class DaylessDateField(forms.Field):
    widget = DaylessDateSelect

    def __init__(self, *, empty_value='', **kwargs):
        self.empty_value = empty_value
        super().__init__(**kwargs)

    def clean(self, value):
        if all([x in self.empty_values for x in value]):
            return self.empty_value
        try:
            value = DaylessDate(*value)
        except:
            raise ValidationError('Invalid date.')
        return value