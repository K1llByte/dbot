import json
from _thread import start_new_thread

import time
from control.logs import info_log


from control.model.memes import Memes
from control.model.users import Users
from control.model.warframe import Warframe
from control.model.crypto import Crypto

###############################################

async def add_list(filename, ctx, key, tag, value):
    torf = False
    data_string = load_data(filename)

    for word in data_string[key].keys():
        if word.lower() == tag.lower():
            torf = True

    if torf == False:
        data_string[key][tag] = value
        save_data(filename, data_string)
        await ctx.send(str(tag).title() + ' adicionado com sucesso')
    else:
        await ctx.send('Tag já existe')

###############################################

def load_data(filename):    
    with open(filename,'r') as file:
        return json.load(file)


def save_data(filename, data):
    with open(filename,'w') as file:
        json.dump(data,file, sort_keys=False, indent=4)


###############################################

class Data:

    def __init__(self):
        self.memes_data    = load_data('data/memes.json')
        self.users_data    = load_data('data/users.json')
        self.warframe_data = load_data('data/warframe.json')
        self.crypto_data = load_data('data/crypto.json')

        self.memes = Memes(self.memes_data)
        self.users = Users(self.users_data)
        self.warframe = Warframe(self.warframe_data)
        self.crypto = Crypto(self.crypto_data)

        start_new_thread(self.autosaver, ())
    
    def save(self):
        save_data('data/memes.json', self.memes_data)
        save_data('data/users.json', self.users_data)
        save_data('data/warframe.json', self.warframe_data)
        save_data('data/crypto.json', self.crypto_data)


    def autosaver(self):
        while True:
            time.sleep(60*5) #60*5
            self.save()
            print( info_log('Saved data') )