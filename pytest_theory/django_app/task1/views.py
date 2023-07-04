from django.http import HttpResponse
from django.urls import reverse_lazy

from django.views.generic import RedirectView


class HomeView(RedirectView):
    permanent = False
    pattern_name = "budget:list"


