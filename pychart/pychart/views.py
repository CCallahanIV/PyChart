"""This is the pychart views file."""
from django.views.generic import TemplateView
from pychart_datarender.models import Render


class HomeView(TemplateView):
    """Class based view for Home Page."""

    template_name = "pychart/home.html"

    def get_context_data(self):
        """Filter db for a random render for home page."""
        import random
        all_renders = Render.objects.all()

        try:
            random_render = random.choice(all_renders)
        except IndexError:
            random_render = None

        return {'chart': random_render}
