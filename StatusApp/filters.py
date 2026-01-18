from django_filters import FilterSet
from . import models


class GroupFilter(FilterSet):
    class Meta:
        model = models.Group
        fields = {"name"}
