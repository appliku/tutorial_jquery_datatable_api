from django.db import models

from datatable.tuples import ORDER_STATUSES


class Client(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ('name',)


class Order(models.Model):
    STATUS_CHOICES = (
        (ORDER_STATUSES.proposal, 'Proposal'),
        (ORDER_STATUSES.in_progress, 'In Progress'),
        (ORDER_STATUSES.done, 'Done'),
        (ORDER_STATUSES.rejected, 'Rejected'),
    )
    name = models.CharField(max_length=255)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)
    status = models.IntegerField(choices=STATUS_CHOICES, default=ORDER_STATUSES.proposal)
    date_start = models.DateField()
    date_end = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ('date_end',)


class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, )
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Order Line"
        verbose_name_plural = "Order Lines"
        ordering = ('name',)
