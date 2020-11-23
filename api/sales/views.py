from rest_framework import viewsets

from .models import Sale
from .serializers import SaleSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    lookup_field = "identifier"

    def get_queryset(self):
        return Sale.objects.filter(reseller=self.request.user)