from django.contrib import messages
from django.contrib.admin import FieldListFilter
from django.core.exceptions import ValidationError
from django.contrib.admin.options import IncorrectLookupParameters

from .helpers import DaylessDate

class DaylessDateFilter(FieldListFilter):
    parameter_name = None
    template = 'djangodaylessdate/daylessdate_filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        if self.parameter_name is None:
            self.parameter_name = self.field.name

        if self.parameter_name in params:
            value = params.pop(self.parameter_name)
            try:
                DaylessDate(*value.split('/'))
                self.used_parameters[self.parameter_name] = value
            except:
                messages.warning(request, 'Invalid data')

    def queryset(self, request, queryset):
        query_params = {k: v for k, v in self.used_parameters.items() if k != self.parameter_name}
        if self.parameter_name in self.used_parameters:
            try:
                query_params[self.parameter_name] = DaylessDate(*self.used_parameters[self.parameter_name].split('/'))
            except:
                pass
        try:
            return queryset.filter(**query_params)
        except (ValueError, ValidationError) as e:
            raise IncorrectLookupParameters(e)

    def has_output(self):
        return True

    def expected_parameters(self):
        return [self.parameter_name]

    def choices(self, changelist):
        yield {
            'get_query': changelist.params,
            'current_value': self.used_parameters.get(self.parameter_name),
            'query_string': changelist.get_query_string({}, [self.parameter_name]),
            'parameter_name': self.parameter_name
        }
