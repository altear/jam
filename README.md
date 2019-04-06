# JAM: Just Another Minesweeper

Andre Telfer, 2019

![#delicious](./docs/_static/jam.jpg) 

<center> Photo by Jonathan Pielmayer on Unsplash </center>

## Running

```
pipenv run python manage.py runserver
```

## Usage

```
pipenv run manage.py runserver
```

## Requirements

- PostgreSQL 11.2 - Stable
- Python 3.6
  - pipenv

## Installation

Install Python/Django dependencies with pipenv

``` 
pipenv install .
```

Install React dependencies with npm

```
npm install .
```

## Configuration

### Database

Configure Django to use the database using the `config.json` file 

Postgres commands for creating user/database (change the password):

```
psql
CREATE USER jam WITH PASSWORD 'put_your_password_here' CREATEDB;
CREATE DATABASE jamdb WITH OWNER jam;
```

## Tests

Django tests

```
pipenv run python manage.py test
```

---

> &ldquo; **the only winning move is not to play**.&rdquo;  - WarGames, 1983

