
"""Views for pychart datarender app."""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DetailView
from pychart_datarender.forms import DataForm, EditDataForm, EditRenderForm
from pychart_datarender.models import Data, Render
from bokeh.charts import Scatter, output_file, save, Bar, Histogram
import json
import pandas as pd


class GalleryView(LoginRequiredMixin, TemplateView):
    """Class based view for gallery."""

    template_name = 'pychart_datarender/gallery.html'
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("gallery")

    def get_context_data(self):
        """Show a user's data and renders."""
        the_user = self.request.user
        user_data = Data.objects.filter(owner=the_user.profile)
        user_renders = Render.objects.filter(owner=the_user.profile)
        context = {'data': user_data, 'renders': user_renders}
        return context


class DataDetailView(TemplateView):
    """Class based view for a single data object."""

    template_name = 'pychart_datarender/data_id.html'

    def get_context_data(self, pk):
        """Get context for single data object."""
        data = Data.objects.get(pk=pk)
        return {'data': data}


class RenderDetailView(DetailView):
    """Class based view for a single render object."""

    template_name = "pychart_datarender/render_detail.html"
    model = Render

    def get_context_data(self, **kwargs):
        """Get context for single render."""
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
    success_url = reverse_lazy('data_library_view')
    form_class = EditDataForm
    model = Data


class EditRenderView(UpdateView):
    """View for editing render."""

    template_name = 'pychart_datarender/edit_render.html'
    success_url = reverse_lazy('gallery')
    form_class = EditRenderForm
    model = Render


class AddDataView(CreateView):
    """View for creating data."""

    model = Data
    form_class = DataForm
    template_name = 'pychart_datarender/add_data.html'

    def form_valid(self, form):
        """Overwrite form_valid method to add user to form before save."""
        data = form.save()
        data.owner.add(self.request.user.profile)
        data.date_uploaded = timezone.now()
        data.date_modified = timezone.now()
        data.save()
        return redirect('data_library_view')


class AddRenderView(LoginRequiredMixin, TemplateView):
    """View for creating render."""

    template_name = "pychart_datarender/add_render.html"
    login_url = reverse_lazy("login")

    def get_context_data(self):
        """Return only user's data sets."""
        user = self.request.user
        data_list = user.profile.data_sets.all()
        return {"data_sets": data_list}


def add_owner_view(request, pk):
    """Function based view to add data objects to user from library page."""
    data = Data.objects.get(pk=pk)
    profile = request.user.profile
    if data in profile.data_sets.all():
        pass
    else:
        profile.data_sets.add(data)
    return redirect('gallery')


@login_required
def retrieve_data(request, pk):
    """Define a view to handle ajax calls to retrieve data."""
    data_obj = Data.objects.get(pk=pk)
    data = pd.read_csv(data_obj.data)
    res = refactor_data(data)
    return JsonResponse(json.dumps(res), safe=False)


def refactor_data(data):
    """Given a DataFrame, return JSON for use in Bootstrap Table."""
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
    return res


@login_required
def render_data(request):
    """Return rendered HTML from Bokeh for the given data."""
    if request.method == 'POST':
        request_data = json.loads(request.body.decode('utf-8'))
        form_data = request_data['form_data']
        table_data = request_data['table_data']
        html = render_chart(form_data, pd.DataFrame(table_data))
        return HttpResponse(html)
    else:
        raise Http404


@login_required
def save_render(request):
    """Save render."""
    if request.method == 'POST':
        request_data = json.loads(request.body.decode('utf-8'))
        request_data["user"] = request.user
        render_to_db(request_data)
        redirect_url = reverse('gallery')
        response = {'url': redirect_url}
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        raise Http404


def render_chart(form_data, table_data):
    """Generate bokeh plot from input dataframe."""
    if form_data['chart_type'] == 'Scatter':
        return generate_scatter(table_data, form_data)
    elif form_data['chart_type'] == 'Bar':
        return generate_bar(table_data, form_data)
    elif form_data['chart_type'] == 'Histogram':
        return generate_histogram(table_data, form_data)


def generate_scatter(table_data, form_data):
    """Generate scatter plot."""
    if form_data['marker'] == '':
        form_data['marker'] = None
    if form_data['color'] == '':
        form_data['color'] = None
    plot = Scatter(table_data,
                   x=form_data['x'],
                   y=form_data['y'],
                   title=form_data['x'] + ' vs ' + form_data['y'],
                   color=form_data['color'],
                   marker=form_data['marker'],
                   tools='pan,wheel_zoom,box_zoom,reset,resize,hover,save')
    plot.title.text_font_style = "bold"
    output_file("output.html")
    save(plot)
    return build_html()


def generate_bar(table_data, form_data):
    """Generate Bar plot."""
    if form_data['group'] == '':
        form_data['group'] = False
    plot = Bar(table_data,
               label=form_data['label'],
               values=form_data['values'],
               agg=form_data['agg'],
               title=form_data['label'] + ' vs ' + form_data['values'],
               group=form_data['group'],
               tools='pan,wheel_zoom,box_zoom,reset,resize,hover,save')
    plot.title.text_font_style = "bold"
    output_file("output.html")
    save(plot)
    return build_html()


def generate_histogram(table_data, form_data):
    """Generate histogram."""
    if form_data['color'] == '':
        color = 'blue'
    else:
        color = form_data['color']
    plot = Histogram(table_data,
                     values=form_data['column'],
                     color=color,
                     tools='pan,wheel_zoom,box_zoom,reset,resize,hover,save')
    plot.title.text_font_style = "bold"
    output_file("output.html")
    save(plot)
    return build_html()


def build_html():
    """Build html file from the resulting graph."""
    lines = []
    with open('output.html', 'r') as infile:
        for line in infile:
            if "<title>Bokeh Plot</title>" in line:
                pass
            else:
                lines.append(line)
    return ''.join(lines)


def render_to_db(render_data):
    """Save the rendered chart to the database."""
    new_chart = Render()
    new_chart.render = render_data["html"]
    new_chart.owner = render_data["user"].profile
    new_chart.title = render_data["title"]
    new_chart.description = render_data["description"]
    new_chart.render_type = render_data["render_type"]
    new_chart.save()
