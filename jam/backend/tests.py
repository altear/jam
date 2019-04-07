import json
import numpy as np
from django.test import TestCase
from django.test.client import RequestFactory
from backend.models import Minesweeper
from backend.views import create_game, load_game, clear_area

class MinesweeperTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_count_adjacent_cells(self):
        '''
        Test expected behavior when counting adjacent cells
        '''
        arr = np.array([
            [0,1,1],
            [0,0,1],
            [1,0,0]
        ])

        expected = np.array([
            [1, 2, 2],
            [2, 4, 2],
            [0, 2, 1]
        ])

        assert np.array_equal(Minesweeper.count_adjacent_mines({},arr), expected)

    def test_flood_fill(self):
        '''
        Check the results of floodfill using a visible_state
        '''

        neighbor_state = np.array([
            [0, 1, 1],
            [0, 1, 1],
            [0, 0, 0],
            [1, 0, 1]
        ])

        flood_fill_starting_point = (0, 0)
        expected_visible_state = np.array([
            [1, 1, 0],
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ])

        # Create the new game
        new_game = Minesweeper.objects.create()
        new_game.neighbors = neighbor_state.tolist()
        new_game.visible_state = np.zeros(neighbor_state.shape).tolist()
        new_game.mine_positions = np.zeros(neighbor_state.shape).tolist()

        # Call the flood_fill to update the visible state
        new_game.flood_fill_safe_cells(flood_fill_starting_point)
        assert np.array_equal(new_game.visible_state, expected_visible_state)

    def test_create_game_small(self):
        new_game = Minesweeper.objects.create()
        new_game.generate_game(m=5,n=5,mines=10)

    def test_create_game_medium(self):
        new_game = Minesweeper.objects.create()
        new_game.generate_game(m=10, n=10, mines=10)

    def test_create_game_large(self):
        new_game = Minesweeper.objects.create()
        new_game.generate_game(m=30, n=30, mines=10)
        assert new_game.uid

    def test_load_game(self):
        new_game = Minesweeper.objects.create()
        new_game.generate_game(m=30, n=30, mines=10)
        new_game.save()

        request = self.factory.get(f'/api/games/{new_game.uid}')
        response = load_game(request, new_game.uid)
        self.assertEqual(response.status_code, 200)

    def test_clear_area(self):
        new_game = Minesweeper.objects.create()
        new_game.generate_game(m=30, n=30, mines=10)
        new_game.save()

        data = json.dumps({'i': 0, 'j': 0})
        request = self.factory.post(f'/api/games/{new_game.uid}/move', data, 'application/json')
        response = clear_area(request, new_game.uid)
        self.assertEqual(response.status_code, 200)

    def test_flood_fill_from_move(self):
        '''
        After a player makes a move on an empty board, the entire board should be visible
        :return:
        '''

        # Create a new game
        new_game = Minesweeper.objects.create()
        new_game.generate_game(m=5, n=5, mines=0)
        new_game.save()

        # Submit a move
        data = json.dumps({'i': 2, 'j': 2})
        request = self.factory.post(f'/api/games/{new_game.uid}/move', data, 'application/json')
        response = clear_area(request, new_game.uid)

        # Check if response is all 1s like expected
        new_game = Minesweeper.objects.get(uid=new_game.uid)
        assert np.array_equal(np.array(new_game.visible_state), np.ones((5,5)))