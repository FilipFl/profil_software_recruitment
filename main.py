import json
import datetime


class Task:

    def __init__(self):
        self.data = None
        self.read_file()
        self.parse_phone_number()

    def read_file(self):
        file = open('persons.json', encoding="utf8")
        self.data = json.loads(file.read())


    def parse_phone_number(self):
        for element in self.data['results']:
            for character in element['phone']:
                if not character.isdecimal():
                    element['phone'] = element['phone'].replace(character, '')
            for character in element['cell']:
                if not character.isdecimal():
                    element['cell'] = element['cell'].replace(character, '')



if __name__ == '__main__':
    task = Task()






