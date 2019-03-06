from django.contrib.auth.forms import UserCreationForm
from accounts.models import User

class CustomUserCreationForm(UserCreationForm):
    """ overriding UserCreationForm to support email instead of username """
    class Meta:
        model = User
        fields = ("email",)
