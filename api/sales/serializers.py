from rest_framework import serializers

from users.models import User

from .models import Sale


class SaleSerializer(serializers.ModelSerializer):
    reseller = serializers.SlugRelatedField(
        required=True, slug_field="username", queryset=User.objects.all(),
    )

    class Meta:
        model = Sale
        fields = (
            "identifier",
            "reseller",
            "code",
            "value",
            "date",
            "status",
            "percentage",
            "cashback"
        )
        read_only_fields = ("status", "percentage", "cashback",)
