import json
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, get_object_or_404, render
from backend.models import Minesweeper

def load_game(request, game_uid):
    '''
    Find an existing minesweeper game

    :param request:
    :param game_uid:
    :return:
    '''
    game = get_object_or_404(Minesweeper, uid=game_uid)
    return JsonResponse(game.get_client_state_data())

def clear_area(request, game_uid):
    '''
    Make a move in an existing game. Expecting a json containing i,j coordinates

    :param request:
    :param game_uid:
    :return:
    '''
    game = get_object_or_404(Minesweeper, uid=game_uid)

    # Return bad request if there are any problems (ie. fields aren't present or can't be cast as integers)
    try:
        # Load data
        data = json.loads(request.body)
        i, j = int(data['i']), int(data['j'])

        game.clear_area(position=(i,j))
        game.save(force_update=True)
        return load_game(request, game_uid)

    except:
        raise HttpResponseBadRequest

def plant_flag(request, game_uid):
    '''
    Make a move in an existing game. Expecting a json containing i,j coordinates

    :param request:
    :param game_uid:
    :return:
    '''
    game = get_object_or_404(Minesweeper, uid=game_uid)

    # Return bad request if there are any problems (ie. fields aren't present or can't be cast as integers)
    try:
        # Load data
        data = json.loads(request.body)
        i, j = int(data['i']), int(data['j'])

        # Plant the flag and update
        game.plant_flag(position=(i, j))
        game.save(force_update=True)
        return load_game(request, game_uid)
    except:
        raise HttpResponseBadRequest

# todo Note: This is in the view because it could be added to the API(if I have time), giving user control of map size
def create_game(m, n, mines):
    '''
    Create a new mine sweeper game.

    :param m: rows
    :param n: cols
    :param mines: mine count
    :return:
    '''
    # Generate a new game using any parameters, or use the default ones
    new_game = Minesweeper.objects.create()
    new_game.create_game(m,n,mines)
    new_game.save()

    return {
        "message-type": "new-game",
        "uuid": new_game.uid
    }

def create_small_game(request):
    return JsonResponse(create_game(8, 8, 8))

def create_medium_game(request):
    return JsonResponse(create_game(15, 15, 25))

def create_large_game(request):
    return JsonResponse(create_game(30, 30, 150))
