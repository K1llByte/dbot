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