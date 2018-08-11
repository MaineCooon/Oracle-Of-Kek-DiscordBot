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
    db.create_tables([User, Admin, Meme, Advice, Trump, Kek])

def add_admin(user):
    if Admin.get_or_none(Admin.discord_id == user.id) == None:
        new_admin = Admin.create(discord_id=user.id)
        new_admin.save()

def get_user(user):
    return User.get_or_none(User.discord_id == user.id)

def does_user_exist(user):
    return not User.get_or_none(User.discord_id == user.id) == None

# Returns created User model if successful, else false
def add_user(user, is_admin=False):
    if not does_user_exist(user):
        new_user = User.create(discord_id=user.id, is_admin=is_admin)
        new_user.save()
        return new_user
    return False

def make_admin(user):
    new_admin = get_user(user)
    if new_admin == None:
        add_user(user, is_admin=True)
    else:
        q = User.update({User.is_admin: True}).where(User.discord_id == user.id)
        q.execute()

class User(Model):
    discord_id = CharField()
    is_admin = BooleanField(default=False)
    class Meta:
        database = db

# Stores Discord IDs of admins so they can be remembered as well as
# easily added/removed
class Admin(Model):
    discord_id = CharField()
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
    added_by_id = CharField()
    quote = CharField()
    class Meta:
        database = db
