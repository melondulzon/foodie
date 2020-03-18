from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from config.config import Config
import json

""" 
    This file takes the recipe database and transfers it to a mongodb collection.
    In addition a first user will be inserted to the user collection and filter
    keywords will be extracted from the database and stored in a filters collection
    for easy and quick queries and to be used to create menus and options.
"""

#  configure mongodb, during development ('localhost', 27017) was used
client = MongoClient(Config.MONGO_URI)

# database / collections
db = client.foodie
recipes = db.recipes
users = db.users
filters = db.filters


# ============================================ #


def add_recipes():

    """
        Add recipes to recipe collection
    """

    with open('db.json') as db_file:
        data = json.load(db_file)
        recipes.insert_many(data['recipes'])


# ============================================ #


def add_user():

    """
        Add first user to user collection
    """

    with open('../schemas/user.json') as users_file:
        user = json.load(users_file)
        user['username'] = 'sean'
        user['password'] = generate_password_hash('password')
        users.insert_one(user)


# ============================================ #


def add_filters():

    """
        Create collection for menu items and mega filter
    """

    with open('db.json') as db_file:
        data = json.load(db_file)

        cuina = []
        planning = []
        dificultat = []
        estat d'ànim = []
        plat = []
        al·lèrgens = []

        # Iterate over Recipes
        for i in data['recipes']:

            # cuina
            if not i['filters']['cuina'] in cuina:
                if not i['filters']['cuina'] == '':
                    cuina.append(i['filters']['cuina'])

            # planning
            if not i['filters']['planning'] in planning:
                if not i['filters']['planning'] == '':
                    planning.append(i['filters']['planning'])

            # dificultat
            if not i['filters']['dificultat'] in dificultat:
                if not i['filters']['dificultat'] == '':
                    dificultat.append(i['filters']['dificultat'])

            # estat d'ànim
            if not i['filters']['estat d'ànim'] in estat d'ànim:
                if not i['filters']['estat d'ànim'] == '':
                    estat d'ànim.append(i['filters']['estat d'ànim'])

            # al·lèrgens
            if not i['filters']['al·lèrgens'] in al·lèrgens:
                if not i['filters']['al·lèrgens'] == '':
                    al·lèrgens.append(i['filters']['al·lèrgens'])

            # plat
            for plats in i['filters']['plat']:
                if plats not in plat:
                    if not plats == '':
                        plat.append(plats)

        # insert document into mongo collection - filters
        filters.insert_one({
            "cuina": cuina,
            "plat": plat,
            "planning": planning,
            "estat d'ànim": mood,
            "al·lèrgens": al·lèrgens,
            "dificultat": dificultat
        })


# ============================================ #


""" 
    Run file
"""

add_recipes()
add_user()
add_filters()