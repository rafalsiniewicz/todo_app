from django.forms import ModelForm, DateInput
from app.models import TODO

class TODOForm(ModelForm):
    class Meta:
        model = TODO
        fields = ['title', 'status', 'priority', 'expiration_date']
        widgets = {
            'expiration_date': DateInput(format=('%m/%d/%Y'),
                            attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'})
        }
