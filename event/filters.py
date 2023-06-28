import django_filters
from django_filters import DateFilter
from .models import *

class EventFilter(django_filters.FilterSet):
    start_date=DateFilter(field_name="date_created", lookup_expr='gte')
    class Meta:
        model=Event
        fields='__all__'
        exclude=['participant', 'date_created', 'review']