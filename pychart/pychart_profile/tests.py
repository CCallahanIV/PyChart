import factory
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse_lazy
from pychart_profile.models import PyChartProfile
from pychart_datarender.models import Data, Render
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
        data_set.save()
        data_set.owner.add(user.profile)
        render = RenderFactory.build()
        render.owner = user.profile
        render.save()
        self.assertTrue(len(user.profile.renders.all()) == 1)
        self.assertTrue(len(user.profile.data_sets.all()) == 1)

    def test_many_users_make_many_profiles(self):
        """Test that making many users makes many profiles."""
        for i in range(20):
            UserFactory.create()
        self.assertTrue(len(User.objects.all()) == 20)
        self.assertTrue(len(User.objects.all()) == len(PyChartProfile.objects.all()))


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

    def test_login_route_uses_right_template(self):
        """Test that the login view uses expected templates."""
        res = self.client.get(reverse_lazy('login'))
        self.assertTemplateUsed(res, 'registration/login.html')
        self.assertTemplateUsed(res, 'pychart/base.html')

    def test_login_route_redirects(self):
        """Test that logging in redirects to profile page."""
        new_user = UserFactory.create()
        new_user.username = "dave"
        new_user.set_password("tugboats")
        new_user.save()
        res = self.client.post("/login/", {
            "username": new_user.username,
            "password": "tugboats"
        }, follow=True)
        self.assertTrue(res.status_code == 200)
        self.assertTrue(res.redirect_chain[0][0] == "/profile/")

    def test_new_user_can_register(self):
        """Test that a new user can register."""
        res = self.client.post("/accounts/register/", {
            "username": "Dave",
            "email": "dave@dave.com",
            "password1": "tugboats",
            "password2": "tugboats"
        }, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.redirect_chain[0][0] == '/accounts/register/complete/')

    def test_registration_not_logged_in_view_status(self):
        """Test registration page not logged in GET returns 200."""
        response = self.client.get(reverse_lazy('registration_register'))
        self.assertEqual(response.status_code, 200)

    def test_registering_new_user_creates_profile(self):
        """Test that registering a new user creates a new profile."""
        self.client.post("/accounts/register/", {
            "username": "testydave",
            "email": "dave@dave.com",
            "password1": "tugboats",
            "password2": "tugboats"
        }, follow=True)
        user = User.objects.get(username="testydave")
        self.assertTrue(user.username == "testydave")
        self.assertIsInstance(user.profile, PyChartProfile)

    def test_home_page_displays_only_reg_login_links(self):
        """Test that the home page only displays registration and login links, not logged in."""
        res = self.client.get(reverse_lazy('home'))
        html = res.content.decode('utf-8')
        logged_in_links = ["Gallery", "Data Library", "Add Data", "Add a Chart", "Logout"]
        for link in logged_in_links:
            self.assertNotIn(link, html)

    def test_home_page_displays_extra_links_logged_in(self):
        """Test that the home page displays more links when user logged in."""
        user = UserFactory.create()
        self.client.force_login(user)
        res = self.client.get("/")
        html = res.content.decode('utf-8')
        logged_in_links = ["Gallery", "Data Library", "Add Data", "Add a Chart", "Logout"]
        for link in logged_in_links:
            self.assertIn(link, html)

    def test_profile_page_not_logged_in_redirects(self):
        """Test that an anon user cannot access the profile page."""
        res = self.client.get("/profile", follow=True)
        self.assertEqual(res.redirect_chain[1][0], '/login/?next=/profile/')

    def test_logged_in_user_sees_profile_page(self):
        """Test that a logged in user can see the profile page."""
        user = UserFactory.create()
        self.client.force_login(user)
        res = self.client.get("/profile", follow=True)
        self.assertTrue(res.status_code == 200)

    def test_logged_in_user_with_data_has_data_on_profile(self):
        """Test that a logged in user sees their data on profile page."""
        user = UserFactory.create()
        user.username = "joeschmoe"
        user.first_name = "Joe"
        user.last_name = "Schmoe"
        user.email = "joe@schmoe.com"
        user.save()
        self.client.force_login(user)
        res = self.client.get("/profile", follow=True)
        html = res.content.decode('utf-8')
        self.assertIn("joeschmoe", html)
        self.assertIn("Joe", html)
        self.assertIn("Schmoe", html)
        self.assertIn("joe@schmoe.com", html)

    def test_user_can_edit_profile(self):
        """Test that a user can edit their profile."""
        user = UserFactory.create()
        self.client.force_login(user)
        user.username = "TestUser"
        user.first_name = "Davey"
        user.save()
        res1 = self.client.get("/profile", follow=True)
        html1 = res1.content.decode('utf-8')
        self.assertIn("Davey", html1)
        self.client.post("/profile/edit/", {
            "First Name": "Jones",
            "Last Name": "Locker",
            "Email": "deadmen@notales.com"
        }, follow=True)
        res2 = self.client.get("/profile", follow=True)
        html2 = res2.content.decode('utf-8')
        self.assertIn("Jones", html2)
        self.assertNotIn("Davey", html2)
