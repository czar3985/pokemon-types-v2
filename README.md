# Pokemon Types

The application keeps a record of all pokemon grouped by type.

## Features

- View all pokemon in the database or per type
- View details of each pokemon
- Edit pokemon details
- Delete a pokemon
- Add a pokemon
- Log-in and Google authentication
- User authorization checks
- JSON API endpoints to acquire: 
  - List and details of all pokemon
  - All pokemon per type
  - Details of a specific pokemon
  - All categories
  - All types
  - All moves


## Prerequisites

1. **python 3.x**
2. **sqlalchemy**
3. **PostgreSQL**
4. **flask**
5. Pokemon Types app files (scripts, htmls, static files) 
6. Google developers account and client secret

## Usage

The following resource gives more information on how to run python scripts: 
[How to Run a Python Script via a File or the Shell](https://www.pythoncentral.io/execute-python-script-file-shell/).

_database_setup.py_ will setup the database: _pokemon.db_

_initial_entries.py_ will populate the database

_pokemon_types.py_ will run the web server 

### Routes

Navigate to port 8000.

Home page: http://localhost:8000/pokemon/

Page for each pokemon type: http://localhost:8000/pokemon/{type}
- Ex. http://localhost:8000/pokemon/fire

Details page for each pokemon: http://localhost:8000/pokemon/{id}/
- Ex. http://localhost:8000/pokemon/1

Page for creating a new pokemon entry in the database: 
http://localhost:8000/pokemon/new

Page for editing a pokemon entry: 
http://localhost:8000/pokemon/{id}/edit
- Ex. http://localhost:8000/pokemon/1/edit

Page for deleting a pokemon entry:
http://localhost:8000/pokemon/{id}/delete
- Ex. http://localhost:8000/pokemon/1/delete

Log-in page: http://localhost:8000/pokemon/login

Cleanup page for removing unused database entries: 
http://localhost:8000/pokemon/cleanup

JSON API endpoint for all pokemon in the database:
http://localhost:8000/pokemon/json

JSON API endpoint for all pokemon with the specified type in the database:
http://localhost:8000/pokemon/{type}/json
- Ex. http://localhost:8000/pokemon/fire/json

JSON API endpoint for pokemon with the specified id in the database:
http://localhost:8000/pokemon/{id}/json
- Ex. http://localhost:8000/pokemon/1/json

JSON API endpoint for all types in the database:
http://localhost:8000/pokemon/type/json

JSON API endpoint for all categories in the database:
http://localhost:8000/pokemon/category/json

JSON API endpoint for all moves in the database:
http://localhost:8000/pokemon/move/json


### Create client secret for Google log-in

Follow the steps below to create _client_secrets.json_

1. In https://console.developers.google.com/apis/dashboard, sign in to your Google account
2. Create Project. Indicate a name for the app
3. Go to your app's page in Google APIs Console
4. Choose Credentials
5. Create an OAuth Client ID.
6. Configure the consent screen, with email and app name
7. Choose Web application list of application types
8. Set the authorized JavaScript origins - http://localhost:8000
9. Authorized redirect URIs: http://localhost:8000/login and http://localhost:8000/gconnect
10. Download the client secret JSON file and copy the contents to client_secrets.json in the same folder as the pokemon_types.py file


## Database Structure

Pokemon table properties
```python
    id = Column(Integer, nullable=False, primary_key=True)
    pokedex_id = Column(Integer, nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(250), nullable=False)
    image = Column(String(250), nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    is_mythical = Column(Boolean, nullable=False)
    is_legendary = Column(Boolean, nullable=False)
    evolution_before = Column(Integer, nullable=True)
    evolution_after_list = Column(PickleType, nullable=True)
    type_list = Column(PickleType, nullable=False)
    weakness_list = Column(PickleType, nullable=False)
    move_list = Column(PickleType, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
```

Types table properties
```python
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
```

Moves table properties
```python
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
```

Categories table properties
```python
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
```

Users table properties
```python
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
```