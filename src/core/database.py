import discord
from peewee import *

from config import *

db = MySQLDatabase(
    mysql_db_name,
    user = mysql_db_username,
    password = mysql_db_password,
    host = db_host,
    port = db_port
)

# Connects to the MySQL database
def open_db():
    db.connect()

# Closes MySQL database connection
def close_db():
    db.close()

def create_db_tables():
    # create_tables() does safe creation by default, and will simply not create
    # table if it already exists
    db.create_tables([User, Meme, Advice, Trump, Kek])

def add_admin(user):
    if Admin.get_or_none(Admin.discord_id == user.id) == None:
        new_admin = Admin.create(discord_id=user.id)
        new_admin.save()

# TODO check if this function looks okay later
def add_kek(discord_user, submission):
    new_kek = Kek.create(added_by_id=discord_user.id, quote=submission)
    new_kek.save()

def get_user_model(discord_user):
    return User.get_or_none(User.discord_id == discord_user.id)

def does_user_exist(discord_user):
    return not User.get_or_none(User.discord_id == discord_user.id) == None

# Returns created User model if successful, else false
def add_user(discord_user, is_admin=False):
    if not does_user_exist(discord_user):
        new_user = User.create(discord_id=discord_user.id, is_admin=is_admin)
        new_user.save()
        return new_user
    return False

def make_admin(discord_user):
    new_admin = get_user_model(discord_user)
    if new_admin == None:
        add_user(discord_user, is_admin=True)
    else:
        q = User.update({User.is_admin: True}).where(User.discord_id == discord_user.id)
        q.execute()

# TODO temporary function for debug, delete later
def remove_admin(discord_user):
    demoted_user = get_user_model(discord_user)
    if not demoted_user == None:
        q = User.update({User.is_admin: False}).where(User.discord_id == discord_user.id)
        q.execute()

def is_admin(discord_user):
    model = get_user_model(discord_user)
    return model.is_admin

class User(Model):
    discord_id = CharField()
    is_admin = BooleanField(default=False)
    class Meta:
        database = db

class Meme(Model):
    added_by_id = CharField()
    img_url = CharField()
    class Meta:
        database = db

class Advice(Model):
    added_by_id = CharField()
    advice = CharField()
    class Meta:
        database = db

class Trump(Model):
    added_by_id = CharField()
    quote = CharField()
    class Meta:
        database = db

class Kek(Model):
    # TODO maybe instead of added_by_id, join with a User object
    added_by_id = CharField()
    quote = CharField()
    class Meta:
        database = db
