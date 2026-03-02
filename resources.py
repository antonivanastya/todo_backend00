import json
import os


def print_with_indent(value, indent=0):
    indentation = '\t' * indent
    print(f'{indentation}{value}')

class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent=indent + 1)

    @classmethod
    def from_json(cls, value: dict):
        new_entry = cls(value['title'])
        for sub_entry in value.get('entries', []):
            new_entry.add_entry(cls.from_json(sub_entry))
        return new_entry

    def __str__(self):
        return self.title

    def json(self):
        res = {
            'title': self.title,
            'entries': [entry.json() for entry in self.entries]
        }
        return res

    def save(self, path):
        filename = f"{self.title}.json"
        full_path = os.path.join(path, filename)
        with open(full_path, 'w') as f:
            json.dump(self.json(), f)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            return cls.from_json(data)

from typing import List
import os


class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries: List[Entry] = []

    def load(self):
        for filename in os.listdir(self.data_path):
            if filename.endswith('.json'):
                full_path = os.path.join(self.data_path, filename)
                entry = Entry.load(full_path)
                self.entries.append(entry)

    def add_entry(self, title: str):
        self.entries.append(Entry(title))

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)


category = Entry('Еда')

category.add_entry(Entry('Морковь'))
category.add_entry(Entry('Капуста'))

category.json()

grocery_list = {
    "title": "Продукты",
    "entries": [
        {
            "title": "Молочные",
            "entries": [
                {
                    "title": "Йогурт",
                    "entries": []
                },
                {
                    "title": "Сыр",
                    "entries": []
                }
            ]
        }
    ]
}