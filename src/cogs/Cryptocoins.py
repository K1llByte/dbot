import asyncio
import discord
from discord.ext import commands

class Cryptocoins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='buycrypto', description='Buy crypto currency')
    async def buycrypto(self,ctx, symbol, qnt: int):
        symbol = symbol.lower()
        qnt = int(qnt)
        if qnt <= 0:
            await ctx.send("Invalid arg range")
            return

        user_data = self.bot.data.users.get_user(ctx.message.author.id)
        if user_data == None:
            await ctx.send("Utilizador inexistente `*new` para criar")
            return

        user_coins = self.bot.data.crypto.get_user_coins(ctx.message.author.id)
        if user_coins == None:
            self.bot.data.crypto.create_user_coins(ctx.message.author.id)
            user_coins = self.bot.data.crypto.get_user_coins(ctx.message.author.id)

        if user_data.cash() < qnt:
            await ctx.send("Insufficient funds")
            return

        #### Proccess transaction ####
        if self.bot.data.crypto.is_coin_active(symbol):
            coin_value = self.bot.data.crypto.coin_value(symbol)
            obtained = qnt / coin_value
            user_data.add_cash((-1)*qnt)
            user_coins.add(symbol, obtained)
            await ctx.send(f'Obtained {obtained} of {symbol}')
        else:
            await ctx.send("Invalid currency")

    @commands.command(name='coins', description='List your coins')
    async def coins(self,ctx, mention: discord.User=None):

        if mention == None:
            usr = ctx.message.author
        else:
            usr = mention

        user_data = self.bot.data.users.get_user(usr.id)
        if user_data == None:
            await ctx.send("Utilizador inexistente `*new` para criar")
            return

        user_coins = self.bot.data.crypto.get_user_coins(usr.id)
        if user_coins == None:
            self.bot.data.crypto.create_user_coins(usr.id)
            user_coins = self.bot.data.crypto.get_user_coins(usr.id)

        embed = discord.Embed(title=user_data.name(), color=self.bot.embed_color)

        coins_data = user_coins.data()
        for code in coins_data:
            embed.add_field(name=code.upper(), value=str(coins_data[code]['quantity']), inline=False)

        await ctx.send(embed=embed)


        

def setup(bot):
    bot.add_cog(Cryptocoins(bot))