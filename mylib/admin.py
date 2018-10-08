from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Book, Author, PublishingHouse, Genre, Country,\
    BookAuthor, User, Publisher


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'birth_date', 'middle_name',
                  'is_publisher', 'is_reader', 'is_staff')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_active',
                  'birth_date', 'middle_name',
                  'is_publisher', 'is_reader', 'is_staff'
                  )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class PublisherInline(admin.StackedInline):
    model = Publisher
    can_delete = False
    verbose_name_plural = 'publisher'


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    inlines = (PublisherInline,)

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email',
                    'is_reader', 'is_publisher', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('middle_name', 'birth_date',)}),
        ('Permissions', {'fields': ('is_reader', 'is_publisher', 'is_staff',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email',
                       'password1', 'password2',
                       'is_reader', 'is_publisher', 'is_staff')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1


class BookAdmin(admin.ModelAdmin):
    inlines = (BookAuthorInline,)


#
# class UserAdmin(UserAdmin):
#     inlines = (PublisherInline,)

# class PublisherInline(admin.StackedInline):
#     model = Publisher
#     can_delete = False
#     verbose_name_plural = 'publisher'
#
#
# class CustomUserAdmin(admin.ModelAdmin):
#     inlines = (PublisherInline, )


admin.site.register(User, UserAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(PublishingHouse)
admin.site.register(Genre)
admin.site.register(Country)

