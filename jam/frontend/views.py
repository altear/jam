from django.shortcuts import redirect, render
from backend.views import create_game

def game(request, game_uid):
    return render(request, 'frontend/index.html')

def start_game(request):
    return render(request, 'frontend/index.html')
