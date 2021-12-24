import discord
from discord.ext import commands
import json
from control.database import *
from control.model.users import Perms


class Stats(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.bot.users_file = 'data/users.json'

    @commands.command(name='new',description='Criar um novo utilizador do bot, inicializando assim os stats')
    async def new(self,ctx):
        user = ctx.message.author

        if self.bot.data.users.create_user(user.id, user.name):
            await ctx.send(user.name + ' joins the fight!')
        else:
            await ctx.send(user.name + ' already joined the fight!')



    @commands.command(name='stats',description='Mostra os stats do utilizador ou de alguem mencionado')
    async def stats(self,ctx , mention: discord.User=None):

        if mention == None:
            usr = ctx.message.author
        else:
            usr = mention

        user_data = self.bot.data.users.get_user(usr.id)

        if user_data != None:
            embed = discord.Embed(title=user_data.name(), color=self.bot.embed_color)
            embed.set_thumbnail(url=usr.avatar_url)

            embed.add_field(name='Nivel :',value=str(user_data.level()), inline=False)
            
            if user_data.badges() != []:
                badges_concatenated = "".join(user_data.badges())
                print(badges_concatenated)
                strf = ""                    #
                for i in user_data.badges(): #
                    strf += i                #
                embed.add_field(name='Badges :', value=badges_concatenated, inline=False)

            embed.add_field(name='Exp :', value= user_data.exp_bar(10) + ' ( ' + str(user_data.exp()) + ' / ' + "%d"%user_data.max_exp() + ' )', inline=False)
            embed.add_field(name='Cash :', value=str(user_data.cash()) + ' €', inline=False)

            await ctx.send(embed=embed)

        else:
            await ctx.send("Utilizador inexistente `*new` para criar")


    @commands.command(name='bless',description='Dá coisas vindas do além' , brief=Perms.OWNER)
    async def bless(self,ctx, item: str , usr:discord.User , qnt):
        add_item = {
            'xp'   : lambda u : u.add_xp(int(qnt)),
            'cash' : lambda u : u.add_cash(int(qnt)),
            'badge': lambda u : u.add_badge(qnt)
        }

        if item not in add_item:
            await ctx.send("Item inválido")
            return

        user_data = self.bot.data.users.get_user(usr.id)
        if user_data != None:
            add_item[item](user_data)
            await ctx.send("{} got blessed with {}".format(usr.name, item))
        else:
            await ctx.send("Utilizador inexistente `*new` para criar")
        


    @commands.command(name='give', description='Dá dinheiro do teu próprio bolso a alguém')
    async def give(self,ctx, usr:discord.User, qnt=0):
        dta = load_data(self.bot.users_file)

        user_from = self.bot.data.users.get_user(ctx.message.author.id)
        if user_from == None:
            await ctx.send("Utilizador inexistente `*new` para criar")
            return
    
        user_to = self.bot.data.users.get_user(usr.id)
        if user_to == None:
            await ctx.send("Utilizador alvo inexistente")
            return

        if qnt <= 0 :
            await ctx.send("Quantidade inválida!")
            return
        
        if user_from.cash() < qnt:
            await ctx.send(":exclamation: Dinheiro Insuficiente :exclamation:")
            return

        user_from.add_cash(-1*qnt)
        user_to.add_cash(qnt)

        await ctx.send(usr.name + " recebeu " + str(qnt) + " € de " + ctx.message.author.name)


    @commands.command(name='ranking',description='Ranking global de maior nivel')
    async def ranking(self,ctx):
        embed = discord.Embed(title='Ranking',color=self.bot.embed_color)

        users_ids = list(self.bot.data.users.users_data['users'])
        prestige_users_ids = []
        for i in users_ids:
            if ':beginner:' in self.bot.data.users.get_user(i).badges():
                prestige_users_ids.append(i)
                users_ids.remove(i)

        users_ids.sort(key=(lambda u_id : -1*self.bot.data.users.get_user(u_id).level()))
        prestige_users_ids.sort(key=(lambda u_id : -1*self.bot.data.users.get_user(u_id).level()))

        count = 1
        for i in prestige_users_ids:
            embed.add_field(name=str(count) + ". " + self.bot.get_user(int(i)).name + " :beginner:", value="Level : " +  str(self.bot.data.users.get_user(i).level()) ,inline=False)
            if count == 10:
                break
            else:
                count+=1

        for i in users_ids:
            embed.add_field(name=str(count) + ". " + self.bot.get_user(int(i)).name , value="Level : " + str(self.bot.data.users.get_user(i).level()) ,inline=False)
            if count == 10:
                break
            else:
                count+=1
        await ctx.send(embed=embed)


    @commands.command(name='buy',description='Compra itens por dinheiro.\nItens disponíveis:\n` xp / 1 €`\n` prestige / 50 lvl`')
    async def buy(self,ctx,item:str,qnt:int=None):
        user_data = self.bot.data.users.get_user(ctx.message.author.id)
        if user_data == None:
            await ctx.send("Utilizador inexistente `*new` para criar")
            return
        
        if qnt != None and qnt<=0:
            await ctx.send("Quantidade inválida")
            return
        

        if item == "xp":
            if qnt > user_data.cash():
                await ctx.send(":exclamation: Dinheiro Insuficiente :exclamation: {} €".format(user_data.cash()))
            else:
                user_data.add_cash(-1*qnt)
                user_data.add_xp(qnt)
                await ctx.send(":white_check_mark: Compra efectuada com sucesso :white_check_mark: ")

        elif item == "prestige":
            if 50 > user_data.level():
                await ctx.send(":exclamation: Nivel Insuficiente :exclamation: {}".format(user_data.level()))
            else:
                if ':beginner:' in user_data.badges():
                    await ctx.send("Já tens esta badge!")
                else:
                    user_data.add_badge(':beginner:')
                    user_data.set_level(1)
                    user_data.set_exp(0)
                    user_data.set_cash(100)
                    await ctx.send("Acabaste de ganhar a badge de Prestige :beginner:!")


def setup(bot):
    bot.add_cog(Stats(bot))

############################################# Player #############################################

class Player:
    def __init__(self, uid:int):#, dic:dict=None):
        """ self.id = uid
        if dic != None:
            
            self.lvl = dic['lvl']
            self.exp = dic['exp']
            self.cash = dic['cash']
        else: """

        with open("data/users.json",'r') as file:
            data_string = json.load(file)
        if str(uid) not in data_string['stats'].keys():
            self.uid  = uid
            self.badges = []
            self.lvl  = 1
            self.exp  = 0
            self.cash = 100
        else:
            dic = data_string['stats'][str(uid)]
            self.uid  = uid
            self.badges = dic['badges']
            self.lvl  = dic['lvl']
            self.exp  = dic['exp']
            self.cash = dic['cash']
        
        


    def ret(self):
        return {
            "lvl": self.lvl,
            "exp": self.exp,
            "cash": self.cash,
            "badges": self.badges
        }



    def max_exp(self):
        return 100*1.15**(self.lvl-1)



    def save(self,file_name:str='data/users.json'):
        with open(file_name,'r') as file:
            data_string = json.load(file)

        data_string['stats'][str(self.uid)] = self.ret()

        with open(file_name,'w') as file:
            json.dump(data_string,file, indent=4)



    def give(self,type:str,qnt):
        if type == "xp":
            self.exp += qnt
            while self.exp >= self.max_exp():
                self.exp = int(self.exp) - int(self.max_exp())
                self.lvl += 1

        elif type == "cash":
            self.cash += int(qnt)

        elif type == "badge":
            self.badges.append(str(qnt))

        

    def par_bar(self,n):
        def bar(n, total):
            def repeat(string_to_expand, length):
                return (string_to_expand * (int(length/len(string_to_expand))+1))[:length]

            return (repeat('▓',n) + repeat('░',total-n))

        i = 0
        while self.exp > i*self.max_exp()/n:
            i+=1
        return bar(i,n)