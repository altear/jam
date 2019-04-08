# JAM: Just Another Minesweeper

Andre Telfer, 2019

![#delicious](./docs/_static/jam.jpg) 

<center> Photo by Jonathan Pielmayer on Unsplash </center>

## Demo
www.andretelfer.com

## Running

```
pipenv run python manage.py runserver
```

## Usage

```
pipenv run python manage.py runserver
```

## Requirements

- PostgreSQL 11.2 - Stable
- Python
  - pipenv
- Node 

## Installation

Install Python/Django dependencies with pipenv

``` 
pipenv install .
```

Install React dependencies with npm

```
npm install .
```

### Building

Create Django models 

```
pipenv run python manage.py makemigrations
```

Build main.js (React)

```
npm run dev
```

### Database
A Postgres database was used for this project

Configure Django to use the database using the `config.json` file 

Postgres commands for creating user/database (change the password):

```
psql
CREATE USER jam WITH PASSWORD 'adsfasdfasf' CREATEDB;
CREATE DATABASE jamdb WITH OWNER jam;
```

## Tests

Django tests

```
pipenv run python manage.py test
```

---

> &ldquo; **the only winning move is not to play**.&rdquo;  - WarGames, 1983

