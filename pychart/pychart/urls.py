"""The URLs for pychart."""

from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from pychart.views import HomeView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^login/$', auth_views.login, name="login"),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^profile/', include('pychart_profile.urls')),
    url(r'^data/', include('pychart_datarender.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
