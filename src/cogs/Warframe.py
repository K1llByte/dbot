import discord
from discord.ext import commands
import random
import json
from control.database import *
from control.model.users import Perms
from control.model.warframe import Build


class Warframe(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.bot.warframe_file = 'data/warframe.json'

    @commands.command(name='plat', description='Dado um numero de platinas ele devolve o valor em euros dessas platinas (pode ser passado o valor em percentagem do desconto das platinas)')
    async def plat(self ,ctx, inp, desc=0):
        # TRASH CODE
        d = (100-float(desc))/100
        plat = int(inp)
        if plat <= 75:
            plat *= 4.49/75
        elif plat <= 170:
            plat *= 8.99/170
        elif plat <= 370:
            plat *= 17.77/370
        elif plat <= 1000:
            plat *= 44.99/1000
        elif plat <= 2100:
            plat *= 89.99/2100
        elif plat <= 4300:
            plat *= 179.99/4300
        else:
            plat = (plat - 4300)*0.057 + 179.99
        embed = discord.Embed(color=self.bot.embed_color)
        embed.set_thumbnail(url='https://lh3.googleusercontent.com/PcZkrGrxWVZAilN5rD06ISUednLXlBYwAwHK7TT_zqXvmuwDCD9i3y5sT-OIOP810ks=s180')
        embed.add_field(name='Preço médio: ', value="%.2f €"%(plat*d), inline=False)
        await ctx.send(embed=embed)



    @commands.command(name='ducats', description='Converte de ducats para o numero de pecas necessárias para obter esses ducats em pecas de 45 ducats com um preço de 5 platinas cada.')
    async def ducats(self,ctx, ducats=0):
        if not (ducats != 0 and ducats < 100000):
            await ctx.send('Insira um numero de ducats válido')
        else:
            # TRASH CODE
            #ducats = int(duc)
            pecas = 0
            while ducats > 0:
                ducats = ducats - 45
                pecas = pecas + 1
            embed = discord.Embed(color=self.bot.embed_color)
            embed.set_thumbnail(url='https://lh3.googleusercontent.com/PcZkrGrxWVZAilN5rD06ISUednLXlBYwAwHK7TT_zqXvmuwDCD9i3y5sT-OIOP810ks=s180')
            embed.add_field(name='Minimo de pecas: ', value=pecas, inline=False)
            embed.add_field(name='Minimo de ducats: ', value=pecas*45, inline=False)
            embed.add_field(name='Platinas: ', value=pecas*5, inline=False)
            await ctx.send(embed=embed)
   


    @commands.command(name='build', description='Mostra um build de uma arma / warframe')
    async def build(self,ctx, *arg):
        pal = ' '.join(arg)
        pal = pal.lower().title()
        if pal != '':
            build = self.bot.data.warframe.get_build(pal)
            if build == None:
                await ctx.send("Build inexistente")
                return
            
            embed = discord.Embed(title=pal,color=self.bot.embed_color)
            embed.set_image(url=build.link())
            if build.description() != "": 
                embed.add_field(name="Descricao:", value=build.description(), inline=False)
            await ctx.send(embed=embed)
        
        else:
            await ctx.send('Insira o nome de uma arma / warframe')



    @commands.command(name='buildlist', description='Mostra a lista de builds disponíveis')
    async def buildlist(self,ctx):
        categories = {
            'Primaria'   : '',
            'Secundaria' : '',
            'Melee'      : '',
            'Warframe'   : '',
            'Other'      : ''
        }
        embed = discord.Embed(title='Lista de builds disponíveis:', color=self.bot.embed_color)

        for build_name in self.bot.data.warframe.warframe_data['builds']:
            categ = self.bot.data.warframe.get_build(build_name).category()
            if categ in categories:
                categories[categ] += '{}\n'.format(build_name)
            else:
                categories['Other'] += '{}\n'.format(build_name)

        for categs in categories:
            if categories[categs] != '':
                embed.add_field(name=categs + "s", value=categories[categs], inline=True)

        await ctx.send(embed=embed)



    @commands.command(name='buildadd', description='Adiciona um build ao bot, sendo necessário pelo menos uma tag e o link do build respetivo sendo a categoria e a descrição opcionais', brief=Perms.ADMIN)
    async def buildadd(self,ctx, tag, link, categ="", desc=""):
        build_name = tag.lower().title()

        await ctx.send( build_name + ' adicionado com sucesso' \
            if self.bot.data.warframe.create_build(build_name, desc, link, categ) \
            else 'Tag já existe')



    @commands.command(name='builddel', description='Remove um build', brief=Perms.ADMIN)
    async def builddel(self,ctx, *args):
        build_name = ' '.join(args)

        await ctx.send( '`{}` apagado'.format(build_name) \
            if self.bot.data.warframe.del_build(build_name) \
            else 'Tag inexistente')



    @commands.command(name='setbuild', description='Altera um parâmetro de um build', brief=Perms.ADMIN)
    async def setbuild(self,ctx, tag, parametro, *args):
        build_name = tag.lower().title()
        value = ' '.join(args)

        set_param = {
            'link'  : lambda b,v: b.set_link(v),
            'desc'  : lambda b,v: b.set_description(v),
            'categ' : lambda b,v: b.set_category(v)
        }

        if parametro not in set_param:
            await ctx.send('Parametros alteráveis disponiveis: `{}`'.format(list(set_param)))
            return

        build = self.bot.data.warframe.get_build(build_name)
        if build != None:
            set_param[parametro](build, value)
            await ctx.send('Parametro de ' + build_name + ' alterado!')
        else:
            await ctx.send('Tag inexistente')



def setup(bot):
    bot.add_cog(Warframe(bot))