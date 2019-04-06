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
    return JsonResponse(game.render_player_view())

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

        # Check if valid move
        if not game.is_valid_move((i, j)):
            raise HttpResponseBadRequest()

        # Check if player just lost
        if game.is_losing_move((i, j)):
            game.is_loser = True
        # Player is still alive
        else:
            game.flood_fill_safe_cells((i,j))

        # Check if player is winner
        if game.has_won():
            game.is_winner = True

        game.save(force_update=True)
        return load_game(request, game_uid)

    except Exception as e:
        print(e)
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

        # Check if valid move
        if not game.is_valid_move((i, j)):
            raise HttpResponseBadRequest()

        # Plant the flag!
        game.flag_state[i][j] = 1

        # Did we win?
        if game.has_won():
            game.is_winner = True

        game.save(force_update=True)
        return load_game(request, game_uid)

    except:
        raise HttpResponseBadRequest()

def create_game(m, n, mines):
    '''
    Create a new mine sweeper game. This is in the view because it could be used to give the user control over
    difficulty in the future.

    :param m: rows
    :param n: cols
    :param mines: mine count
    :return:
    '''
    # Generate a new game using any parameters, or use the default ones
    new_game = Minesweeper.objects.create()
    new_game.generate_game(m,n,mines)
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
