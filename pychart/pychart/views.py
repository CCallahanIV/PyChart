"""This is the pychart views file."""
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Class for HomeView."""

    template_name = "pychart/home.html"
