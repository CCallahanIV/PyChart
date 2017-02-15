
"""Views for pychart datarender app."""
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DetailView
from django.views.decorators.csrf import csrf_exempt
from pychart_datarender.models import Data, Render
from pychart_datarender.forms import DataForm, EditDataForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.http import Http404
from django.shortcuts import redirect
from django.utils import timezone
from django.urls import reverse_lazy
import pandas as pd
import json
import bokeh

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


class AddRenderView(LoginRequiredMixin, TemplateView):
    """View for creating render."""

    template_name = "pychart_datarender/add_render.html"
    login_url = reverse_lazy("login")

    def get_context_data(self):
        user = self.request.user
        data_list = user.profile.data_sets.all()
        return {"data_sets": data_list}


def retrieve_data(request, pk):
    """Define a view to handle ajax calls to retrieve data."""
    data_obj = Data.objects.get(pk=pk)
    data = pd.read_csv(data_obj.data)
    res = {}
    res['columns'] = []
    for col in data.columns.values:
        new_col = {}
        new_col['field'] = col
        new_col['title'] = col.upper()
        res['columns'].append(new_col)
    res['data'] = []
    for row in data.iterrows():
        new_row = {}
        for col in data.columns.values:
            new_row[col] = row[1][col]
        res['data'].append(new_row)
    return JsonResponse(json.dumps(res), safe=False)


@csrf_exempt
def render_data(request):
    """Return rendered HTML from Bokeh for the given data."""
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
    else:
        raise Http404


def render_to_db(**kwargs):
    """Save the rendered chart to the database."""
    new_chart = Render()
    new_chart.render = render
    new_chart.owner = user.profile
    new_chart.title = title
    new_chart.description = description
    new_chart.render_type = render_type
    new_chart.save()
