from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("create/", views.start_record, name="create"),
    path("update/", views.update_record, name="update"),
    path("delete/", views.delete_records, name="delete"),
    path("mix/", views.both_update_and_create_records, name="mix"),
]
