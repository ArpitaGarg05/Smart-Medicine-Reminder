from django import forms
from django.forms import formset_factory

from medicines.models import Medicine

FREQUENCY_CHOICES = ((1, '1 time/day'), (2, '2 times/day'), (3, '3 times/day'), (4, '4 times/day'))


class MedicineConfirmForm(forms.Form):
    name = forms.CharField(max_length=255)
    dosage = forms.CharField(max_length=100, required=False)
    frequency_per_day = forms.ChoiceField(choices=FREQUENCY_CHOICES)
    timing = forms.CharField(max_length=100, required=False)
    total_quantity = forms.IntegerField(min_value=1, initial=10)
    delete = forms.BooleanField(required=False)


class MedicineEditForm(forms.ModelForm):
    frequency_per_day = forms.ChoiceField(choices=FREQUENCY_CHOICES)

    class Meta:
        model = Medicine
        fields = ('name', 'dosage', 'frequency_type', 'day_of_week', 'total_quantity', 'remaining_quantity')


MedicineConfirmFormSet = formset_factory(MedicineConfirmForm, extra=1)
