from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time
from datetime import datetime

from events.factories import EventFactory, AttendanceFactory
from accounts.factories import UserFactory
from accounts.models import User
from events.models import Event, Attendance


class TestListEvent(TestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_pagination(self):
        EventFactory.create_batch(30, user=self.user)
        response = self.client.get(reverse('event:list'))
        self.assertContains(response, "Event 10")
        self.assertContains(response, "page=2")

    @freeze_time("2012-01-01")
    def test_filter(self):
        EventFactory(user=self.user, title="future", date=datetime(2020, 1, 1))
        EventFactory(user=self.user, title="past", date=datetime(2000, 1, 1))
        response = self.client.get(reverse('event:list'))

        self.assertContains(response, "future")
        self.assertNotContains(response, "past")


class TestCreateEvent(TestCase):
    def setUp(self):
        User.objects.create_user(email='test@example.com', password='12345')

    def test_unauth_user(self):
        response = self.client.get(reverse('event:create'))

        self.assertEqual(response.status_code, 302)

    @freeze_time("2012-01-01")
    def test_success_redirect(self):
        self.client.login(email='test@example.com', password='12345')
        response = self.client.post(reverse('event:create'), {
            "title": "Fyre Festival",
            "description": "Private Island festival",
            "date": datetime(2020, 1, 1),
        }, follow=True)
        self.assertContains(response, "Fyre Festival")

    @freeze_time("2012-01-01")
    def test_failure(self):
        self.client.login(email='test@example.com', password='12345')
        response = self.client.post(reverse('event:create'), {
            "title": "",
            "description": "",
            "date": "",
        }, follow=True)
        self.assertContains(response, "This field is required")


class TestUpdateEvent(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='12345'
        )
        self.event = EventFactory(user=user)

    def test_unauth_user(self):
        url = reverse('event:update', kwargs={"pk": self.event.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_not_owner_user(self):
        User.objects.create_user(email='some_other@example.com', password='12345')
        self.client.login(email='some_other@example.com', password='12345')

        url = reverse('event:update', kwargs={"pk": self.event.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

class TestDetailEvent(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='12345'
        )
        self.event = EventFactory(user=user, title="Detail Event")

    def test_event_data(self):
        url = reverse('event:detail', kwargs={"pk": self.event.pk})
        self.client.login(email='test@example.com', password='12345')
        response = self.client.get(url)

        self.assertContains(response, "Detail Event")
        self.assertContains(response, "Lorem ipsum")
        self.assertContains(response, "March 6, 2019")

    def test_attendance_data(self):
        user1 = UserFactory(email='user1@example.com')
        user2 = UserFactory(email='user2@example.com')
        AttendanceFactory(user=user1, event=self.event)
        AttendanceFactory(user=user2, event=self.event)

        url = reverse('event:detail', kwargs={"pk": self.event.pk})
        self.client.login(email='test@example.com', password='12345')
        response = self.client.get(url)
        self.assertContains(response, "user1")
        self.assertContains(response, "user2")

