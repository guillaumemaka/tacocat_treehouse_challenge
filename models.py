from peewee import *
from flask.ext.bcrypt import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

DATABASE = SqliteDatabase("peewee.db")


class User(UserMixin, Model):
    email = CharField(unique=True)
    password = CharField()

    @classmethod
    def create_user(cls, email, password):
        try:
            cls.create(
                email=email,
                password=generate_password_hash(password)
            )
        except IntegrityError:
            raise ValueError

    class Meta:
        database = DATABASE
    
    
class Taco(Model):
    protein = CharField()
    shell = CharField()
    cheese = BooleanField()
    extras = TextField()
    user = ForeignKeyField(User)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Taco], safe=True)