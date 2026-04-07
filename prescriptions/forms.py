from django import forms

from prescriptions.models import Prescription


class PrescriptionUploadForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ('image',)
