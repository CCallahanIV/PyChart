from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, UpdateView
import pandas as pd
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt


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


class AddRenderView(LoginRequiredMixin, TemplateView):
    """View for creating render."""
    template_name = "pychart_datarender/add_render.html"
    login_url = reverse_lazy("login")

    def get_context_data(self):
        user = self.request.user
        data_list = user.profile.data_sets.all()
        return {"data_sets": data_list}


from pychart_datarender.models import Data, Render
from django.http import JsonResponse
import json


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


import bokeh
from django.http import Http404


@csrf_exempt
def render_data(request):
    """Return rendered HTML from Bokeh for the given data."""
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        import pdb;pdb.set_trace()
    else:
        raise Http404
