from django import forms
from .models import ValidLabelPair

class LabelEditForm(forms.ModelForm):
    class Meta:
        model = ValidLabelPair
        fields = ['label', 'label_status']
