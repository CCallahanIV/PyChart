"""Views for pychart datarender app."""
# from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DetailView
from pychart_datarender.models import Data, Render
from pychart_datarender.forms import DataForm, EditDataForm
from django.utils import timezone
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class GalleryView(LoginRequiredMixin, TemplateView):
    """View for gallery."""

    template_name = 'pychart_datarender/gallery.html'
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("gallery")
    login_url = reverse_lazy("login")

    def get_context_data(self):
        """Show a users data and renders."""
        the_user = self.request.user
        user_data = Data.objects.filter(owner=the_user.profile)
        user_renders = Render.objects.filter(owner=the_user.profile)
        context = {'data': user_data, 'renders': user_renders}
        return context


class DataDetailView(TemplateView):
    """View for data detail."""

    template_name = 'pychart_datarender/data_id.html'

    def get_context_data(self, pk):
        """Get context for album view."""
        data = Data.objects.get(pk=pk)
        return {'data': data}


class RenderDetailView(DetailView):
    """View for data render."""

    template_name = "pychart_datarender/render_detail.html"
    model = Render

    def get_context_data(self, **kwargs):
        """Get context class method."""
        render = Render.objects.get(id=self.kwargs.get("pk"))
        context = {"render": render}
        return context


class DataLibraryView(LoginRequiredMixin, ListView):
    """View for data library."""

    template_name = 'pychart_datarender/library.html'
    model = Data
    context_object_name = 'data'
    success_url = reverse_lazy("data_library_view")
    login_url = reverse_lazy("login")

    def get_queryset(self):
        """Get data objects."""
        return Data.objects.all()


class EditDataView(UpdateView):
    """View for editing dataset."""

    login_required = True
    template_name = 'pychart_datarender/edit_data.html'
    success_url = reverse_lazy('home')
    form_class = EditDataForm
    model = Data




# Stretch Goal to edit Renders


class EditRenderView(UpdateView):
    """View for editing render."""

    pass


class AddDataView(CreateView):
    """View for creating data."""

    model = Data
    form_class = DataForm
    template_name = 'pychart_datarender/add_data.html'

    def form_valid(self, form):
        data = form.save()
        data.owner = self.request.user.profile
        data.date_uploaded = timezone.now()
        data.date_modified = timezone.now()
        data.save()
        return redirect('home')


class AddRenderView(CreateView):
    """View for creating render."""

    pass
