import json
import random


# adds a new user to the database
def add_user(username):
    if username not in user_json['users']:
        user_json['users'][username] = {}
    save_json()


# adds a new profile_image to a user in the database
def add_profile_image(username, image_path):
    if username in user_json['users']:
        user_json['users'][username]["profile_image"] = image_path
    else:
        add_user(username)
        add_profile_image(username, image_path)
    save_json()


# adds verified to a user
def add_verified(username, verified):
    if username in user_json['users']:
        user_json['users'][username]["verified"] = verified
    else:
        add_user(username)
        add_verified(username, verified)
    save_json()


# adds verified to a user
def add_verified(username, verified):
    if username in user_json['users']:
        user_json['users'][username]["verified"] = verified
    else:
        add_user(username)
        add_verified(username, verified)
    save_json()


# adds subscriber to a user
def add_subscriber(username, subscriber):
    if username in user_json['users']:
        user_json['users'][username]["subscriber"] = subscriber
    else:
        add_user(username)
        add_subscriber(username, subscriber)
    save_json()


# adds subscriber to a user
def add_post_amount(username, post_amount):
    if username in user_json['users']:
        user_json['users'][username]["post_amount"] = post_amount
    else:
        add_user(username)
        add_post_amount(username, post_amount)
    save_json()


# adds subscribed_to to a user
def add_subscribed_to(username, subscriber):
    if username in user_json['users']:
        user_json['users'][username]["subscribed_to"] = subscriber
    else:
        add_user(username)
        add_subscribed_to(username, subscriber)
    save_json()


# adds subscribed_to to a user
def add_is_private(username, private):
    if username in user_json['users']:
        user_json['users'][username]["private"] = private
    else:
        add_user(username)
        add_is_private(username, private)
    save_json()


# adds bio_info to a user
def add_bio_info(username, info):
    if username in user_json['users']:
        user_json['users'][username]["bio_info"] = info
    else:
        add_user(username)
        add_bio_info(username, info)
    save_json()


# adds bio_info to a user
def add_gender_guess(username, gender):
    if username in user_json['users']:
        user_json['users'][username]["gender_guess"] = gender
    else:
        add_user(username)
        add_gender_guess(username, gender)
    save_json()


# adds list to accounts todo
def add_list_to_todo(user_list):
    for username in user_list:
        if username not in user_json['todo'] and username not in user_json['users']:
            user_json['todo'].append(username)
    save_json()


# removes user from todo
def remove_from_todo(username):
    if username in user_json['todo']:
        user_json['todo'].remove(username)
    save_json()


# gets random element from todo and removes it
def get_next_todo_and_remove():
    if len(user_json['todo']) > 0:
        idx = random.randint(0, len(user_json['todo']) - 1)
        username = user_json['todo'][idx]
        remove_from_todo(username)
        return username
    else:
        return None


# returns if a user already is in the database (not todo)
def user_in_database(username):
    return username in user_json['users']


# returns the amount of users in the database
def get_user_amount():
    return len(user_json['users'])


# saves the file
def save_json():
    f.seek(0)
    json.dump(user_json, f, indent=4)
    f.truncate()


f = open("./userinfo.json", 'r+')
user_json = json.load(f)