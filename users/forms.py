from django.contrib.auth import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserChangeForm(forms.UserChangeForm):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'type', 'is_active', 'is_staff',
            'is_superuser', 'password'
        )
        exclude = ('username',)


class UserCreationForm(forms.UserCreationForm):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'type', 'is_active', 'is_staff',
            'is_superuser', 'password'
        )
        exclude = ('username',)
