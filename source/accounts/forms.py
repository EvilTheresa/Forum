from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import EmailField


class MyUserCreationForm(UserCreationForm):
    email = EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        if not first_name and not last_name:
            raise ValidationError('At least one of the fields (first_name, last_name) must be filled.')
        return cleaned_data
