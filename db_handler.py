import sqlite3
from peewee import *


class Idcolumn(Model):
    name = CharField()
    value = CharField()

    class Meta:
        database = SqliteDatabase('recruitment_db.db')


class Registered(Model):
    date = CharField()
    age = IntegerField()

    class Meta:
        database = SqliteDatabase('recruitment_db.db')


class Dob(Model):
    date = CharField()
    age = IntegerField()

    class Meta:
        database = SqliteDatabase('recruitment_db.db')


class Login(Model):
    uuid = CharField()
    username = CharField()
    password = CharField()
    salt = CharField()
    md5 = CharField()
    sha1 = CharField()
    sha256 = CharField()

    class Meta:
        database = SqliteDatabase('recruitment_db.db')


class Timezone(Model):
    offset = CharField()
    description = CharField()

    class Meta:
        database = SqliteDatabase('recruitment_db.db')


class Coordinates(Model):
    latitude = CharField()
    longitude = CharField()

    class Meta:
        database = SqliteDatabase('recruitment_db.db')


class Street(Model):
    number = IntegerField()
    name = CharField()

    class Meta:
        database = SqliteDatabase('recruitment_db.db')


class Location(Model):
    street = ForeignKeyField(Street, backref='street')
    city = CharField()
    state = CharField()
    country = CharField()
    postcode = IntegerField()
    coordinates = ForeignKeyField(Coordinates, backref='coordinates')
    timezone = ForeignKeyField(Timezone, backref='timezone')

    class Meta:
        database = SqliteDatabase('recruitment_db.db')


class Name(Model):
    title = CharField()
    first = CharField()
    last = CharField()

    class Meta:
        database = SqliteDatabase('recruitment_db.db')


class Person(Model):
    person_id = AutoField()
    gender = CharField()
    name = ForeignKeyField(Name, backref='name')
    location = ForeignKeyField(Location, backref='location')
    email = CharField()
    login = ForeignKeyField(Login, backref='login')
    dob = ForeignKeyField(Dob, backref='dob')
    registered = ForeignKeyField(Registered, backref='registered')
    phone = CharField()
    cell = CharField()
    id = ForeignKeyField(Idcolumn, backref='idcolumn')
    nat = CharField()
    daysleft = IntegerField()

    class Meta:
        database = SqliteDatabase('recruitment_db.db')


class DBHandler:

    def __init__(self, data):
        self.db = SqliteDatabase('recruitment_db.db')
        self.db.connect()
        self.initialize_database(data)

    def initialize_database(self, data):
        self.db.create_tables([Person, Name, Location, Street, Coordinates, Timezone, Login, Dob, Registered, Idcolumn])
        i = 0
        for record in data['results']:
            print(i)
            print(record)
            if record['id']['value'] is not None:
                id_inst = Idcolumn.create(name=record['id']['name'], value=record['id']['value'])
            else:
                id_inst = Idcolumn.create(name='', value='')
            name_inst = Name.create(title=record['name']['title'], first=record['name']['first'], last=record['name']['last'])
            street_inst = Street.create(number=record['location']['street']['number'], name=record['location']['street']['name'])
            coord_inst = Coordinates.create(latitude=record['location']['coordinates']['latitude'], longitude=record['location']['coordinates'])
            timezone_inst = Timezone.create(offset=record['location']['timezone']['offset'], description=record['location']['timezone']['description'])
            login_inst = Login.create(uuid=record['login']['uuid'], username=record['login']['username'], password=record['login']['password'],
                                      salt=record['login']['salt'], md5=record['login']['md5'],sha1=record['login']['sha1'],
                                      sha256=record['login']['sha256'])
            dob_inst = Dob.create(date=record['dob']['date'], age=record['dob']['age'])
            reg_inst = Registered.create(date=record['registered']['date'], age=record['registered']['age'])
            location_inst = Location.create(street=street_inst, city=record['location']['city'], state=record['location']['state'],
                                            country=record['location']['country'], postcode=record['location']['postcode'],
                                            coordinates=coord_inst, timezone=timezone_inst)
            Person.create(gender=record['gender'], name=name_inst, location=location_inst, email=record['email'],
                         login=login_inst, dob=dob_inst, registered=reg_inst, phone=record['phone'], cell=record['cell'],
                         id=id_inst, nat=record['nat'], daysleft=record['daysleft'])
            i += 1

    def get_sth(self):
        person = Person.select().where(Person.email == 'louane.vidal@example.com').get()
        return person.name.first


