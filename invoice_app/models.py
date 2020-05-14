from django.db import models
from membership.models import UserMembership

# "Pending", "Processing", "Draft", "Cancelled", "Completed"

INVOICE_STATUS = (
    ("pending", "Pending"),
    ("processing", "Processing"),
    ("draft", "Draft"),
    ("cancelled", "Cancelled"),
    ("completed", "Completed"),
)

class Invoice(models.Model):
    inv_date = models.DateField(auto_now_add=True, editable=False)
    inv_number = models.IntegerField()
    inv_receiving_member = models.ForeignKey(UserMembership, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True, blank=True)
    due_date = models.DateField(auto_now_add=True, editable=False, blank=True)
    total_amount = models.DecimalField(max_digits=19, decimal_places=4)
    # member = models.OneToOneField(UserMembership, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=INVOICE_STATUS)

    # purchased =


class InvoiceItem(models.Model):
    inv_id = models.OneToOneField(Invoice, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=19, decimal_places=4)
    rate = models.DecimalField(max_digits=10, decimal_places=4)




