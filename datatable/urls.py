from django.urls import path
from django.views.generic import TemplateView

from datatable.views import datatable_static, DataTableAPIView

urlpatterns = [
    path('static', datatable_static, name='datatable_static'),
    path('dynamic', TemplateView.as_view(template_name='datatable/datatable_dynamic.html'), name='datatable_dynamic'),
    path('data', DataTableAPIView.as_view(), name='datatable_data'),
]