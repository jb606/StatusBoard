from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML, Layout, Field, Row, Column
from crispy_forms.bootstrap import FormActions
from . import models


class GroupForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = ["name", "description"]

    layout = Layout(
        "name",
        "description",
        FormActions(
            Submit("submit", "Submit", css_class="btn btn-sm"),
            # HTML('<a href="{% url "sb-default" %}" class="btn btn-sm btn-link">Cancel</a>'),
        ),
    )
    helper = FormHelper()
    helper.layout = layout


class UserStatusForm(forms.ModelForm):

    class Meta:
        model = models.UserStatus
        fields = "__all__"
        exclude = ["user", "slug", "updated_by"]
        labels = {
            "lock_status": "Lock Status",
            "lock_notes": "Lock Notes",
        }

    layout = Layout(
        Row(
            Column("status", css_class="col-1"),
            Column("notes", css_class="col-8"),
            Column("lock_status", "lock_notes", css_class="col"),
            Column(
                HTML('<label for="submit-id-submit" class="form-label"></label>'),
                FormActions(
                    Submit("submit", "Update", css_class="btn btn-danger"),
                    css_class="col-1",
                ),
                HTML(
                    '<a href="{% url "home" %}" class="btn btn-sm btn-link">Cancel</a>'
                ),
            ),
            css_class="row text-start mb-2",
        ),
    )
    # helper = FormHelper()
    # helper.layout = layout
