"""Tests for Render class within pychart_datarender app."""
from django.test import TestCase
from django.contrib.auth.models import User
import factory
import os
# from django.test import Client, RequestFactory
# from django.urls import reverse_lazy
# from pychart_profile import PyChartProfile
from pychart_datarender.models import Render

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_HTML_FILE_PATH = os.path.join(BASE_DIR, 'MEDIA/render/TestScatter.html')

class UserFactory(factory.django.DjangoModelFactory):
    """Setting up users for tests."""

    class Meta:
        """Set up model."""

        model = User

    username = factory.Sequence(lambda n: "Charter {}".format(n))
    email = factory.LazyAttribute(
        lambda x: "{}@thechart.com".format(x.username.replace(" ", ""))
    )


class RenderFactory(factory.django.DjangoModelFactory):
    """Create test instance of Render Class."""

    class Meta:
        """Invoke photo instance using Render model class."""

        model = Render

    title = factory.Sequence(lambda n: "Render{}".format(n))
    render = open(TEST_HTML_FILE_PATH, 'r').read()


class UserTestCase(TestCase):
    """The User Model test class."""

    def setUp(self):
        """The setup and buildout for renders."""
        self.users = [UserFactory.create() for i in range(20)]
        self.renders = [RenderFactory.build() for i in range(20)]
        for i in range(20):
            self.renders[i].owner = self.users[i].profile
            self.renders[i].save()
            self.users[i].save

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
