import factory
from datetime import datetime
from events.models import Event, Attendance
from accounts.factories import UserFactory

class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    title = factory.Sequence(lambda n: "Event {}".format(n + 1))
    description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    date = datetime(2019, 3, 6, 20, 00)
    user = factory.SubFactory(UserFactory)

class AttendanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Attendance

    event = factory.SubFactory(EventFactory)
    user = factory.SubFactory(UserFactory)