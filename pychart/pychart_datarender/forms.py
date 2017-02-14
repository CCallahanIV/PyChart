from django import forms
from pychart_datarender.models import Data, Render


class DataForm(forms.ModelForm):
    """Create a form for adding new dataset."""

    class Meta:
        model = Data
        fields = ['title', 'description', 'data']
