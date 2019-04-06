from django.shortcuts import redirect, render
from backend.views import create_game

def game(request, game_uid):
    return render(request, 'frontend/index.html')

def start_game(request):
    '''
    Hacky redirect to new game. We're skipping a menu this time
    '''
    return redirect(f"/games/{create_game(30,30,50)['uuid']}")
