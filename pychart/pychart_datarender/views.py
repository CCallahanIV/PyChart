"""Views for pychart datarender app."""
# from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView
from pychart_datarender.models import Data, Render


class GalleryView(TemplateView):
    """View for gallery."""

    template_name = 'pychart_datarender/gallery.html'

    def get_context_data(self):
        """Show a users data and renders."""
        the_user = self.request.user
        user_data = Data.objects.filter(owner=the_user.profile)
        user_renders = Render.objects.filter(owner=the_user.profile)
        context = {'data': user_data, 'renders': user_renders}
        return context


class DataDetailView(TemplateView):
    """View for data detail."""

    pass


class RenderDetailView(DetailView):
    """View for data render."""

    template_name = "pychart_datarender/render_detail.html"
    model = Render

    def get_context_data(self, **kwargs):
        """Get context class method."""
        render = Render.objects.get(id=self.kwargs.get("pk"))
        context = {"render": render}
        return context


class DataLibraryView(TemplateView):
    """View for data library."""

    template_name = 'pychart_datarender/library.html'
    model = Data

    def get_queryset(self):
        """Get data objects."""
        return Data.objects.all()


class EditDataView(UpdateView):
    """View for editing dataset."""

    pass

# Stretch Goal to edit Renders


class EditRenderView(UpdateView):
    """View for editing render."""

    pass


class AddDataView(CreateView):
    """View for creating data."""

    pass


class AddRenderView(CreateView):
    """View for creating render."""

    pass
