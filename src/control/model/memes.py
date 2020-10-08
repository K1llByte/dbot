import random

class Memes:

    def __init__(self, memes_data_ref):
        self.memes_data = memes_data_ref

    def get_random(self):
        return self.memes_data['memes'][random.choice(list(self.memes_data['memes']))]

    def get(self, key):
        if key not in self.memes_data['memes']:
            return None
        return self.memes_data['memes'][key]

    def add(self, key, value):
        if key not in self.memes_data['memes']:
            self.memes_data['memes'][key] = value
            return True
        return False

    def delete(self,key):
        if key in self.memes_data['memes']:
            del self.memes_data['memes'][key]
            return True
        return False

    def key_list(self):
        return list(self.memes_data["memes"].keys())