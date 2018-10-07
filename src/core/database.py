import datetime
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

################################################################################
##### General database functions ###############################################

# Connects to the MySQL database
def open_db():
    db.connect()

# Closes MySQL database connection
def close_db():
    db.close()

def create_db_tables():
    # create_tables() does safe creation by default, and will simply not create
    # table if it already exists
    db.create_tables([User, Server, Tip, Advice, Gif, Kek, Meme, Trump])
    print("Database tables prepared")


################################################################################
##### User model related functions #############################################

def get_users():
    return User.select()

def get_user_model(discord_user):
    return User.get_or_none(User.discord_id == discord_user.id)

def get_or_make_user_model(discord_user):
    res = User.get_or_none(User.discord_id == discord_user.id)
    if res == None:
        return add_user(discord_user)
    return res

# Returns created User model if successful, else false
def add_user(discord_user, is_admin=False, deposit_address=None):
    if not does_user_exist(discord_user):
        new_user = User.create(discord_id=discord_user.id, is_admin=is_admin, deposit_address=deposit_address)
        new_user.save()
        return new_user
    return False

def does_user_exist(discord_user):
    return not User.get_or_none(User.discord_id == discord_user.id) == None

def bot_has_admin():
    users = get_users()
    for u in users:
        if u.is_admin == True:
            return True
    return False

def add_admin(user):
    if Admin.get_or_none(Admin.discord_id == user.id) == None:
        new_admin = Admin.create(discord_id=user.id)
        new_admin.save()

def make_admin(discord_user):
    new_admin = get_user_model(discord_user)
    if new_admin == None:
        add_user(discord_user, is_admin=True)
    else:
        q = User.update({User.is_admin: True}).where(User.discord_id == discord_user.id)
        q.execute()

def is_admin(discord_user):
    model = get_user_model(discord_user)
    return False if model == None else model.is_admin

# Returns the deposit address registered for the given user.  If user does not
#    have a deposit address registered, returns False
def get_deposit_address(discord_user):
    model = get_user_model(discord_user)
    if model != None:
        if model.deposit_address != None:
            return model.deposit_address
    return False

def set_deposit_address(discord_user, deposit_address):
    user_model = get_user_model(discord_user)
    if user_model == None:
        add_user(discord_user, deposit_address=deposit_address)
    else:
        q = User.update({User.deposit_address: deposit_address}).where(User.discord_id == user_model.discord_id)
        q.execute()

def has_tip_account(discord_user):
    model = get_user_model(discord_user)
    return False if model == None else model.deposit_address != None


################################################################################
##### Server model related functions ###########################################

def get_server_model(discord_server):
    return Server.get_or_none(Server.server_id == discord_server.id)

def get_or_make_server_model(discord_server):
    res = Server.get_or_none(Server.server_id == discord_server.id)
    if res == None:
        return add_server(discord_server)
    return res

# Returns created Server model if successful, else false
def add_server(discord_server, welcome_channel_id=None, poll_channel_id=None):
    if not does_server_exist(discord_server):
        new_server = Server.create(
            server_id=discord_server.id,
            welcome_channel_id=welcome_channel_id,
            poll_channel_id=poll_channel_id
        )
        new_server.save()
        return new_server
    return False

def does_server_exist(discord_server):
    return not Server.get_or_none(Server.server_id == discord_server.id) == None

def set_welcome_channel(channel):
    server_model = get_server_model(channel.server)
    if server_model == None:
        add_server(channel.server, welcome_channel_id = channel.id)
    else:
        q = Server.update({Server.welcome_channel_id: channel.id}).where(Server.server_id == server_model.server_id)
        q.execute()

def set_poll_channel(channel):
    server_model = get_server_model(channel.server)
    if server_model == None:
        add_server(channel.server, poll_channel_id = channel.id)
    else:
        q = Server.update({Server.poll_channel_id: channel.id}).where(Server.server_id == server_model.server_id)
        q.execute()


################################################################################
##### Tip model related commands ###############################################

def add_tip(tipper, receiver, amount):
    tipper_id = tipper.id
    receiver_id = receiver.id
    amount = float(amount)
    new_tip = Tip.create(
        tipper_discord_id=tipper_id,
        receiver_discord_id=receiver_id,
        amount=amount
    )
    new_tip.save()
    return new_tip

def get_tips_by_user(user):
    given = Tip.select().where(Tip.tipper_discord_id == user.id).order_by(-Tip.date_time)
    received = Tip.select().where(Tip.receiver_discord_id == user.id).order_by(-Tip.date_time)
    return {
        'given': given,
        'received': received
    }


################################################################################
##### Advice model related functions ###########################################

def get_advices():
    return Advice.select()

def add_advice(discord_user, submission):
    new_advice = Advice.create(added_by_id=discord_user.id, submission=submission)
    new_advice.save()
    return new_advice


################################################################################
##### Gif model related functions ##############################################

def get_gifs():
    return Gif.select()

def add_gif(discord_user, img_url):
    new_gif = Gif.create(added_by_id=discord_user.id, img_url=img_url)
    new_gif.save()
    return new_gif


################################################################################
##### Kek model related functions ##############################################

def get_keks():
    return Kek.select()

def add_kek(discord_user, submission):
    new_kek = Kek.create(added_by_id=discord_user.id, submission=submission)
    new_kek.save()
    return new_kek


################################################################################
##### Meme model related functions #############################################

def get_memes():
    return Meme.select()

def add_meme(discord_user, img_url):
    new_meme = Meme.create(added_by_id=discord_user.id, img_url=img_url)
    new_meme.save()
    return new_meme


################################################################################
##### Trump model related functions ############################################

def get_trumps():
    return Trump.select()

def add_trump(discord_user, submission):
    new_trump = Trump.create(added_by_id=discord_user.id, submission=submission)
    new_trump.save()
    return new_trump


################################################################################
##### Model classes ############################################################

class User(Model):
    discord_id = CharField()
    is_admin = BooleanField(default=False)
    deposit_address = CharField(null=True)
    class Meta:
        database = db

class Server(Model):
    server_id = CharField()
    welcome_channel_id = CharField(null=True)
    poll_channel_id = CharField(null=True)
    class Meta:
        database = db

class Tip(Model):
    date_time = DateTimeField(default=datetime.datetime.now)
    tipper_discord_id = CharField()
    receiver_discord_id = CharField()
    amount = FloatField()
    class Meta:
        database = db

class Advice(Model):
    added_by_id = CharField()
    submission = CharField()
    class Meta:
        database = db

class Gif(Model):
    added_by_id = CharField()
    img_url = CharField()
    class Meta:
        database = db

class Kek(Model):
    added_by_id = CharField()
    submission = CharField()
    class Meta:
        database = db

class Meme(Model):
    added_by_id = CharField()
    img_url = CharField()
    class Meta:
        database = db

class Trump(Model):
    added_by_id = CharField()
    submission = CharField()
    class Meta:
        database = db
