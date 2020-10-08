import discord
from discord.ext import commands
from control.logs import info_log, error_log
import subprocess
import os
from control.logs import info_log
from control.model.users import Perms



class Management(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    @commands.command(name='unload', description='Faz unload de uma cog' , brief=Perms.OWNER)
    async def unload(self,ctx,ext):
        try:
            self.bot.unload_extension('cogs.' + ext)
            print( info_log("Unloaded {}".format(ext)) )
            await ctx.send("{} Unloaded".format(ext))
        except Exception as error:
            print( error_log('{} cannot be unloaded. {}'.format(ext , error)) )
            await ctx.send("Error Unloading")



    @commands.command(name='load', description='Faz load de uma cog' , brief=Perms.OWNER)
    async def load(self,ctx,ext):
        try:
            self.bot.load_extension('cogs.' + ext)
            print( info_log("Loaded {}".format(ext)) )
            await ctx.send("{} Loaded".format(ext))
        except Exception as error:
            print( error_log('{} cannot be loaded. {}'.format(ext , error)) )
            await ctx.send("Error Unloading")



    @commands.command(name='cogs', description='Mostra todas as cogs disponiveis' , brief=Perms.OWNER)
    async def cogs(self,ctx):
        await ctx.send(str(list(self.bot.cogs.keys())))




    @commands.command(name='restart', description='Reinicia o bot',brief=Perms.OWNER)
    async def restart(self,ctx):
        await self.bot.change_presence(status=discord.Status.idle,activity=discord.Game(name='rebooting'))
        
        pid = os.fork()
        if pid == 0:
        
            subprocess.call("sleep 5 ; python3 src/bot.py", shell=True)
            
        else:
            #await self.bot.logout()
            subprocess.call("kill -9 " + str(pid), shell=True)
            await self.bot.logout()
            #os._exit(0)


    @commands.command(name='kill',description='Mata o bot *Musica dramática*', brief=Perms.OWNER)
    async def kill(self,ctx):
        await ctx.send(":dizzy_face:")
        await self.bot.logout()

        #print( info_log('Exiting bot . . .') )
        #subprocess.call('kill -9 ' + str(os.getpid()),shell=True)

def setup(bot):
    bot.add_cog(Management(bot))


#Example cog

#import discord
#from discord.ext import commands
#
#class Example(commands.Cog):
#    def __init__(self,bot):
#        self.bot = bot
#
#
#def setup(bot):
#    bot.add_cog(Example(bot))