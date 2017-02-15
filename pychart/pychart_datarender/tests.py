"""Tests for pychart_datarender app."""
import factory
from django.test import TestCase
from django.contrib.auth.models import User
from pychart_profile.models import PyChartProfile
from pychart_datarender.models import Data, Render
from django.test import Client, RequestFactory
from django.urls import reverse_lazy
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_HTML_FILE_PATH = os.path.join(BASE_DIR, 'MEDIA/render/TestScatter.html')

class UserFactory(factory.django.DjangoModelFactory):
    """Generate test users."""

    class Meta:
        model = User

    username = factory.Sequence(lambda n: "User {}".format(n))
    email = factory.LazyAttribute(
        lambda x: "{}@thechart.com".format(x.username.replace(" ", "")))


class ProfileFactory(factory.django.DjangoModelFactory):
    """Generate test users."""

    class Meta:
        """Set up meta class for PyChartProfile model."""

        model = PyChartProfile

    user = factory.SubFactory(UserFactory)


class DataFactory(factory.django.DjangoModelFactory):
    """Generate test datasets."""

    class Meta:
        """Set up meta class for Data model."""

        model = Data

    title = factory.Sequence(lambda n: "Data {}".format(n))
    owner = factory.SubFactory(ProfileFactory)


class RenderFactory(factory.django.DjangoModelFactory):
    """Generate test datasets."""

    class Meta:
        """Set up meta class for Render model."""
        model = Render

    title = factory.Sequence(lambda n: "Render {}".format(n))
    render = open(TEST_HTML_FILE_PATH, 'r').read()



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
            # self.datasets[i].renders.add(self.renders[i])
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

    # def test_owner_now_has_no_datasets(self):
    #     """Test that owner now has no datasets."""
    #     data = Data.objects.first()
    #     data_owner = data.owner
    #     new_owner = User.objects.all()[3].profile
    #     data.owner = new_owner
    #     new_owner.save()
    #     data.save()
    #     self.assertTrue(len(data_owner.data_sets.all()) == 0)

    # def test_render_has_dataset(self):
    #     """Test that render has a dataset."""
    #     render = Render.objects.first()
    #     self.assertTrue(len(render.data_sets.all()) == 1)

    def test_string_rep_data_is_title(self):
        """Test that a string representation of data is the title."""
        data = Data.objects.first()
        self.assertTrue(str(data) == data.title)

    def test_string_rep_render_is_title(self):
        """Test that a string representation of render is the title."""
        render = Render.objects.first()
        self.assertTrue(str(render) == render.title)

    def test_render_exists(self):
        """Test existance of a render."""
        this_render = self.renders[0]
        this_render.save()
        self.assertTrue(self.renders[0])

    def test_render_has_a_title(self):
        """Test render has a title."""
        this_render = self.renders[0]
        this_render.title = "My Render"
        this_render.save()
        self.assertTrue(self.renders[0].title)

    def test_render_has_a_title_of_my_render(self):
        """Test render has a title."""
        this_render = self.renders[0]
        this_render.title = "My Render"
        this_render.save()
        self.assertTrue(self.renders[0].title == "My Render")

    def test_render_has_an_owner(self):
        """Test render is tied to a user."""
        this_user = self.users[0]
        this_user.username = "User 1"
        this_user.save()
        this_render = self.renders[0]
        this_render.owner = this_user.profile
        this_render.save()
        self.assertTrue(self.renders[0].owner.user.username == "User 1")

    def test_render_is_type_scatter(self):
        """Test render is a scatter type."""
        this_render = self.renders[0]
        this_render.render_type = "Scatter"
        this_render.save()
        self.assertTrue(self.renders[0].render_type == "Scatter")

    def test_render_is_bar_graph(self):
        """Test render is a bar graph type."""
        this_render = self.renders[0]
        this_render.render_type = "Bar"
        this_render.save()
        self.assertTrue(self.renders[0].render_type == "Bar")

    def test_render_is_a_historgram(self):
        """Test photo has their published setting as Public."""
        this_render = self.renders[0]
        this_render.render_type = "Histogram"
        this_render.save()
        self.assertTrue(self.renders[0].render_type == "Histogram")

    def render_has_a_description(self):
        """Test render has a description."""
        this_render = self.renders[0]
        this_render.description == "My render description"
        this_render.save()
        self.assertTrue(self.renders[0].description == "My render description")


class FrontEndTests(TestCase):
    """Adding functional tests."""

    def setUp(self):
        """Set up Front End Tests."""
        self.client = Client()
        self.request = RequestFactory
        self.users = [UserFactory.create() for i in range(10)]
        self.datasets = [DataFactory.build() for i in range(10)]
        self.renders = [RenderFactory.build() for i in range(10)]
        for i in range(10):
            self.datasets[i].owner = self.users[i].profile
            self.datasets[i].save()
        for i in range(10):
            self.renders[i].save()
            # self.datasets[i].renders.add(self.renders[i])
            self.datasets[i].save()

    def test_data_detail_returns_200(self):
        """Test working data detail page."""
        data = Data.objects.first()
        response = self.client.get(reverse_lazy('data_detail',
                                                kwargs={'pk': data.id}))
        self.assertTrue(response.status_code == 200)

    def test_data_detail_returns_description(self):
        """Test working data detail page."""
        data = Data.objects.first()
        response = self.client.get(reverse_lazy('data_detail',
                                                kwargs={'pk': data.id}))
        self.assertTrue(str(data.description) in str(response.content))

    def test_add_data_returns_200(self):
        """Test working add data page."""
        response = self.client.get(reverse_lazy('data_add'))
        self.assertTrue(response.status_code == 200)

    def user_login(self):
        """New User login."""
        new_user = UserFactory.create()
        new_user.username = 'chartpy'
        new_user.set_password('wordpass')
        new_user.save()
        return new_user

    def test_gallery_route_is_status_ok(self):
        """Funcional test for gallery."""
        new_user = self.user_login()
        self.client.login(username=new_user.username, password='wordpass')
        response = self.client.get(reverse_lazy("gallery"))
        self.assertTrue(response.status_code == 200)

    def test_logged_in_user_sees_add_data_and_chart(self):
        """A logged in user can see correct nav."""
        user = self.user_login()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy("gallery"))
        self.assertTrue("Add Data" and "Add a Chart" in str(response.content))

    def test_logged_in_user_can_get_to_data_library(self):
        """A logged in user can get to the data library page."""
        user = self.user_login()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy("data_library_view"))
        self.assertTrue(response.status_code == 200)

    def test_logged_in_user_sees_data_png_on_filled_library_page(self):
        """A logged in user sees data png on library page."""
        this_user = self.users[0]
        this_user.save()
        self.client.force_login(this_user)
        response = self.client.get(reverse_lazy("data_library_view"))
        self.assertTrue("data.png" in str(response.content))

    def test_logged_in_user_can_get_to_render_detail_page(self):
        """A logged in user can get to the render detail page."""
        user = self.user_login()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy("data_library_view"))
        self.assertTrue(response.status_code == 200)
