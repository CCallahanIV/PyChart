import factory
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, RequestFactory
from django.test import RequestFactory
from django.urls import reverse_lazy
from pychart_profile.models import PyChartProfile
from pychart_datarender.models import Data, Render
import unittest
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_FILE_PATH = os.path.join(BASE_DIR, 'MEDIA/data/drug.csv')

TEST_HTML_FILE_PATH = os.path.join(BASE_DIR, 'MEDIA/render/TestScatter.html')


class UserFactory(factory.django.DjangoModelFactory):
    """Define a factory for creating user objects."""

    class Meta:
        """Assign a model."""

        model = User

    username = factory.Sequence(lambda n: "Test user {}".format(n))
    email = factory.LazyAttribute(
        lambda x: "{}@foo.com".format(x.username.replace(" ", ""))
    )


class DataFactory(factory.django.DjangoModelFactory):
    """Define a factory for creating Data models."""

    class Meta:
        """Assign a model."""

        model = Data

    title = factory.Sequence(lambda n: "Test Data Object {}".format(n))
    description = "Test Description"
    data = SimpleUploadedFile(
        name='drug.csv',
        content=open(TEST_FILE_PATH, 'rb').read(),
        content_type='text/csv'
    )


class RenderFactory(factory.django.DjangoModelFactory):
    """Define a factory for creating Data models."""

    class Meta:
        """Assign a model."""

        model = Render

    title = factory.Sequence(lambda n: "Test Data Object {}".format(n))
    description = "Test Description"
    render = open(TEST_HTML_FILE_PATH, 'r').read()


class ProfileTestCase(TestCase):
    """The Profile Model test runner."""

    def create_test_user(self):
        """Create a test user."""
        UserFactory.create()

    def test_create_user_creates_profile(self):
        """Test that creating a user creates a profile."""
        user = UserFactory.create()
        self.assertEqual(user, PyChartProfile.objects.all().first().user)

    def test_all_profile_fields(self):
        """Test all profile fields."""
        user = UserFactory.create()
        data_set = DataFactory.build()
        data_set.owner = user.profile
        data_set.save()
        render = RenderFactory.build()
        render.owner = user.profile
        render.save()
        self.assertTrue(len(user.profile.renders.all()) == 1)
        self.assertTrue(len(user.profile.data_sets.all()) == 1)


class ProfileFrontEndTests(TestCase):
    """Test the profile front end."""

    def setUp(self):
        """Set up the tests."""
        self.client = Client()
        self.request = RequestFactory()

    def test_home_view_status_ok(self):
        """Test that the HomeView returns a 200 on GET."""
        from pychart.views import HomeView
        req = self.request.get(reverse_lazy('home'))
        view = HomeView.as_view()
        response = view(req)
        self.assertEqual(response.status_code, 200)

    def test_login_not_logged_in_view_status(self):
        """Test login view not logged in GET returns 200."""
        response = self.client.get(reverse_lazy('login'))
        self.assertEqual(response.status_code, 200)

    def test_registration_not_logged_in_view_status(self):
        """Test registration page not logged in GET returns 200."""
        response = self.client.get(reverse_lazy('registration_register'))
        self.assertEqual(response.status_code, 200)