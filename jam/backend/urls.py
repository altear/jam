from django.urls import path
from . import views

urlpatterns = [
    path('create-small-game/', views.create_small_game),
    path('create-medium-game/', views.create_medium_game),
    path('create-large-game/', views.create_large_game),
    path('games/<str:game_uid>', views.load_game),
    path('games/<str:game_uid>/clear-area/', views.clear_area),
    path('games/<str:game_uid>/plant-flag/', views.plant_flag)
]
