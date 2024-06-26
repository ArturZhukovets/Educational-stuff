import datetime

import requests
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView


BASE_URL = 'https://httpbin.org/'

@method_decorator(cache_page(60 * 5), name='dispatch')
class ApiCalls(TemplateView):
    template_name = 'apicalls/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        response = requests.get(f'{BASE_URL}/delay/2')
        response.raise_for_status()

        context['content'] = 'Results received!'
        context['current_time'] = datetime.datetime.now()
        return context
