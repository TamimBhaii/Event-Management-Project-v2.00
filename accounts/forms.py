from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = (
                'w-full border border-gray-300 rounded px-3 py-2 '
                'focus:outline-none focus:ring focus:ring-indigo-300'
            )


# For Admin (compatibility)
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name", "bio", "date_of_birth", "profile_picture")


#  For User Profile Editing
class ProfileUpdateForm(UserChangeForm):
    password = None  # hide default password field

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "bio", "date_of_birth", "profile_picture")
        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-indigo-300"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-indigo-300"
            }),
            "bio": forms.Textarea(attrs={
                "rows": 3,
                "class": "w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-indigo-300"
            }),
            "date_of_birth": forms.DateInput(attrs={
                "type": "date",
                "class": "w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-indigo-300"
            }),
            "profile_picture": forms.ClearableFileInput(attrs={
                "class": "w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-indigo-300"
            }),
        }


# For Password Change Form (with styling)
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-indigo-300"}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-indigo-300"}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring focus:ring-indigo-300"}))
