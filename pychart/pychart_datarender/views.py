from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, UpdateView
from pychart_datarender.models import Data, Render
from pychart_datarender.forms import DataForm, EditDataForm
from django.utils import timezone
from django.shortcuts import redirect

class GalleryView(TemplateView):
    """View for gallery."""

    pass


class DataDetailView(TemplateView):
    """View for data detail."""

    template_name = 'pychart_datarender/data_id.html'

    def get_context_data(self, pk):
        """Get context for album view."""
        data = Data.objects.get(pk=pk)
        return {'data': data}



class RenderDetailView(TemplateView):
    """View for data render."""

    pass


class DataLibraryView(TemplateView):
    """View for data library."""

    pass


class EditDataView(LoginRequiredMixin, UpdateView):
    """View for editing dataset."""
    login_required = True
    template_name =  'pychart_datarender/edit_data.html'
    success_url = reverse_lazy('home')
    # form_class =
    model = Data 

    def get_form(self):


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

