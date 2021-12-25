import discord
from discord.ext import commands
import random
from urllib import request
import json
from control.model.users import Perms


class Fun(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='choose', description='Escolhe dos argumentos um aleatório')
    async def choose(self,ctx,*args):
        await ctx.send(random.choice(args))


    @commands.command(name='secret_friend', description='Cria um jogo de amigo secreto e manda por mensagem privada o alvo', brief=Perms.OWNER)
    async def secret_friend(self,ctx,*users: discord.User):
        if users == ():
            await ctx.send("You have to mention users")
        # print(users)
        it = set(users)
        tmp = set(users)
        # print(tmp)

        for u in it:
            print(u)
            dm = u.dm_channel
            if dm == None:
                dm = await u.create_dm()
            
            can_be_choosen = tmp.copy()
            if u in can_be_choosen: 
                can_be_choosen.remove(u)
            if can_be_choosen == set([]):
                await ctx.send("Unexpected error")
                return

            selected = random.sample(can_be_choosen,1)[0]
            tmp.remove(selected)

            await dm.send("Tu és amigo secreto de: {}".format(str(selected)))

        await ctx.send("Created secret friend game")


    @commands.command(name='dog', description='Cão aleatório')
    async def dog(self,ctx):
        req = request.Request('https://some-random-api.ml/img/dog', headers={'User-Agent' : "Magic Browser"}) 
        jsonObj = request.urlopen(req)
        data = json.load(jsonObj)
        await ctx.send(embed=discord.Embed().set_image(url=data['link']))


    @commands.command(name='cat', description='Gato aleatório')
    async def cat(self,ctx):
        req = request.Request('https://some-random-api.ml/img/cat', headers={'User-Agent' : "Magic Browser"}) 
        jsonObj = request.urlopen(req)
        data = json.load(jsonObj)
        await ctx.send(embed=discord.Embed().set_image(url=data['link']))


    @commands.command(name='redpanda', description='Panda vermelho aleatório')
    async def redpanda(self,ctx):
        req = request.Request('https://some-random-api.ml/img/red_panda', headers={'User-Agent' : "Magic Browser"}) 
        jsonObj = request.urlopen(req)
        data = json.load(jsonObj)
        await ctx.send(embed=discord.Embed().set_image(url=data['link']))


    @commands.command(name='panda', description='Panda aleatório')
    async def panda(self,ctx):
        req = request.Request('https://some-random-api.ml/img/panda', headers={'User-Agent' : "Magic Browser"}) 
        jsonObj = request.urlopen(req)
        data = json.load(jsonObj)
        await ctx.send(embed=discord.Embed().set_image(url=data['link']))


def setup(bot):
    bot.add_cog(Fun(bot))