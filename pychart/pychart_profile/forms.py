"""Form module."""

from django import forms
from pychart_profile.models import PyChartProfile


class UserProfileForm(forms.ModelForm):
    """Update form for user profile.

    Thanks, Claire and http://stackoverflow.com/questions/15889794/creating-one-django-form-to-save-two-models
    """

    def __init__(self, *args, **kwargs):
        """Setup the form fields to include User properties."""
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields["First Name"] = forms.CharField(
            initial=self.instance.user.first_name)
        self.fields["Last Name"] = forms.CharField(
            initial=self.instance.user.last_name)
        self.fields["Email"] = forms.EmailField(
            initial=self.instance.user.email)
        del self.fields["user"]

    class Meta:
        """Model for form and fields to exclude."""

        model = PyChartProfile
        exclude = []
