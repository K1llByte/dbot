
class Perms:
    DEFAULT = 0b00000000
    ADMIN   = 0b00000001
    OWNER   = 0b11111111


class Users:

    def __init__(self, users_data_ref):
        self.users_data = users_data_ref

    def get_user(self, user_id:int):
        user_id = str(user_id)
        if user_id in self.users_data['users']:
            return User(self.users_data['users'][user_id])
        return None

    def add_user(self, user_id:int, user):
        user_id = str(user_id)
        if user_id not in self.users_data['users']:
            self.users_data['users'][user_id] = user
            return True
        return False

    def create_user(self, user_id:int, name, permissions=0b0):
        user_id = str(user_id)
        if user_id not in self.users_data['users']:
            self.users_data['users'][user_id] = {
                "name" : name,
                "stats" : { "level":1 , "badges":[], "exp":0, "cash":100 },
                "permissions" : permissions
            }
            return True
        return False
        
        


class User:
    def __init__(self, user_data_ref):
        self.user_data = user_data_ref
    
    ############### Getters ###############
    def name(self):
        return self.user_data['name']

    def stats(self):
        return self.user_data['stats']
        
    def level(self):
        return self.user_data['stats']['level']

    def badges(self):
        return self.user_data['stats']['badges']

    def exp(self):
        return self.user_data['stats']['exp']
    
    def cash(self):
        return self.user_data['stats']['cash']

    def permissions(self):
        return self.user_data['permissions']

    ############### Setters ###############
    def set_name(self, name):
        self.user_data['name'] = name

    def set_stats(self, stats):
        self.user_data['stats'] = stats
        
    def set_level(self, level):
        self.user_data['stats']['level'] = level

    def set_badges(self, badges):
        self.user_data['stats']['badges'] = badges

    def set_exp(self, exp):
        self.user_data['stats']['exp'] = exp
    
    def set_cash(self, cash):
        self.user_data['stats']['cash'] = cash

    def set_permissions(self, permissions):
        self.user_data['permissions'] = permissions

    ############## Modifiers ##############
    def add_xp(self,qnt): # TODO: Refactor this code
        self.user_data['stats']['exp'] += qnt
        while self.user_data['stats']['exp'] >= self.max_exp():
            self.user_data['stats']['exp'] = int(self.user_data['stats']['exp']) - int(self.max_exp())
            self.user_data['stats']['level'] += 1

    def add_badge(self, badge): 
        self.user_data['stats']['badges'].append(badge)

    def add_cash(self, qnt):
        self.user_data['stats']['cash'] += qnt
    #######################################
    
    def has_permissions(self, perms):
        return self.user_data['permissions'] & perms >= perms

    #######################################
    # Maximum current level exp
    def max_exp(self):
        return 100*1.15**(self.user_data['stats']['level']-1)

    # Exp bar string
    def exp_bar(self,n):
        def bar(n, total):
            def repeat(string_to_expand, length):
                return (string_to_expand * (int(length/len(string_to_expand))+1))[:length]

            return (repeat('▓',n) + repeat('░',total-n))

        i = 0
        while self.user_data['stats']['exp'] > i*self.max_exp()/n:
            i+=1
        return bar(i,n)