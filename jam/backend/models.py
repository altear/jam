import numpy as np
import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField

class Minesweeper(models.Model):
    '''
    Model for backend

    When serialized, the player is only given visible information
    '''

    # The unique identifier of this game (used to return to an existing game by URL)
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Records whether a cell is a mine or not. [not_mine: 0, mine: 1]
    mine_positions = ArrayField(ArrayField(models.IntegerField()), null=True)

    # The cells whose values are visible to the player. [hidden: 0, visible: 1]
    visible_state = ArrayField(ArrayField(models.IntegerField()), null=True)

    # The cells that have been flagged by the player. [not_flagged: 0, flagged: 1]
    flag_state = ArrayField(ArrayField(models.IntegerField()), null=True)

    # The count of neighboring mines surrounding each cell.
    neighbors = ArrayField(ArrayField(models.IntegerField()), null=True)

    # hah. hah. hah. hah. hah.
    is_loser = models.BooleanField(default=False)

    # yeah right.
    is_winner = models.BooleanField(default=False)

    def flood_fill_safe_cells(self, starting_position):
        '''
        Given a starting coordinate, make all surrounding cells that do not border a mine visible.
        - Requires dimensions m > 2, n > 2 for m x n matrix

        :param position: tuple(i, j)
        '''
        # Floodfill implementation using a queue and breadth-first search
        queue = [starting_position]
        visited = set()
        m, n = np.array(self.mine_positions).shape # Get boundaries

        while len(queue):
            # Get the next point from the queue
            point = queue.pop(0)
            visited.add(point)

            new_points = set()  # Used to extend the existing queue
            i, j = point
            self.visible_state[i][j] = 1

            # If this cell has neighbors then we do not need to add its adjacent cells
            if self.neighbors[i][j] > 0:
                continue

            # Can we move left?
            if j + 1 < n:
                new_points.add((i, j + 1))

                # Can we move up?
                if i + 1 < m:
                    new_points.update([
                        (i + 1, j),
                        (i + 1, j + 1),
                    ])

                # Can we move down?
                if i > 0:
                    new_points.update([
                        (i - 1, j),
                        (i - 1, j + 1)
                    ])

            # Can we move right?
            if j > 0:
                new_points.add((i, j - 1))

                # Can we move up?
                if i + 1 < m:
                    new_points.update([
                        (i + 1, j),
                        (i + 1, j - 1),
                    ])

                # Can we move down?
                if i > 0:
                    new_points.update([
                        (i - 1, j),
                        (i - 1, j - 1),
                    ])

            # Filter out the points we've already visited or that are in the current queue
            visited_or_queued = visited | set(queue)
            filtered_new_points = list(filter(lambda x: x not in visited_or_queued, new_points))

            # Add new points onto the current queue
            queue.extend(filtered_new_points)

    def get_client_state_data(self):
        '''
        The data the client needs to display the game

        :return: message dictionary
        '''

        visible = np.array(self.visible_state)
        neighbors = np.array(self.neighbors)
        flags = np.array(self.flag_state)

        # Only the revealed neighbors will have numbers
        rendered_view = np.multiply(
            visible,
            neighbors
        )

        # Make the non-revealed cells all -1
        rendered_view[np.where(visible==0)] = -1

        # Make all cells with a flag on them -2
        rendered_view[np.where(flags==1)] = -2

        return {
            'message-type': 'game-state',
            'view': rendered_view.tolist(),
            'is_loser': self.is_loser,
            'is_winner': self.is_winner
        }

    def has_won(self):
        '''
        Check to see if the player has won
        :return:
        '''

        # todo: Arrays initialized multiple times. Look for how django loads model and create arrays once there.
        visible = np.array(self.visible_state)
        flagged = np.array(self.flag_state)
        mines = np.array(self.mine_positions)

        # If any of the flags are on cells that are not mines, the game is not over
        if not np.array_equal(mines, flagged):
            return False

        # If the player has revealed or flagged every possible position, then the union of visible and flagged squares
        # should be a matrix of 1s
        # - If the players steps on a mine in the last round they still won't win due to the order game_end conditions
        #   are checked
        return np.array_equal(
            np.bitwise_or(flagged.astype(bool), visible.astype(bool)),
            np.ones(shape=visible.shape)
        )

    def is_game_over(self):
        return self.is_winner or self.is_loser

    def is_position_in_boundaries(self, position):
        i, j = position
        m, n = np.array(self.visible_state).shape  # boundaries
        return (i >= 0 and i < m) and (j >=0 and j < n)

    def is_mine_at_position(self, position):
        i, j = position
        return bool(self.mine_positions[i][j])

    def is_flag_at_position(self, position):
        i, j = position
        return bool(self.flag_state[i][j])

    def is_position_visible(self, position):
        i, j = position
        return bool(self.visible_state[i][j])

    def is_valid_clear_area_position(self, position):
        '''
        Can the player clear this area of mines?
        :return: True/False
        '''
        return self.is_position_in_boundaries(position) and \
            not self.is_flag_at_position(position) and \
            not self.is_position_visible(position)

    def clear_area(self, position):
        '''
        Clear an area of mines
        :param position:
        :return:
        '''
        if self.is_game_over() or not self.is_valid_clear_area_position(position):
            return

        # Player clicked on a mine - player dies.
        if self.is_mine_at_position(position):
            self.is_loser = True
            return

        # Make surrounding areas visible if they have no neighboring mines
        self.flood_fill_safe_cells(position)

        if self.has_won():
            self.is_winner = True

    def plant_flag(self, position):
        '''
        This will add/delete a flag at a valid position

        :return:
        '''
        if self.is_game_over() or not self.is_position_in_boundaries(position) or self.is_position_visible(position):
            return

        # Add or remove the flag
        i, j = position
        if self.is_flag_at_position(position):
            self.flag_state[i][j] = 0
        else:
            self.flag_state[i][j] = 1

        if self.has_won():
            self.is_winner = True

    def count_adjacent_mines(self, mine_positions):
        '''
        Return an array that holds the counts to adjacent mines
        :param mine_positions:
        :return: adjacent_mines_count:
        '''

        # We count the adjacent mines by creating a stack of arrays from the game state. Each array is shifted in a
        # different direction. In this way, we can count the adjacent mines for each cell by taking the sum over the
        # stacked arrays.
        stack = [
            shift_up(mine_positions),
            shift_down(mine_positions),
            shift_left(mine_positions),
            shift_right(mine_positions),
            shift_left(shift_up(mine_positions)),
            shift_left(shift_down(mine_positions)),
            shift_right(shift_up(mine_positions)),
            shift_right(shift_down(mine_positions)),
        ]
        return np.sum(np.stack(stack), axis=0)

    def create_game(self, m=8, n=8, mines=20):
        '''
        Initialize a new game
        :param m: number of rows
        :param n: number of columns
        :param mines: number of mines
        :return:
        '''
        # todo make a is_first_move:bool, so the player cannot lose on their first turn
        # todo create model.Manager for Minesweeper and move this method into it
        empty_array = np.zeros(shape=(m,n), dtype=bool)

        # Select random indices to place mines
        indices = list(np.ndindex(n, m))  # Create a list of all possible indices in the game
        selected_indices = np.random.choice(np.arange(0, len(indices)), size=mines, replace=False)
        mine_indices = np.array(indices)[selected_indices]

        # Place the mines
        rows, cols = mine_indices[:, 0], mine_indices[:, 1]
        mine_positions = empty_array.copy()
        mine_positions[rows, cols] = 1
        self.mine_positions = mine_positions.tolist()

        # Visible and flag states start empty
        self.visible_state = empty_array.tolist()
        self.flag_state = empty_array.tolist()

        # Count the adjacent mines for each cell. Pass mines as param in case we want to generate mines in the future
        self.neighbors = self.count_adjacent_mines(mine_positions).tolist()

# todo consider moving array operations to new file
def shift_down(arr):
    '''
    Returns a new array with each element shifted down
    :param arr:
    :return:
    '''
    return np.r_[np.zeros((1, arr.shape[1])), arr[:-1, :]]

def shift_up(arr):
    '''
    Returns a new array with each element shifted up
    :param arr:
    :return:
    '''
    return np.r_[arr[1:, :], np.zeros((1, arr.shape[1]))]

def shift_left(arr):
    '''
    Returns a new array with each element shifted left
    :param arr:
    :return:
    '''
    return np.c_[arr[:, 1:], np.zeros(arr.shape[0])]

def shift_right(arr):
    '''
    Returns a new array with each element shifted right

    :param arr:
    :return:
    '''
    return np.c_[np.zeros(arr.shape[0]), arr[:, :-1]]  # shift matrix in direction  (0, -1)

