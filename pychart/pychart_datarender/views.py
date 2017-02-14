from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, UpdateView
from pychart_datarender.models import Data, Render
from pychart_datarender.forms import DataForm


class GalleryView(TemplateView):
    """View for gallery."""

    pass


class DataDetailView(TemplateView):
    """View for data detail."""

    pass
    # def get_context_data(self, pk):
    #     """Get context for album view."""
    #     data = Data.objects.get(pk=pk)
    #     return {'data': data}



class RenderDetailView(TemplateView):
    """View for data render."""

    pass


class DataLibraryView(TemplateView):
    """View for data library."""

    pass


class EditDataView(UpdateView):
    """View for editing dataset."""

    pass

# Stretch Goal to edit Renders


class EditRenderView(UpdateView):
    """View for editing render."""

    pass


class AddDataView(CreateView):
    """View for creating data."""

    model = Data
    form_class = DataForm
    template_name = 'pychart_datarender/templates/add_data.html'

    def form_valid(self, form):
        data = form.save()
        data.owner = self.request.user.profile
        


class AddRenderView(CreateView):
    """View for creating render."""

    pass

