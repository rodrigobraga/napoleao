from rest_framework import routers

from .views import SaleViewSet

app_name = "sales"

router = routers.SimpleRouter()
router.register("", SaleViewSet, basename="sale")

urlpatterns = router.urls
