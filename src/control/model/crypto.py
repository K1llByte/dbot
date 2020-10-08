import requests

class Crypto:

    def __init__(self, crypto_data_ref):
        self.crypto_data = crypto_data_ref

        res = requests.get('https://api.cryptowat.ch/markets/kraken')
        if res.status_code == 200:
            print('Success')
            self.symbols = []
            for curr in res.json()['result']:
                if curr['pair'].endswith('eur') and curr['active']:
                    self.symbols.append(curr['pair'][:-3])
        else:
            print('No success')
            self.symbols = None
        print(self.symbols)


    def get_user_coins(self, user_id):
        user_id = str(user_id)
        if user_id not in self.crypto_data['cryptocoins']:
            return None
        return UserCoins(self.crypto_data['cryptocoins'][user_id])

    def coin_value(self, symbol):
        res = requests.get('https://api.cryptowat.ch/markets/kraken/{}eur/price'.format(symbol.lower()))
        if res.status_code == 200:
            return res.json()['result']['price']
        else:
            return None

    def create_user_coins(self, user_id:int):
        user_id = str(user_id)
        if user_id not in self.crypto_data['cryptocoins']:
            self.crypto_data['cryptocoins'][user_id] = { }
            return True
        return False

    def is_coin_active(self, symbol):
        return symbol in self.symbols


class UserCoins:
    def __init__(self, coins_data_ref):
        self.coins_data = coins_data_ref

    def get_owned(self, symbol):
        if symbol not in self.coins_data:
            return None
        return self.coins_data[symbol]['quantity']

    def data(self):
        return self.coins_data

    def add(self, symbol, qnt):
        if symbol not in self.coins_data:
            self.coins_data[symbol] = {
                'quantity' : qnt
            }
        else:
            self.coins_data[symbol]['quantity'] += qnt
    
    def remove(self, symbol, qnt):
        if symbol in self.coins_data and self.coins_data[symbol]['quantity'] >= qnt:
            self.coins_data[symbol]['quantity'] -= qnt
            if self.coins_data[symbol]['quantity'] == 0:
                del self.coins_data[symbol]
            return True
        else:
            return False