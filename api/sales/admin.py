from django.contrib import admin

from .models import Sale


class SaleAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "value",
        "date",
        "reseller",
        "status",
        "percentage",
        "cashback"
    )
    list_filter = ("reseller", "status", "date",)


admin.site.register(Sale, SaleAdmin)
