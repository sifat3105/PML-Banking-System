from django.db import models
from django.utils import timezone
from accounts.models import Account

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
        ('received ', 'Received '),
    ]
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)

    def __str__(self):
        return f"{self.get_transaction_type_display()} of ${self.amount}"

    class Meta:
        ordering = ['-timestamp']