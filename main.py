import json
from datetime import date
import calendar
from db_handler import *
import argparse


class JsonParser:

    def __init__(self):
        self.data = None
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--percentage", help="Get percentage of women and men", action="store_true")
    parser.add_argument("--init", help="Initialize database", action="store_true")
    parser.add_argument("--average_age", type=str, help="Get average age (general, female, male)",
                        choices=['general','female','male'])
    parser.add_argument("--most_common_cities", type=int, help="Get N most common cities")
    parser.add_argument("--most_common_passwords", type=int, help="Get N most common passwords")
    pars = JsonParser()
    handle = DBHandler()
    args = parser.parse_args()
    if args.init:
        handle.initialize_database(pars.get_data())
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





