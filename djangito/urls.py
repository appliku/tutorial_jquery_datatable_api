from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('sns/', include('ses_sns.urls')),
    path('datatable/', include('datatable.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
