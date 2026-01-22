from django_tables2 import tables, TemplateColumn, LinkColumn
from . import models
from django.contrib.auth import get_user_model
from django_tables2.utils import A

Person = get_user_model()


class GroupTable(tables.Table):
    name = LinkColumn("status:sb-group-view", args=[A("slug")])

    class Meta:
        model = models.Group
        attrs = {"class": "table table-sm"}
        fields = ["name", "description"]

    # actions = TemplateColumn(template_name="Roster/list_actions.html")


class UserStatusTable(tables.Table):
    class Meta:
        model = models.UserStatus
        attrs = {"class": "table table-sm"}
        fields = ["user", "status", "notes"]
