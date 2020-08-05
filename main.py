import json
from datetime import date
import calendar
from db_handler import *
import argparse
import sqlite3
import requests

class JsonParser:

    def __init__(self):
        self.data = None

    def load_from_api(self, api_response):
        self.data = api_response
        self.parse_phone_number()
        self.delete_picture()
        self.days_to_bd()

    def load_from_file(self):
        self.read_file()
        self.parse_phone_number()
        self.delete_picture()
        self.days_to_bd()

    def read_file(self):
        file = open('persons.json', encoding="utf8")
        self.data = json.loads(file.read())

    def parse_phone_number(self):
        for record in self.data['results']:
            for character in record['phone']:
                if not character.isdecimal():
                    record['phone'] = record['phone'].replace(character, '')
            for character in record['cell']:
                if not character.isdecimal():
                    record['cell'] = record['cell'].replace(character, '')

    def delete_picture(self):
        for record in self.data['results']:
            record.pop('picture')

    def days_to_bd(self):
        today = date.today()
        for record in self.data['results']:
            birthday_date = record['dob']['date']
            days_remaining = self.calculate_days(today, birthday_date)
            record['daysleft'] = days_remaining

    def calculate_days(self, today, date_str):
        bdday = date_str.split('T')
        bdday = bdday[0].split('-')
        birthday = date(today.year, int(bdday[1]), int(bdday[2]))
        delta = birthday - today
        if delta.days < 0:
            if int(bdday[1]) == 2 and int(bdday[2]) == 29:
                add = 1
                while not calendar.isleap(today.year + add):
                    add += 1
                birthday = date(today.year + add, int(bdday[1]), int(bdday[2]))
            else:
                birthday = date(today.year + 1, int(bdday[1]), int(bdday[2]))
            delta = birthday - today
        return delta.days

    def get_data(self):
        return self.data

    def create_my_func(self, func):
        self.con = sqlite3.connect('recruitment_db.db')
        self.con.create_function("evaluate_password", 1, func)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--percentage", help="Get percentage of women and men", action="store_true")
    parser.add_argument("--init", help="Initialize database", action="store_true")
    parser.add_argument("--average_age", type=str, help="Get average age (general, female, male)",
                        choices=['general','female','male'])
    parser.add_argument("--most_common_cities", type=int, help="Get N most common cities")
    parser.add_argument("--most_common_passwords", type=int, help="Get N most common passwords")
    parser.add_argument("--best_password", help="Get the best password", action='store_true')
    parser.add_argument("--born_between", type=str, help="Get people born between dates (Use format \"YYYY-MM-DD:YYYY-MM-DD\"")
    parser.add_argument("--load_from_api", type=int,help="Get data from API into database")
    parser.add_argument("--how_many", help="Get amount of records", action='store_true')
    parser.add_argument("--api_init", help="Initialize db with api response")
    args = parser.parse_args()
    pars = JsonParser()
    handle = DBHandler()
    if args.init:
        pars.load_from_file()
        handle.dump_into_database(pars.get_data())
    if args.percentage:
        handle.get_percentage()
    if args.average_age:
        handle.get_average_age(args.average_age)
    if args.most_common_cities:
        if args.most_common_cities < 1:
            msg = "Wrong argument"
            raise argparse.ArgumentTypeError(msg)
        handle.get_common(args.most_common_cities, 'city')
    if args.most_common_passwords:
        if args.most_common_passwords < 1:
            msg = "Wrong argument"
            raise argparse.ArgumentTypeError(msg)
        handle.get_common(args.most_common_passwords, 'password')
    if args.best_password:
        handle.get_best_password()
    if args.born_between:
        my_string = args.born_between
        my_string = my_string.replace(':', '-')
        my_string = my_string.split("-")
        print(my_string)
        try:
            start = date(int(my_string[0]), int(my_string[1]), int(my_string[2]))
            end = date(int(my_string[3]), int(my_string[4]), int(my_string[5]))
        except ValueError:
            msg = "Wrong argument, try \"YYYY-MM-DD:YYYY-MM-DD\" format"
            raise argparse.ArgumentTypeError(msg)
        handle.get_between(start, end)
    if args.load_from_api:
        if args.load_from_api < 1:
            msg = "Wrong argument"
            raise argparse.ArgumentTypeError(msg)
        else:
            response = requests.get('https://randomuser.me/api/?results={}'.format(args.load_from_api))
            if not response:
                print('An error has occured.')
            elif "error" in response.json():
                print(response.json()['error'])
            else:
                pars.load_from_api(response.json())
                if args.api_init:
                    handle.dump_into_database(pars.get_data())
                else:
                    handle.dump_into_database(pars.get_data(), False)
    if args.how_many:
        handle.get_how_many()







