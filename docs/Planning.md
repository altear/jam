# Planning

## Strategy to Glue Django/React 

Have a Django app dedicated to loading the React source in a single web page. 

Source: 

> Gagliardi, Valentino. “Tutorial: Django REST with React (Django 2.0 and a Sprinkle of Testing).” *Valentino Gagliardi*, 19 Dec. 2018, www.valentinog.com/blog/tutorial-api-django-rest-react/. 

### Other Options?

- Have tiny react snippets in each Django template that requires it. 
  - This could really hurt code readability if there are a lot of snippets.
  - Doesn't seem very efficient for coding. 
- Completely separate the Django backend and React frontend. 
  - This might lead to security issues that will waste time. ie JWT authentication [Valentino, 2018]. 

## Models

Note that we can easily serialize/de-serialize numpy arrays which are convenient to work with for matrices. We can also convert numpy arrays into standard python lists using `array.tolist()`, which can then be serialized to JSON and read by React. 

It seems most simple to just use numpy when generating a game, store them as Django ArrayFields, and transfer them as JSON encoded lists.

### GameState

The complete state of a game

- [array2d] mine_positions: the true positions of all mines on the board.
- [array2d] mine_neighbors: the count of neighbors for each mine (saves on computation).
- [array2d] revealed_state: whether the position is revealed, flagged, or hidden.
- [bool] is_game_over: has this game finished? 
  - Useful for cleaning up old games if database becomes too large
- [datetime] last_modified: when did a player last make a move? 
  - Useful for cleaning up old games if database becomes too large

### PlayerView

- [array2d] revealed_state: just what the player should see.
- [bool] is_game_over: should we disable the UI or not?

## Algorithms

- Expanding the visible boxes around a player's action? Floodfill
- Getting neighbors cells? Copy game state 8x for each neighbor and shift in each direction. Count of neighboring mines at an index are the sum of these arrays (1 is a mine, 0 is no mine).
- Generating a new game? Select n-indices (n based on difficulty) using random choice from total indices. 

## Comments

CoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeBeerCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeWineCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffeeCoffee