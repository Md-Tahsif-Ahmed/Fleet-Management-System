from django.urls import path

from .views import reports, export_report


urlpatterns = [
    path('export/', export_report, name='export_report'),
    path('', reports, name='reports'),
]