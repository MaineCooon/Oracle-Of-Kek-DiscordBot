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
    db.create_tables([User, Server, Meme, Gif, Advice, Trump, Kek])

def add_admin(user):
    if Admin.get_or_none(Admin.discord_id == user.id) == None:
        new_admin = Admin.create(discord_id=user.id)
        new_admin.save()

def get_user_model(discord_user):
    return User.get_or_none(User.discord_id == discord_user.id)

def get_server_model(discord_server):
    return Server.get_or_none(Server.server_id == discord_server.id)

def does_user_exist(discord_user):
    return not User.get_or_none(User.discord_id == discord_user.id) == None

def does_server_exist(discord_server):
    return not Server.get_or_none(Server.server_id == discord_server.id) == None

# Returns created User model if successful, else false
def add_user(discord_user, is_admin=False):
    if not does_user_exist(discord_user):
        new_user = User.create(discord_id=discord_user.id, is_admin=is_admin)
        new_user.save()
        return new_user
    return False

# Returns created Server model if successful, else false
def add_server(discord_server, welcome_channel_id=None):
    if not does_server_exist(discord_server):
        new_server = Server.create(server_id=discord_server.id, welcome_channel_id=welcome_channel_id)
        new_server.save()
        return new_server
    return False

def set_welcome_channel(channel):
    server_model = get_server_model(channel.server)
    if server_model == None:
        add_server(channel.server, welcome_channel_id = channel.id)
    else:
        q = Server.update({Server.welcome_channel_id: channel.id}).where(Server.server_id == channel.server.id)
        q.execute()

    # if does_server_exist(channel.server):
    #
    #
    #     def make_admin(discord_user):
    #         new_admin = get_user_model(discord_user)
    #         if new_admin == None:
    #             add_user(discord_user, is_admin=True)
    #         else:
    #             q = User.update({User.is_admin: True}).where(User.discord_id == discord_user.id)
    #             q.execute()

def add_meme(discord_user, img_url):
    new_meme = Meme.create(added_by_id=discord_user.id, img_url=img_url)
    new_meme.save()
    return new_meme

def add_gif(discord_user, img_url):
    new_gif = Gif.create(added_by_id=discord_user.id, img_url=img_url)
    new_gif.save()
    return new_gif

def add_kek(discord_user, submission):
    new_kek = Kek.create(added_by_id=discord_user.id, submission=submission)
    new_kek.save()
    return new_kek

def add_trump(discord_user, submission):
    new_trump = Trump.create(added_by_id=discord_user.id, submission=submission)
    new_trump.save()
    return new_trump

def add_advice(discord_user, submission):
    new_advice = Advice.create(added_by_id=discord_user.id, submission=submission)
    new_advice.save()
    return new_advice

def get_memes():
    return Meme.select()

def get_keks():
    return Kek.select()

def get_gifs():
    return Gif.select()

def get_trumps():
    return Trump.select()

def get_advices():
    return Advice.select()

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
    return False if model == None else model.is_admin

class User(Model):
    discord_id = CharField()
    is_admin = BooleanField(default=False)
    deposit_address = CharField(null=True)
    class Meta:
        database = db

class Server(Model):
    server_id = CharField()
    welcome_channel_id = CharField(null=True)
    class Meta:
        database = db

class Meme(Model):
    added_by_id = CharField()
    img_url = CharField()
    class Meta:
        database = db

class Gif(Model):
    added_by_id = CharField()
    img_url = CharField()
    class Meta:
        database = db

class Advice(Model):
    added_by_id = CharField()
    submission = CharField()
    class Meta:
        database = db

class Trump(Model):
    added_by_id = CharField()
    submission = CharField()
    class Meta:
        database = db

class Kek(Model):
    # TODO maybe instead of added_by_id, join with a User object
    added_by_id = CharField()
    submission = CharField()
    class Meta:
        database = db
