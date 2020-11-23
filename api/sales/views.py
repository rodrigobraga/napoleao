import requests

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.conf import settings

from .models import Sale
from .serializers import SaleSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    lookup_field = "identifier"
    filterset_fields = ("date", "percentage", "status",)

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):  # pragma: no cover
            return Sale.objects.none()

        return Sale.objects.filter(reseller=self.request.user)

    @action(detail=False, methods=['get'])
    def accumulated(self, request, identifier=None):
        url = settings.ACCUMULATED_API_BASE_URL
        token = settings.ACCUMULATED_API_TOKEN
        headers = {"token": token}
        params = {"cpf": request.user.cpf}

        try:
            accumulated = requests.get(url, headers=headers, params=params)
            accumulated = accumulated.json()
            status_code = accumulated.get("statusCode")
            body = accumulated.get("body")

            if not status_code == 200:
                raise ValueError("an error has occurred")

        except ValueError:
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(body,  status=status.HTTP_200_OK)
