"""
 --- Unfinished ---

Provide a ModelMultipleChoiceField that is able to take an empty list of choices
and be filled with choices dynamically on the client side by ajax calls. This
creates a multi-select box the user can type in strings, get a list of matching
options presented and selects one. The result is a list of selected options that
are send back on form-submit as a ModelMultipleChoiceField with the difference
that the choices list is not static.

Use in form definitions:

    stones = DynamicModelMultipleChoiceField(queryset=Stone.objects.none(),
                                             queryset2=Stone.objects.all())

"""

from django.core.exceptions import ValidationError
from django.forms import ModelMultipleChoiceField


class DynamicModelMultipleChoiceField(ModelMultipleChoiceField):
    def __init__(self, queryset, queryset2, *args, **kwargs):
        self.queryset2 = queryset2
        super(DynamicModelMultipleChoiceField, self).__init__(queryset,
                                                              *args, **kwargs)

    def validate(self, value):
        """
        Override and do NOT verify that value is part of choices list.
        """
        if self.required and not value:
            raise ValidationError(self.error_messages['required'],
                                  code='required')
        # Validate that each value in the value list is in self.choices.
        for val in value:
           if not self.valid_value(val):
               raise ValidationError(
                   self.error_messages['invalid_choice'],
                   code='invalid_choice',
                   params={'value': val},
               )

    def _check_values(self, value):
        """
        Given a list of possible PK values, returns a QuerySet of the
        corresponding objects. Raises a ValidationError if a given value is
        invalid (not a valid PK, not in the queryset, etc.)
        """
        key = self.to_field_name or 'pk'
        # deduplicate given values to avoid creating many querysets or
        # requiring the database backend deduplicate efficiently.
        try:
            value = frozenset(value)
        except TypeError:
            # list of lists isn't hashable, for example
            raise ValidationError(
                self.error_messages['list'],
                code='list',
            )
        for pk in value:
            try:
                self.queryset2.filter(**{key: pk})
            except (ValueError, TypeError):
                raise ValidationError(
                    self.error_messages['invalid_pk_value'],
                    code='invalid_pk_value',
                    params={'pk': pk},
                )
        qs = self.queryset2.filter(**{'%s__in' % key: value})
        pks = set(force_text(getattr(o, key)) for o in qs)
        for val in value:
            if force_text(val) not in pks:
                raise ValidationError(
                    self.error_messages['invalid_choice'],
                    code='invalid_choice',
                    params={'value': val},
                )
        return qs
