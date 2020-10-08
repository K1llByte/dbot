import discord
from discord.ext import commands
from cogs.Stats import Player
import random
from control.model.users import Perms


class Games(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.command(name="roll",description="Aposta um valor de cash em um dos valores da roulette tradicional de casino")
    async def roll(self,ctx,choice:str, bet:int): # TODO: Refactor code
        if bet <= 0:
            return
        
        user_data = self.bot.data.users.get_user(ctx.message.author.id)
        if user_data == None:
            await ctx.send("Utilizador inexistente `*new` para criar")
            return
        
        if user_data.cash() < bet:
            await ctx.send(":exclamation: Ayyyy lmao ... tas sem guito :exclamation:")
            return
        r = random.randrange(0, 36, 1)

        if r == 0 :
            res = 'green'
        elif r % 2 :
            res = 'red'
        elif not r % 2:
            res = 'black'
        else:
            return

        if res == choice.lower():
            if res == 'green' :
                user_data.add_cash(35*bet)
            else:
                user_data.add_cash(bet)
            await ctx.send( ":white_check_mark: `{}` - Saiu '{}' Ganhaste {} €  :) :white_check_mark:".format(user_data.name(),res,bet) )
        else:
            user_data.add_cash(-1*bet)
            await ctx.send(":x: `{}` - Saiu '{}' Perdeste {} €  :( :x:".format(user_data.name(),res,bet))

        user_data.add_xp(5)



def setup(bot):
    bot.add_cog(Games(bot))