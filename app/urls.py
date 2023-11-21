from django.urls import include,path
from rest_framework import routers
from . import views
from .views import UserViewSet, KulutusViewSets,register_user, login_user



router = routers.DefaultRouter()
router.register(r"kulutus", KulutusViewSets,"nimi")
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path("api/", include((router.urls,"app"))),
    path('login/', login_user, name='login_user'),
    path('register/', register_user, name='register_user'),
]

