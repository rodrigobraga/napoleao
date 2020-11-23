from rest_framework import routers

from .views import UserViewSet, UserCreate

app_name = "users"

router = routers.SimpleRouter()
router.register("register", UserCreate, basename="register")
router.register("user", UserViewSet, basename="user")

urlpatterns = router.urls
