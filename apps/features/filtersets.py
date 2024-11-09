from django_filters.rest_framework import FilterSet
from django_filters import CharFilter
from features.models import Component

class ComponentFilter(FilterSet):
    repository__contains = CharFilter(field_name='repository', lookup_expr='icontains')

    class Meta:
        model = Component
        fields = ['repository', 'status', 'build']
