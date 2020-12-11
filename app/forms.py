from django.forms import ModelForm, DateInput, CharField, Textarea
from app.models import TODO, Team, Comment
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TODOForm(ModelForm):
    class Meta:
        model = TODO
        fields = ['title', 'status', 'priority', 'expiration_date', 'user']
        widgets = {
            'expiration_date': DateInput(format=('%m/%d/%Y'),
                            attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'})
        }

class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['title']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': Textarea()
        }


class CustomizedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username", "email",)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
