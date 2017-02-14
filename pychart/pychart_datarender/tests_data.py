import factory
from django.test import TestCase
from django.contrib.auth.models import User
from pychart_profile.models import PyChartProfile
from pychart_datarender.models import Data, Render
from django.test import Client, RequestFactory


class UserFactory(factory.django.DjangoModelFactory):
    """Generate test users."""

    class Meta:
        model = User

    username = factory.Sequence(lambda n: "User {}".format(n))
    email = factory.LazyAttribute(
        lambda x: "{}@imager.com".format(x.username.replace(" ", "")))


class ProfileFactory(factory.django.DjangoModelFactory):
    """Generate test users."""

    class Meta:
        model = PyChartProfile

    user = factory.SubFactory(UserFactory)


class DataFactory(factory.django.DjangoModelFactory):
    """Generate test datasets."""

    class Meta:
        model = Data

    title = factory.Sequence(lambda n: "Data {}".format(n))
    owner = factory.SubFactory(ProfileFactory)


class RenderFactory(factory.django.DjangoModelFactory):
    """Generate test datasets."""

    class Meta:
        model = Render

    title = factory.Sequence(lambda n: "Render {}".format(n))
    #owner = factory.SubFactory(ProfileFactory)



class TestData(TestCase):
    """Tests for the data model."""

    def setUp(self):
        """User setup for tests."""
        self.users = [UserFactory.create() for i in range(10)]
        self.datasets = [DataFactory.build() for i in range(10)]
        self.renders = [RenderFactory.build() for i in range(10)]
        for i in range(10):
            self.datasets[i].owner = self.users[i].profile
            self.datasets[i].save()
        for i in range(10):
            self.renders[i].save()
            self.datasets[i].renders.add(self.renders[i])
            self.datasets[i].save()

    def test_data_title_change(self):
        """Test that changing dataset title changes."""
        data = Data.objects.first()
        data.title = 'newtitle'
        data.save()
        self.assertTrue(data.title == 'newtitle')

    def test_owner_has_correct_data(self):
        """Test that the owner has correct data."""
        data = Data.objects.first()
        owner = data.owner
        owner_datasets = owner.data_sets
        self.assertTrue(data == owner_datasets.all()[0])

    def test_owner_can_have_multiple_datasets(self):
        """Test that a profile can have multiple datasets."""
        new_user = UserFactory.create()
        data1 = DataFactory.build()
        data2 = DataFactory.build()
        data1.owner = new_user.profile
        data2.owner = new_user.profile
        data1.save()
        data2.save()
        self.assertTrue(len(new_user.profile.data_sets.all()) == 2)

    def test_owner_now_has_no_datasets(self):
        """Test that owner now has no datasets."""
        data = Data.objects.first()
        data_owner = data.owner
        new_owner = User.objects.all()[3].profile
        data.owner = new_owner
        new_owner.save()
        data.save()
        self.assertTrue(len(data_owner.data_sets.all()) == 0)

    def test_render_has_dataset(self):
        """Test that render has a dataset."""
        render = Render.objects.first()
        self.assertTrue(len(render.data_sets.all()) == 1)


