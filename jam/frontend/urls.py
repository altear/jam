from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_game),
    path('games/<str:game_uid>', views.game),
]