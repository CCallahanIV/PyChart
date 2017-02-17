from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from pychart_profile.models import PyChartProfile
from pychart_profile.forms import UserProfileForm


class ProfileView(LoginRequiredMixin, DetailView):
    """Display user's profile."""

    template_name = "pychart_profile/profile.html"
    model = PyChartProfile
    login_url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        """Get object from request rather than pk or slug."""
        user = request.user
        return self.render_to_response({'user': user})


class UserProfileView(DetailView):
    """Display any user's profile."""

    template_name = "pychart_profile/user_profile.html"
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "user"


class EditProfileView(LoginRequiredMixin, UpdateView):
    """Allow user to edit own profile details."""

    login_url = reverse_lazy("login")
    template_name = "pychart_profile/edit_profile.html"
    model = PyChartProfile
    form_class = UserProfileForm

    def get_object(self):
        """Modify get_object to return this user."""
        return PyChartProfile.objects.all().get(user=self.request.user)

    def form_valid(self, form):
        """Save object after post."""
        self.object = form.save()
        self.object.user.first_name = form.cleaned_data['First Name']
        self.object.user.last_name = form.cleaned_data['Last Name']
        self.object.user.email = form.cleaned_data['Email']
        self.object.user.save()
        self.object.save()
        return redirect("/profile")
