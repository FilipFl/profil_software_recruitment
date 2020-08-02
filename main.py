import json


class Task:

    def __init__(self):
        self.data = None
        self.read_file()
        self.parse_phone_number()
        self.delete_picture()

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


if __name__ == '__main__':
    task = Task()






