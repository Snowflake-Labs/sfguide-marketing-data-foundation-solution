import os
import json
import glob
from datetime import datetime

supported_format = ['json']
translations_folder = '../locales/'

class Translator():
    _instance = None

    def __new__(class_, *args, **kwargs):
        # singleton definition
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__(self, file_format='json', default_locale='en'):
        self.data = {}
        self.locale = default_locale

        # validate format is supported
        if file_format in supported_format:
            self.load_data(file_format)
        else:
            # TODO handle error
            print(f'Invalid file format, should be any of {supported_format}')
        
    def load_data(self, file_format):
        abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), translations_folder))
        files = glob.glob(os.path.join(abs_path, f'*.{file_format}'))
        for f in files:
            # get the name of the file without extension, will be used as locale name
            loc = os.path.splitext(os.path.basename(f))[0]
            with open(f, 'r', encoding='utf8') as f:
                if file_format == 'json':
                    self.data[loc] = json.load(f)

    def translate(self, key):
        # returns the key instead if key is not found
        if self.locale not in self.data:
            # TODO handle error
            return key

        text = self.data[self.locale].get(key, key)
        return text

    def set_locale(self, loc):
        if loc in self.data:
            self.locale = loc
        else:
            # TODO handle error
            print('Invalid locale')

    def get_locale(self):
        return self.locale
