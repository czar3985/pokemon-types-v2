# POKEMON_TYPES.PY is an application that allows a user to create, edit, delete
# and view pokemon in the database. It includes sign-in and user authentication
# features. It also features JSON API endpoints for acquiring data.

import random
import string
import httplib2
import json
import requests
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from database_setup import Base, engine, Pokemon, User, Category, Type, Move
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session as login_session,
    make_response,
    jsonify
    )
from view_model import (
    Pokemon_VM,
    get_type_id,
    get_category_id,
    get_move_id,
    get_pokemon_name_list,
    get_type_name_list,
    get_move_name_list,
    get_move_name, get_user_id
    )


app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = 'Pokemon Types'


# Connect to Database and create database session
engine = create_engine('sqlite:///pokemon.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#
# HELPER FUNCTIONS
#
def create_user(login_session):
    """Add a new user to the database"""

    # Use the log-in data to set the properties for the new user
    newUser = User(name=login_session['username'],
                   email=login_session['email'])
    session.add(newUser)
    session.commit()

    # Return the created id after committing to the database
    user = session.query(User).filter_by(email=login_session['email']).first()
    return user.id


def parse_evolution_after_list(pokemon_input):
    """Get the list of pokemon from the comma-separated input"""

    separated_input = pokemon_input.replace(' ', '').split(',')

    pokemon_list = []
    if separated_input:
        # Check if pokemon id is valid
        for item in separated_input:
            try:
                int(item)
                pokemon_list.append(item)
            except ValueError:
                continue

    return pokemon_list


def parse_type_list(type_input):
    """Get the list of types from the comma-separated input"""

    separated_input = type_input.split(',')

    type_list = []
    if separated_input:

        # All possible types have been added in the database.
        # Check each type input now for validity
        for item in separated_input:
            type = string.capwords(item.strip())

            id = get_type_id(type, session)
            if (id is not None):
                type_list.append(id)

    return type_list


def parse_move_list(move_input):
    """Get the list of moves from the comma-separated input"""

    separated_input = move_input.split(',')

    move_list = []
    if separated_input:

        # Check each move if already in the database
        for item in separated_input:
            move = string.capwords(item.strip())

            id = get_move_id(move, session)
            if (id is not None):
                move_list.append(id)
            else:
                if move == '':
                    continue

                # Move doesn't exist yet in the database. Add it.
                new_move = Move(name=move)
                session.add(new_move)
                session.commit()

                move_list.append(get_move_id(move, session))

    return move_list


def check_category(category_name):
    """Database entries are in capitalized first letter format"""

    category_name_cap = string.capwords(category_name)

    # Check if already in the database
    id = get_category_id(category_name_cap, session)

    if id is None:
        # Add to the database if not found
        new_category = Category(name=category_name_cap)
        session.add(new_category)
        session.commit()

        id = get_category_id(category_name_cap, session)

    return id


#
# DATABASE OPERATIONS
#
@app.route('/')
@app.route('/pokemon/')
def showHome():
    """Show all pokemon and types in the Home Page"""

    pokemon_list = session.query(Pokemon).order_by(asc(Pokemon.pokedex_id))

    # Indicate if there are no pokemon entries in the database
    if not pokemon_list:
        flash('There are currently no pokemon in the database.')

    types = session.query(Type).order_by(asc(Type.name))

    # Home page shown is different when a user is logged-in.
    # Add option is available
    if 'email' in login_session:
        return render_template('home_signed_in.html',
                               pokemon_list=pokemon_list,
                               types=types,
                               selected_type='All')
    else:
        return render_template('home.html',
                               pokemon_list=pokemon_list,
                               types=types,
                               selected_type='All')


@app.route('/pokemon/<string:type>')
def showType(type):
    """Show all pokemon with the specified type"""

    all_pokemon_list = session.query(Pokemon).order_by(asc(Pokemon.pokedex_id))
    all_types = session.query(Type).order_by(asc(Type.name))

    # If type specified is "All", use showHome that displays all pokemon
    if type.lower() == 'all':
        return redirect(url_for('showHome'))

    type_id = get_type_id(string.capwords(type), session)

    # Create a collection of the pokemon with the specified type
    pokemon_list = []
    if all_pokemon_list:
        for pokemon in all_pokemon_list:
            type_list = list(pokemon.type_list)
            if type_id in type_list:
                pokemon_list.append(pokemon)

    # Indication for when there are no pokemon found with the specified type
    if not pokemon_list:
        flash('There are currently no %s type pokemon in the database.' % type)

    # Page shown is different when a user is logged-in. Add option is available
    if 'email' in login_session:
        return render_template('home_signed_in.html',
                               pokemon_list=pokemon_list,
                               types=all_types,
                               selected_type=string.capwords(type))
    else:
        return render_template('home.html',
                               pokemon_list=pokemon_list,
                               types=all_types,
                               selected_type=string.capwords(type))


@app.route('/pokemon/<int:id>')
def showPokemon(id):
    """Show details page for the pokemon with the specified ID"""

    pokemon = session.query(Pokemon).filter_by(id=id).one()

    # Map the pokemon entry from the database to a structure with displayable
    # properties. Ex. Some entries are pointers to lists. Display
    # comma-separated list of corresponding strings instead
    pokemon_view_model = Pokemon_VM(pokemon, session)

    # If the entry's creator is signed in, the page allows Edits and Deletes
    if 'email' in login_session:
        if login_session['user_id'] == pokemon.user_id:
            return render_template('details_signed_in.html',
                                   pokemon=pokemon_view_model)

    return render_template('details.html', pokemon=pokemon_view_model)


@app.route('/pokemon/new', methods=['GET', 'POST'])
def newPokemon():
    """Page for creating a new pokemon entry"""

    # Only logged-in users may add new pokemon
    if 'email' not in login_session:
        return redirect(url_for('showLogin'))

    if request.method == 'POST':
        # Get the values inputted by the user in the form
        if request.form.get('mythical'):
            is_mythical = True
        else:
            is_mythical = False

        if request.form.get('legendary'):
            is_legendary = True
        else:
            is_legendary = False

        newPokemon = Pokemon(pokedex_id=request.form['pokedex_id'],
                             name=request.form['name'],
                             description=request.form['description'],
                             image=request.form['image'],

                             height=(request.form.get(
                                     'height_ft', type=int) * 12) +
                             request.form.get('height_inch', type=int),

                             weight=request.form['weight'],

                             is_mythical=is_mythical,
                             is_legendary=is_legendary,

                             evolution_before=request.form['evolution_before'],
                             evolution_after_list=parse_evolution_after_list(
                                 request.form['evolution_after']),

                             type_list=parse_type_list(request.form['type']),
                             weakness_list=parse_type_list(
                                 request.form['weakness']),
                             move_list=parse_move_list(request.form['move']),
                             category_id=check_category(
                                 request.form['category']),

                             user_id=login_session['user_id'])

        # Add the new pokemon entry to the database
        session.add(newPokemon)
        session.commit()

        # Indicate success in a message
        flash('New pokemon added')

        # Show the newly-added pokemon's details
        returnPokemon = session.query(Pokemon).filter_by(
            pokedex_id=newPokemon.pokedex_id).filter_by(
                name=newPokemon.name).filter_by(
                    description=newPokemon.description).filter_by(
                        image=newPokemon.image).first()
        return redirect(url_for('showPokemon', id=returnPokemon.id))

    else:
        # Show the form for adding new pokemon
        return render_template('new.html')


@app.route('/pokemon/<int:id>/edit', methods=['GET', 'POST'])
def editPokemon(id):
    """Allows editing of pokemon details"""

    # Only logged-in users may perform edits
    if 'email' not in login_session:
        return redirect(url_for('showLogin'))

    pokemon = session.query(Pokemon).filter_by(id=id).one()

    # Only the entry's creator may edit
    if pokemon.user_id != login_session['user_id']:
        flash('You are not authorized to edit that pokemon entry. '
              'You may only edit a pokemon entry you added.')
        return redirect(url_for('showHome'))

    if request.method == 'POST':
        # Get the edited pokemon details from the form
        pokemon.pokedex_id = request.form['pokedex_id']
        pokemon.name = request.form['name']
        pokemon.description = request.form['description']
        pokemon.image = request.form['image']

        pokemon.height = (request.form.get('height_ft', type=int) * 12)
        + request.form.get('height_inch', type=int)

        pokemon.weight = request.form['weight']

        if request.form.get('mythical'):
            pokemon.is_mythical = True
        else:
            pokemon.is_mythical = False

        if request.form.get('legendary'):
            pokemon.is_legendary = True
        else:
            pokemon.is_legendary = False

        pokemon.evolution_before = request.form['evolution_before']
        pokemon.evolution_after_list = parse_evolution_after_list(
            request.form['evolution_after'])
        pokemon.type_list = parse_type_list(request.form['type'])
        pokemon.weakness_list = parse_type_list(request.form['weakness'])
        pokemon.move_list = parse_move_list(request.form['move'])
        pokemon.category_id = check_category(request.form['category'])

        # Update the database entry for that pokemon
        session.add(pokemon)
        session.commit()

        # Indicate success in a message and show the added pokemon's details
        flash('Pokemon details edited')
        return redirect(url_for('showPokemon', id=id))

    else:
        # Show the form for editing the pokemon details
        # Show the displayable strings given the id list for some properties
        evolutions_after = ', '.join(str(item)
                                     for item in pokemon.evolution_after_list)
        types = ', '.join(get_type_name_list(pokemon.type_list, session))
        weaknesses = ', '.join(get_type_name_list(
            pokemon.weakness_list, session))
        moves = ', '.join(get_move_name_list(pokemon.move_list, session))

        return render_template('edit.html',
                               pokemon=pokemon,
                               evolutions_after=evolutions_after,
                               types=types,
                               weaknesses=weaknesses,
                               moves=moves)


@app.route('/pokemon/<int:id>/delete', methods=['GET', 'POST'])
def deletePokemon(id):
    """Delete the pokemon with the indicated id from the database"""

    # Only logged-in users may delete
    if 'email' not in login_session:
        return redirect(url_for('showLogin'))

    pokemon = session.query(Pokemon).filter_by(id=id).one()

    # Only the user that created the entry may delete
    if pokemon.user_id != login_session['user_id']:
        flash('You are not authorized to delete that pokemon entry. '
              'You may only delete a pokemon entry you added.')
        return redirect(url_for('showHome'))

    if request.method == 'POST':
        # Delete the entry from the database
        session.delete(pokemon)
        session.commit()

        # Indicate success in a message and go back to Home page
        flash('Pokemon deleted')
        return redirect(url_for('showHome'))

    else:
        # Ask for confirmation in the Delete page
        return render_template('delete.html', pokemon=pokemon)


@app.route('/pokemon/cleanup', methods=['GET', 'POST'])
def cleanup():
    """Moves and Categories may be added automatically when adding new
       pokemon. Cleanup removes the moves and categories previously added
       but are no longer associated with any pokemon and so are safe to remove.
    """

    all_pokemon = session.query(Pokemon).filter_by().all()

    # Get all categories (names) and moves (ids) in the database
    all_category_names = []
    all_categories = session.query(Category).filter_by().all()
    for category in all_categories:
        all_category_names.append(category.name)

    all_move_ids = []
    all_moves = session.query(Move).filter_by().all()
    for move in all_moves:
        all_move_ids.append(move.id)

    # Get categories and moves associated with pokemon entries
    categories_used = []        # List of names
    moves_used = []             # List of ids
    for pokemon in all_pokemon:
        if pokemon.category.name not in categories_used:
            categories_used.append(pokemon.category.name)
        for move_id in list(pokemon.move_list):
            if move_id not in moves_used:
                moves_used.append(move_id)

    # Get the categories (names) and moves (names) unused and can be deleted
    categories_to_delete = list(
        set(all_category_names).difference(categories_used))

    moves_to_delete = list(set(all_move_ids).difference(moves_used))
    move_names_to_delete = []
    for id in moves_to_delete:
        name = get_move_name(id, session)
        move_names_to_delete.append(name)

    if request.method == 'POST':
        # Deletion have been allowed by the user

        # Delete unused categories
        for item in categories_to_delete:
            category = session.query(Category).filter_by(name=item).first()
            session.delete(category)

        # Delete unused moves
        for item in move_names_to_delete:
            move = session.query(Move).filter_by(name=item).first()
            session.delete(move)

        session.commit()

        # Indicate success and go back to home page
        flash('Unused categories and moves have been deleted')
        return redirect(url_for('showHome'))

    else:
        # Confirmation page before performing deletes
        return render_template('cleanup.html',
                               categories_to_delete=categories_to_delete,
                               move_names_to_delete=move_names_to_delete)


#
# LOGIN-RELATED FUNCTIONS
#
@app.route('/pokemon/login/')
def showLogin():
    """Prepare for logging-in"""

	# Create anti-forgery state token
    # Python 2 to Python 3 modification
    # state = ''.join(random.choice(string.ascii_letters + string.digits)
    #                for x in xrange(32))
    state = ''.join(random.choice(string.ascii_letters + string.digits)
                    for x in range(32))
    login_session['state'] = state

    # Show the log-in page
    return render_template('login.html', CLIENT_ID=CLIENT_ID, STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Performs checks after logging in with a Google account"""

    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    # Python 2 to Python 3 modification
    # result = json.loads(h.request(url, 'GET')[1])
    result = json.loads((h.request(url, 'GET')[1]).decode('utf-8'))

    # If there was an error in the access token info, abort
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps('Token\'s user ID doesn\'t match given user ID.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps('Token\'s client ID does not match app\'s.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if the user is already logged-in
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # If no 'name' exists in the user info, use email instead
    if 'name' in data:
        login_session['username'] = data['name']
    else:
        login_session['username'] = data['email']
    login_session['email'] = data['email']

    # See if the user exists in the database or create a new entry
    userId = get_user_id(login_session['email'], session)
    if userId is None:
        userId = create_user(login_session)
    login_session['user_id'] = userId

    output = '<br />'

    # Log-in success message
    if login_session['username'] != '':
        flash('You are now logged in as %s' % login_session['username'])
    else:
        flash('You are now logged in as %s' % login_session['email'])

    return output


@app.route('/gdisconnect')
def gdisconnect():
    """Logs out of the Google account"""

    access_token = login_session.get('access_token')

    # Check if user is connected
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % login_session['access_token'])

    h = httplib2.Http()

    # No login session data indicates that no user is logged-in
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']

    # Redirect to home page after logging out
    response = make_response(redirect(url_for('showHome')))
    response.headers['Content-Type'] = 'text/html'

    return response


#
# JSON API ENDPOINTS
#
@app.route('/pokemon/json')
def showAllJson():
    """Shows all pokemon entries and details for each in JSON"""

    pokemon_list = session.query(Pokemon).all()

    # Use view model to display readable strings for columns containing
    # pointers to list
    return jsonify(Pokemon=[(Pokemon_VM(pokemon, session)).serialize
                            for pokemon in pokemon_list])


@app.route('/pokemon/<string:type>/json')
def showTypeJson(type):
    """Show JSON format of entries and details of pokemon with the specified
       type
    """

    all_pokemon_list = session.query(Pokemon).order_by(asc(Pokemon.pokedex_id))
    all_types = session.query(Type).order_by(asc(Type.name))
    pokemon_list = []

    if type.lower() == 'all':
        # Type: All shows all the pokemon
        pokemon_list = all_pokemon_list

    else:
        type_id = get_type_id(string.capwords(type), session)

        # Create a collection of pokemon with the specified type
        if all_pokemon_list:
            for pokemon in all_pokemon_list:
                type_list = list(pokemon.type_list)
                if type_id in type_list:
                    pokemon_list.append(pokemon)

    # Return JSON format of the collection of pokemon
    return jsonify(Pokemon=[(Pokemon_VM(pokemon, session)).serialize
                            for pokemon in pokemon_list])


@app.route('/pokemon/<int:id>/json')
def showPokemonJson(id):
    """Show JSON format of the details of the pokemon with the specified id"""

    # Get the pokemon
    pokemon = session.query(Pokemon).filter_by(id=id).first()

    if pokemon:
        # Show displayable string
        pokemon_view_model = Pokemon_VM(pokemon, session)

        return jsonify(Pokemon=[pokemon_view_model.serialize])
    else:
        # Return an empty collection
        return jsonify(Pokemon=[])


@app.route('/pokemon/category/json')
def showCategoriesJson():
    """Show JSON format of all categories in the database"""

    categories = session.query(Category).all()
    return jsonify(Categories=[category.serialize
                               for category in categories])


@app.route('/pokemon/type/json')
def showTypesJson():
    """Show JSON format of all types in the database"""

    types = session.query(Type).all()
    return jsonify(Types=[type.serialize for type in types])


@app.route('/pokemon/move/json')
def showMovesJson():
    """Show JSON format of all moves in the database"""

    moves = session.query(Move).all()
    return jsonify(Moves=[move.serialize for move in moves])

#
# MAIN FUNCTION
#
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True

    # App runs in http://localhost:8000/
    app.run(host='0.0.0.0', port=8000)
