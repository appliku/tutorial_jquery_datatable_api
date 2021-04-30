from django.contrib.postgres.search import SearchVector
from django.db.models import Sum, F, DecimalField
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from datatable.models import Order
from datatable.serializers import OrderSerializer


def datatable_static(request, *args, **kwargs):
    orders_qs = Order.objects.all().select_related('client').annotate(
        amount=Sum(
            F('orderline__unit_price') * F('orderline__quantity'),
            output_field=DecimalField())
    )
    return render(
        request=request,
        template_name="datatable/datatable_static.html",
        context={
            "order_list": orders_qs
        })


class DataTableAPIView(ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.all().select_related('client').annotate(
        amount=Sum(
            F('orderline__unit_price') * F('orderline__quantity'),
            output_field=DecimalField())
    )

    def filter_for_datatable(self, queryset):
        # filtering
        search_query = self.request.query_params.get('search[value]')
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector(
                    'name',
                    'client__name',
                    'address', 'zip_code')
            ).filter(search=search_query)
        # ordering
        ordering_column = self.request.query_params.get('order[0][column]')
        ordering_direction = self.request.query_params.get('order[0][dir]')
        ordering = None
        if ordering_column == '0':
            ordering = 'id'
        if ordering_column == '1':
            ordering = 'name'
        if ordering and ordering_direction == 'desc':
            ordering = f"-{ordering}"
        if ordering:
            queryset = queryset.order_by(ordering)
        return queryset

    def list(self, request, *args, **kwargs):
        draw = request.query_params.get('draw')
        queryset = self.filter_queryset(self.get_queryset())
        recordsTotal = queryset.count()
        filtered_queryset = self.filter_for_datatable(queryset)
        try:
            start = int(request.query_params.get('start'))
        except ValueError:
            start = 0
        try:
            length = int(request.query_params.get('length'))
        except ValueError:
            length = 10
        end = length + start
        serializer = self.get_serializer(filtered_queryset[start:end], many=True)
        response = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': filtered_queryset.count(),
            'data': serializer.data
        }
        return Response(response)
