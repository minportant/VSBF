from .models import Profile
import django_filters

class DropdownFilter(django_filters.FilterSet):
    class Meta:
        model = Profile
        fields = ['name','major','graduation',]

