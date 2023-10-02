from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from .forms import CreateUserForm


# Create your views here.

class HomePageView(TemplateView):
    template_name = "web/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_users = User.objects.all()
        context['list_users'] = list_users
        return context

class CreateUserView(CreateView):
    model = User
    # queryset = User.objects.all()
    form_class = CreateUserForm
    template_name = "web/log_up.html"
    success_url = reverse_lazy("web:home")

    def get_queryset(self):
        qs = User.objects.all()
        d = True
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = True
        return context
        

