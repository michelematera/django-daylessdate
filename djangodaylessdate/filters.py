from django.contrib import messages
from django.contrib.admin import FieldListFilter
from django.core.exceptions import ValidationError
from django.contrib.admin.options import IncorrectLookupParameters

from .helpers import DaylessDate

class DaylessDateFilter(FieldListFilter):
    template = 'djangodaylessdate/daylessdate_filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        if self.field_path in params:
            value = params.pop(self.field_path)
            try:
                DaylessDate(*value.split('/'))
                self.used_parameters[self.field_path] = value
            except:
                messages.warning(request, 'Invalid data')

    def queryset(self, request, queryset):
        query_params = {k: v for k, v in self.used_parameters.items() if k != self.field_path}
        if self.field_path in self.used_parameters:
            try:
                query_params[self.field_path] = DaylessDate(*self.used_parameters[self.field_path].split('/'))
            except:
                pass
        try:
            return queryset.filter(**query_params)
        except (ValueError, ValidationError) as e:
            raise IncorrectLookupParameters(e)

    def has_output(self):
        return True

    def expected_parameters(self):
        return [self.field_path]

    def choices(self, changelist):
        yield {
            'get_query': changelist.params,
            'current_value': self.used_parameters.get(self.field_path),
            'query_string': changelist.get_query_string({}, [self.field_path]),
            'field_path': self.field_path
        }