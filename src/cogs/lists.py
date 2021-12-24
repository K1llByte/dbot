import discord
from discord.ext import commands
import random
import json
from control.database import *
from control.model.users import Perms


class Lists(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.bot.memes_file = 'data/memes.json'
        self.bot.users_file = 'data/users.json'



    @commands.command(name='permsadd', description='Adiciona um admin ao bot',brief=Perms.OWNER)
    async def permsadd(self,ctx, *mention):
        tag = ctx.message.mentions[0].name
        try:
            await self.bot.add_list(self.bot.users_file, ctx, 'admins', tag , int(ctx.message.mentions[0].id))
        except Exception as error:
            await ctx.send(error)



    @commands.command(name='adminlist', description='Mostra todos os admins do bot', brief=Perms.ADMIN)
    async def adminlist(self,ctx):
        embed = discord.Embed(color=self.bot.embed_color)
        embed.set_author(name='Administradores')

        for user_id in self.bot.data.users.users_data['users']:
            user_data = self.bot.data.users.get_user(user_id)
            if user_data.permissions() > Perms.DEFAULT:
                embed.add_field(name=user_data.name(), value= 'Permissões : ' + str(user_data.permissions()), inline=False)
                
        await ctx.message.author.send(embed=embed)



    @commands.command(name='meme', description='Commando que mostra um meme aleatório ou um específico com uma certa tag')
    async def meme(self,ctx, *args):
        key = ' '.join(args)
        if key != '':
            value = self.bot.data.memes.get(key)
            await ctx.send(value if value != None else 'Tag inexistente')
        else:
            await ctx.send(self.bot.data.memes.get_random())

    @commands.command(name='memelist', description='Mostra todos os memes guardados no bot')
    async def memelist(self,ctx):
        res = ''
        for w in self.bot.data.memes.key_list():
            res += '{}\n'.format(w)
        await ctx.send(res)

    @commands.command(name='memeadd', description='Adiciona um link de meme ao bot', brief=Perms.ADMIN)
    async def memeadd(self,ctx,key,*value):
        value = ' '.join(value)
        added = self.bot.data.memes.add(key,value)
        await ctx.send( '`{}` adicionado com sucesso'.format(key) if added else 'Tag já existe')

    @commands.command(name='memedel', description='Deleta um meme', brief='admin')
    async def memedel(self,ctx, *args):
        key = ' '.join(args)
        deleted = self.bot.data.memes.delete(key)
        await ctx.send('Apagado `{}`'.format(key) if deleted else 'Tag inexistente')

    

    @commands.command(name='data', description='Envia por PM data json de uma tag', brief=Perms.OWNER)
    async def data(self,ctx,tag):
        data_string = load_data(self.bot.users_file)
        await ctx.message.author.send(str(data_string[tag]))

def setup(bot):
    bot.add_cog(Lists(bot))