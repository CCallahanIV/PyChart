from django.db import models

# Create your models here.

class Data(models.Model):
    """Implementation of data model."""
    title = models.Charfield(max_length=255, blank=False, null=False)
    description = models.Charfield(max_length=255, blank=True, null=True)
    data = models.FileField(upload_to=' ', blank=True, null=True)
    date_uploaded = models.DateField(auto_now=True)
    date_modified = models.DateField(auto_now=True)
    # owner = models.ForeignKey(Profile,
    #                           related_name='data_sets',
    #                           blank=False,
    #                           null=False)

    def __str__(self):
        """Create string representation of this model."""
        return self.title


class Render(models.model):
    """Implementation of render model."""

    RENDER_TYPE = (
        ('Scatter', 'Scatter'),
        ('Bar', 'Bar'),
        ('Histogram', 'Histogram')
    )

    title = models.Charfield(max_length=255, blank=False, null=False)
    description = models.Charfield(max_length=255, blank=True, null=True)
    render_type = models.Charfield(max_length=255,
                                   choices=RENDER_TYPE,
                                   blank=True,
                                   null=True)
    date_uploaded = models.DateField(auto_now=True)
    date_modified = models.DateField(auto_now=True)

    def __str__(self):
        """Create string representation of this model."""
        return self.title
