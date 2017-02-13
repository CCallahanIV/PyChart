"""URLs for the imager_profile app."""

from django.conf.urls import url

from . import views

app_name = 'pychart_profile'

urlpatterns = [
    url(r'^$', views.ProfileView.as_view(), name="profile"),
    url(r'^edit/$', views.EditProfileView.as_view(), name="edit_profile"),
    url(r'^(?P<username>[\w.@+-]+)/$', views.UserProfileView.as_view(), name="user_profile"),
]
