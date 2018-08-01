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
    db.create_tables([Admin, Meme, Advice, Trump, Kek])

def add_admin(user):
    if Admin.get_or_none(Admin.discord_id == user.id) == None:
        new_admin = Admin.create(discord_id=user.id)
        new_admin.save()

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

# def test_function():
#     db.connect()
#     if not db.table_exists("feet"):
#         print("no feet")
#     if User.table_exists():
#         print("gaspu")
#     if not User.table_exists():
#         User.create_table()
#         print("created table")
#     db.close()
