"""Url patterns for data render app."""
from django.conf.urls import url
from pychart_datarender.views import (
    GalleryView,
    DataDetailView,
    RenderDetailView,
    DataLibraryView,
    EditDataView,
    EditRenderView,
    AddDataView,
    AddRenderView,
    retrieve_data,
    render_data,
    save_render
)

urlpatterns = [

    url(r'^gallery/$', GalleryView.as_view(), name='gallery'),
    url(r'^data/(?P<pk>\d+)/$', DataDetailView.as_view(), name='data_detail'),
    url(r'^render/(?P<pk>\d+)/$', RenderDetailView.as_view(), name='render_detail'),
    url(r'^data/(?P<pk>\d+)/edit/$', EditDataView.as_view(), name='data_edit'),
    url(r'^render/(?P<pk>\d+)/edit/$', EditRenderView.as_view(), name='render_edit'),
    url(r'^render/add/$', AddRenderView.as_view(), name='render_add'),
    url(r'^retrieve/(?P<pk>\d+)$', retrieve_data, name="get_data"),
    url(r'^retrieve/render/$', render_data, name="get_render"),
    url(r'^data/add/$', AddDataView.as_view(), name='data_add'),
    url(r'^library/$', DataLibraryView.as_view(), name='data_library_view'),
    url(r'^render/create/$', save_render, name="save_render")
]
