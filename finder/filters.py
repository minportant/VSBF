'''***************************************************************************************
*  REFERENCES
*  Title: How to Filter QuerySets Dynamically
*  Author: Vitor Freitas
*  Date: 11/28/16
*  Code version: 1.0
*  URL: https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
*  Software License: BSD
***************************************************************************************'''

from .models import Profile
from django.db import models
import django_filters

class DropdownFilter(django_filters.FilterSet):
    class Meta:
        model = Profile
        fields = ['name', 'major', 'graduation']
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }
