from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Comment


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label=("First name"),
    )
    middle_name = forms.CharField(
        label=("Middle name"),
    )
    last_name = forms.CharField(
        label=("Last name"),
    )
    email = forms.EmailField(
        label=("Email"),
        widget=forms.EmailInput,
    )
    birth_date = forms.DateField(
        label=("Birth date"),
        widget=forms.DateInput,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'birth_date')

    def save(self):
        user = super().save(commit=False)
        user.is_reader = True
        user.first_name = self.cleaned_data.get("first_name")
        user.middle_name = self.cleaned_data.get("middle_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.email = self.cleaned_data.get("email")
        user.birth_date = self.cleaned_data.get("birth_date")
        user.save()
        return user


class CommentForm(forms.ModelForm):
    parent = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Comment
        fields = ('text', 'parent', )
