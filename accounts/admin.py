from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'user', 'phone_number', 'balance', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('account_number', 'user__username', 'phone_number')
    raw_id_fields = ('user',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    # If you want to customize how accounts are created in admin
    def save_model(self, request, obj, form, change):
        if not change:  # Only for new accounts
            # You could add automatic account number generation here
            pass
        super().save_model(request, obj, form, change)