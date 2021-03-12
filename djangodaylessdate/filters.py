from django.contrib import messages
from django.contrib.admin import FieldListFilter
from django.core.exceptions import ValidationError
from django.contrib.admin.options import IncorrectLookupParameters

from .helpers import DaylessDate


class DaylessDateFilter(FieldListFilter):
    template = 'djangodaylessdate/daylessdate_filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = field_path
        self.lookup_kwarg_isnull = '{}__isnull'.format(field_path)
        self.lookup_kwarg_empty = '{}__exact'.format(field_path)
        self.lookup_val = params.get(self.lookup_kwarg)
        self.lookup_val_isnull = params.get(self.lookup_kwarg_isnull)
        self.empty_value_display = model_admin.get_empty_value_display()
        self.include_none = model.objects.filter(**{field_path: None}).exists()
        self.include_empty = model.objects.filter(**{field_path: ''}).exists()
        super().__init__(field, request, params, model, model_admin, field_path)
        if self.lookup_val in params:
            try:
                DaylessDate(*params[self.lookup_val].split('/'))
            except:
                messages.warning(request, 'Invalid data')

    def queryset(self, request, queryset):
        query_params = {k: v for k, v in self.used_parameters.items()}
        if self.lookup_kwarg in self.used_parameters and self.used_parameters[self.lookup_kwarg]:
            try:
                query_params[self.lookup_kwarg] = DaylessDate(*self.used_parameters[self.lookup_kwarg].split('/'))
            except:
                query_params.pop(self.lookup_kwarg)
        try:
            return queryset.filter(**query_params)
        except (ValueError, ValidationError) as e:
            raise IncorrectLookupParameters(e)

    def has_output(self):
        return True

    def expected_parameters(self):
        return [self.lookup_kwarg, self.lookup_kwarg_isnull, self.lookup_kwarg_empty]

    def choices(self, changelist):
        yield {
            'params': changelist.params,
            'value': self.used_parameters.get(self.lookup_kwarg),
            'query_string': changelist.get_query_string(
                {}, [self.lookup_kwarg, self.lookup_kwarg_isnull, self.lookup_kwarg_empty]
            ),
            'lookup_kwarg': self.lookup_kwarg,
            'include_none': self.include_none,
            'include_empty': self.include_empty,
            'lookup_kwarg_empty': self.lookup_kwarg_empty,
            'query_string_empty': changelist.get_query_string(
                {self.lookup_kwarg_empty: ''}, [self.lookup_kwarg_isnull, self.lookup_kwarg]
            ),
            'lookup_kwarg_isnull': self.lookup_kwarg_isnull,
            'query_string_isnull': changelist.get_query_string(
                {self.lookup_kwarg_isnull: 'True'}, [self.lookup_kwarg, self.lookup_kwarg_empty]
            ),
            'display_isnull': self.empty_value_display,
        }
