from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Comment


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label="First name",
    )
    middle_name = forms.CharField(
        label="Middle name",
    )
    last_name = forms.CharField(
        label="Last name",
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput,
    )
    birth_date = forms.DateField(
        label="Birth date",
        widget=forms.DateInput,
    )
    is_subscription = forms.BooleanField(
        label="Send email",
        widget=forms.CheckboxInput,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name',
                  'email', 'birth_date', 'is_subscription')

    def save(self):
        user = super().save(commit=False)
        user.is_reader = True
        user.first_name = self.cleaned_data.get("first_name")
        user.middle_name = self.cleaned_data.get("middle_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.email = self.cleaned_data.get("email")
        user.birth_date = self.cleaned_data.get("birth_date")
        user.is_subscription = self.cleaned_data.get("is_subscription")
        user.save()
        return user


class CommentForm(forms.ModelForm):
    parent = forms.CharField(widget=forms.HiddenInput(
                             attrs={'class': 'parent'}),
                             required=False)
    text = forms.CharField(label="", widget=forms.Textarea(attrs={'rows': '3'}))

    class Meta:
        model = Comment
        fields = ('text',)
