from django.contrib import admin
from datatable.models import Order, OrderLine, Client

admin.site.register(Order)
admin.site.register(OrderLine)
admin.site.register(Client)
