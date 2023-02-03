from django.contrib import admin
from django.conf.urls import include
from rest_framework import routers
from django.urls import path
from levelupapi.views import register_user, login_user, GameTypeView, EventView, GameView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'gametypes', GameTypeView, 'gametype')
router.register(r'events', EventView, 'event')
router.register(r'games', GameView, 'game')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
]
