import discord
from discord.ext.commands import Bot
import json
import os
from control.logs import info_log, command_log, error_log
from control.database import add_list, Data
import signal
import sys
import asyncio
from control.model.users import Perms

################################### bot startup ######################################

TOKEN = None
try:
    from auth import TOKEN
except ModuleNotFoundError as mnf:
    if TOKEN == None:
        print( error_log("Missing TOKEN, auth.py file not present or TOKEN not defined") )
        exit(1)

bot = Bot(command_prefix='*', help_command=None)

all_cogs = list(map(lambda x: x[:-3] , filter(lambda x: not x.startswith('__') , os.listdir('src/cogs/'))))

bot.users_file    = 'data/users.json'
bot.memes_file    = 'data/memes.json'
bot.warframe_file = 'data/warframe.json'
bot.embed_color = 0x000000#0x519181

################################### bot events ######################################

@bot.event
async def on_message(message):
    if message.content.lower() == "diz ola bob":
        await message.channel.send("Olá Bob!\n:black_heart:️:heart:\n   :tongue:")

    if message.content.startswith(bot.command_prefix):

        print( command_log(message.author.name + "#" + message.author.discriminator, message.content) )
        #print('> ' + message.content)

        try:
            #Permission checking
            cmd = message.content.split()[0][1:]
            cmd_perms = bot.all_commands[cmd].brief
            user_data = bot.data.users.get_user(message.author.id)
            if (not (cmd_perms == None or cmd_perms == Perms.DEFAULT)) and (user_data == None or not user_data.has_permissions(cmd_perms)):
                print(error_log('No permitions'))#await message.channel.send('No permitions')
            else:
                await bot.process_commands(message)

        except KeyError:
            #TODO: Various Exceptions handlings here
            print(error_log('Invalid command'))
            


@bot.event
async def on_message_edit(before, after):
	await bot.process_commands(after)


@bot.event
async def on_command_error(event, *args, **kwargs):
    print( error_log( str(args[0]) ) )

@bot.event
async def on_ready():
    #signal.signal(signal.SIGINT, signal_handler)

    await bot.change_presence(activity=discord.Game(name= bot.command_prefix + 'help to list commands'))

    print( info_log('{bot_name} ONLINE in {num_servers} Servers'.format(bot_name=bot.user.name, num_servers=len(bot.guilds))) )
    
    #print('# ' + bot.user.name + ' ONLINE')#(await bot.application_info()).name + ' ONLINE')
    #print('# In ' + str(len(bot.guilds)) + ' Servers')

    #print('# Cogs loaded: ' + str(list(bot.cogs.keys())))



def load_cogs(ext):
    for ext in all_cogs:
        try:
            bot.load_extension('cogs.' + ext)
        except Exception as error:
            print( error_log('{} cannot be loaded <{}>'.format(ext , error)) )


    str_cogs = ''
    for c in list(bot.cogs.keys()):
        str_cogs += (c + ' ')

    print( info_log('Loaded cogs: [ {cogs}]'.format(cogs=str_cogs)) )


##################################### help ########################################

@bot.command(name='help', description='Mostra todos os comandos disponíveis ou informações sobre um comando')
async def help(ctx,cmd=''):

    list_cmds = bot.all_commands  #map(lambda h : h.name , bot.commands)
    embed = discord.Embed(title='Lista de comandos:',color=bot.embed_color)
    
    if cmd != '':
        if cmd in list_cmds:
            
            command = list_cmds[cmd]

            embed = discord.Embed(title="Comando",description=command.qualified_name,color=bot.embed_color)
            if command.brief != None:
                embed.add_field(name="Permissions:", value=command.brief,inline=False)
            embed.add_field(name="Descrição:",value=command.description,inline=False)
            synopse = bot.command_prefix + command.name
            
            for param in command.clean_params.keys():
                synopse = synopse + " [" + param + "]"
                
            embed.add_field(name="Como utilizar:",value="`" + synopse + "`",inline=False)
            if len(command.aliases) > 0:
                embed.add_field(name="Alias:",value=command.aliases,inline=False)
            await ctx.send(embed=embed)

        else:
            await ctx.send('Comando inexistente')
    else: 
        
        embed = discord.Embed(title="Commands",description="Lista de commandos disponiveis",color=bot.embed_color)
        for cogs_i in bot.cogs.keys():
            cmdsStr = ''
            cog_cmds = list(map(lambda c : c.name , bot.cogs[cogs_i].get_commands()))
            cog_cmds.sort()
            for word in cog_cmds:
                user_data = bot.data.users.get_user(ctx.message.author.id)
                # TODO: Refactor THIS IS A MASSIVE HARDCODED SPAGHET REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE (its 5 am im tired <:c)
                if list_cmds[word].brief == None or list_cmds[word].brief == Perms.DEFAULT:
                    cmdsStr += ('**' + '\\' + bot.command_prefix + word + '** ' + '\n')
                if list_cmds[word].brief == Perms.ADMIN and user_data != None and user_data.has_permissions(list_cmds[word].brief):
                    cmdsStr += ('**' + '\\' + bot.command_prefix + word + '** Admin ' + '\n')
                if list_cmds[word].brief == Perms.OWNER and user_data != None and user_data.has_permissions(list_cmds[word].brief):
                    cmdsStr += ('**' + '\\' + bot.command_prefix + word + '** Owner ' + '\n')
            if cmdsStr != '':
                embed.add_field(name=cogs_i , value=cmdsStr,inline=True)
        
        embed.set_footer(text="{}help [comando] para mais informações sobre o comando".format(bot.command_prefix))
        await ctx.message.author.send(embed=embed)

##################################### main ########################################

if __name__ == '__main__':
    
    ##### Start #####
    print( info_log('Starting . . .') )
    bot.data = Data()
    load_cogs(all_cogs)

    ##### Run #####
    try:
        bot.run(TOKEN)
    except Exception as e:
        print( error_log(e) )

    ##### End #####
    bot.data.save()
    print( info_log('Saved data') )
    print( info_log('Exiting . . .') )
    asyncio.run(bot.logout())