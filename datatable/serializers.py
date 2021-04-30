from rest_framework import serializers

from datatable.models import Order


class OrderSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    client_name = serializers.ReadOnlyField(source='client.name')
    client_email = serializers.ReadOnlyField(source='client.email')
    client_phone = serializers.ReadOnlyField(source='client.phone')
    status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id', 'name', 'address',
            'state', 'zip_code', 'status',
            'date_start', 'date_end',
            'client_name', 'client_phone', 'client_email', 'amount')

    def get_status(self, obj: Order):
        return obj.get_status_display()
