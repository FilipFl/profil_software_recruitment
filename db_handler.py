from peewee import *
from datetime import *
import re


class Password(Model):
    password = CharField()
    evaluation = IntegerField()

    class Meta:
        database = SqliteDatabase('recruitment_db.db')


class Person(Model):
    person_id = AutoField()
    gender = CharField()
    email = CharField()
    phone = CharField()
    cell = CharField()
    nat = CharField()
    daysleft = IntegerField()

    class Meta:
        database = SqliteDatabase('recruitment_db.db')


class Location(Model):
    city = CharField()
    state = CharField()
    country = CharField()
    postcode = IntegerField()
    person = ForeignKeyField(Person, backref='location')

    class Meta:
        database = SqliteDatabase('recruitment_db.db')


class Idcolumn(Model):
    name = CharField()
    value = CharField()
    person = ForeignKeyField(Person, backref='idcolumn')

    class Meta:
        database = SqliteDatabase('recruitment_db.db')


class Registered(Model):
    date = DateField()
    age = IntegerField()
    person = ForeignKeyField(Person, backref='registered')

    class Meta:
        database = SqliteDatabase('recruitment_db.db')


class Dob(Model):
    date = DateField()
    age = IntegerField()
    person = ForeignKeyField(Person, backref='dob')

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
    person = ForeignKeyField(Person, backref='login')

    class Meta:
        database = SqliteDatabase('recruitment_db.db')


class Timezone(Model):
    offset = CharField()
    description = CharField()
    location = ForeignKeyField(Location, backref='timezone' )

    class Meta:
        database = SqliteDatabase('recruitment_db.db')


class Coordinates(Model):
    latitude = CharField()
    longitude = CharField()
    location = ForeignKeyField(Location, backref='coordinates')

    class Meta:
        database = SqliteDatabase('recruitment_db.db')


class Street(Model):
    number = IntegerField()
    name = CharField()
    location = ForeignKeyField(Location, backref='street')

    class Meta:
        database = SqliteDatabase('recruitment_db.db')


class Name(Model):
    title = CharField()
    first = CharField()
    last = CharField()
    person = ForeignKeyField(Person, backref='name')

    class Meta:
        database = SqliteDatabase('recruitment_db.db')



class DBHandler:

    def __init__(self):
        self.db = SqliteDatabase('recruitment_db.db')
        self.db.connect()
        self.special_check = re.compile('[@_!#$%^&*()<>?/\|}{~:]')


    def initialize_database(self, data):
        self.db.create_tables([Person, Name, Location, Street, Coordinates, Timezone, Login, Dob, Registered, Idcolumn])
        i = 0
        with self.db.atomic():
            for record in data['results']:
                print(i)
                person_inst = Person.create(gender=record['gender'], email=record['email'], phone=record['phone'], cell=record['cell'],
                                                                                        nat=record['nat'], daysleft=record['daysleft'])
                location_inst = Location.create(city=record['location']['city'], state=record['location']['state'],
                                                country=record['location']['country'], postcode=record['location']['postcode'], person=person_inst)
                Street.create(number=record['location']['street']['number'], name=record['location']['street']['name'], location=location_inst)
                Coordinates.create(latitude=record['location']['coordinates']['latitude'],
                                                longitude=record['location']['coordinates'], location=location_inst)
                Timezone.create(offset=record['location']['timezone']['offset'],
                                                description=record['location']['timezone']['description'],
                                                location=location_inst)
                Name.create(title=record['name']['title'], first=record['name']['first'], last=record['name']['last'], person=person_inst)
                Login.create(uuid=record['login']['uuid'], username=record['login']['username'], password=record['login']['password'],
                                          salt=record['login']['salt'], md5=record['login']['md5'],sha1=record['login']['sha1'],
                                          sha256=record['login']['sha256'], person=person_inst)
                Dob.create(date=self.parse_date(record['dob']['date']), age=record['dob']['age'], person=person_inst)
                Registered.create(date=self.parse_date(record['registered']['date']), age=record['registered']['age'], person=person_inst)
                if record['id']['value'] is not None:
                    Idcolumn.create(name=record['id']['name'], value=record['id']['value'], person=person_inst)
                else:
                    Idcolumn.create(name='', value='', person=person_inst)
                i += 1

    def get_percentage(self):
        query = Person.select(fn.COUNT()).where(Person.gender == "female")
        females = query.scalar()
        all = Person.select(fn.COUNT()).scalar()
        msg = "Percentage of male: {:.3%} \n Percentage of female: {:.3%}".format((all-females)/all, females/all)
        print(msg)

    def get_average_age(self, flag):
        if flag == "general":
            query = Dob.select(fn.AVG(Dob.age * 1.0))
            value = query.scalar()
            description = "in general"
        elif flag == "male":
            query = Dob.select(fn.AVG(Dob.age * 1.0)).join(Person).where(Person.gender == 'male')
            value = query.scalar()
            description = "of men"
        elif flag == "female":
            query = Dob.select(fn.AVG(Dob.age* 1.0)).join(Person).where(Person.gender == 'female')
            value = query.scalar()
            description = "of women"
        msg = "Average age {} is {:.2f} years old.".format(description, value)
        print(msg)

    def get_common(self, amount, get_what):
        if get_what == "city":
            query = Location.select(Location.city, fn.Count(Location.city).alias('quantity')).group_by(Location.city).order_by(fn.Count(Location.city).desc())
            print('Most common {} cities.'.format(amount))
        elif get_what == "password":
            query = Login.select(Login.password, fn.Count(Login.password).alias('quantity')).group_by(
                Login.password).order_by(fn.Count(Login.password).desc())
            print('Most common {} passwords.'.format(amount))
        for index, element in enumerate(query):
            if index > amount-1:
                break
            if get_what == "city":
                print(element.city, element.quantity)
            else:
                print(element.password, element.quantity)

    def get_best_password(self):
        query = Login.select()
        best = ['', 0]
        for login in query:
            password_str = login.password
            val = self.evaluate_password(password_str)
            if val > best[1]:
                best = [password_str, val]
        print("The best password is \"{}\" with score {}".format(best[0], best[1]))

    def evaluate_password(self, password):
        flags = [0 for i in range(5)]
        if len(password) >= 8:
            flags[3] = 5
        if self.special_check.search(password) is not None:
            flags[4] = 3
        for c in password:
            if c.islower():
                flags[0] = 1
            elif c.isupper():
                flags[1] = 2
            elif c.isdigit():
                flags[2] = 1
        return sum(flags)

    def parse_date(self, date_str):
        date_str = date_str.split("T")
        date_str = date_str[0].split("-")
        return date(int(date_str[0]), int(date_str[1]), int(date_str[2]))

    def get_between(self, start, end):
        datetime_object = datetime.now()
        print(datetime_object)
        query = Person.select(Person.person_id, Name.first, Name.last).join(Name).switch(Person).join(Dob).where(Dob.date.between(start, end))
        print(query)
        for element in query:
            print(element.name.first, element.name.last, element.person_id)




