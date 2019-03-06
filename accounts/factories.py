import factory
from accounts.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = "John"
    last_name = "Doe"
    email = "john@example.com"