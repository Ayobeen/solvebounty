import django_filters
from .models import Challenge

class ChallengeFilter(django_filters.FilterSet):
    min_prize = django_filters.NumberFilter(field_name="budget", lookup_expr='gte')
    max_prize = django_filters.NumberFilter(field_name="budget", lookup_expr='lte')
    category = django_filters.CharFilter(field_name="category", lookup_expr='iexact')
    status = django_filters.CharFilter(field_name="status", lookup_expr='iexact')
    skill = django_filters.CharFilter(field_name="skills__name", lookup_expr='iexact')

    class Meta:
        model = Challenge
        fields = ['category', 'status', 'currency', 'min_prize', 'max_prize', 'skill']
