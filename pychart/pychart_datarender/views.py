from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, UpdateView


class GalleryView(TemplateView):
    """View for gallery."""

    pass


class DataDetailView(TemplateView):
    """View for data detail."""

    pass


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

    pass


class AddRenderView(CreateView):
    """View for creating render."""

    pass

