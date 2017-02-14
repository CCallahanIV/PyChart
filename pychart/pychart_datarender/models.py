from django.db import models
from pychart_profile.models import PyChartProfile

# Create your models here.

class Data(models.Model):
    """Implementation of data model."""
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    data = models.FileField(upload_to='data', blank=True, null=True)
    date_uploaded = models.DateField(auto_now=True)
    date_modified = models.DateField(auto_now=True)
    owner = models.ForeignKey(PyChartProfile,
                              related_name='data_sets',
                              blank=False,
                              null=True)

    def __str__(self):
        """Create string representation of this model."""
        return self.title


class Render(models.Model):
    """Implementation of render model."""

    RENDER_TYPE = (
        ('Scatter', 'Scatter'),
        ('Bar', 'Bar'),
        ('Histogram', 'Histogram')
    )

    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    render_type = models.CharField(max_length=255,
                                   choices=RENDER_TYPE,
                                   blank=True,
                                   null=True)
    render = models.TextField(blank=True, null=True)
    date_uploaded = models.DateField(auto_now=True)
    date_modified = models.DateField(auto_now=True)
    owner = models.ForeignKey(PyChartProfile,
                              related_name='my_renders',
                              blank=False,
                              null=True)


    def __str__(self):
        """Create string representation of this model."""
        return self.title
