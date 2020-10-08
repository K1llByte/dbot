import asyncio
import discord
from discord.ext import commands
import youtube_dl
#from queue import Queue
from control.model.users import Perms
import os


#######################################################

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(id)s.mp3', #'%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.id = data.get('id')
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
            #print(data)

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

#######################################################

class Music(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.queue = []#Queue() # Unlimited size queue

        self.REMOVE_DOWNLOADS = True


    @commands.command(name='join', description='Entra no voice channel')
    async def join(self,ctx):
        await ctx.author.voice.channel.connect()


    @commands.command(name='leave', description='Sai do voice channel')
    async def leave(self,ctx):
        await ctx.voice_client.disconnect()


    @commands.command(name='play', description='Play\'s music', aliases=['p'])
    async def play(self, ctx, *, url):
#        if ctx.voice_client == None:
#            await ctx.author.voice.channel.connect()
#
#        async with ctx.typing():
#            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
#            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
#
#        await self.nowplaying(ctx)
        if ctx.voice_client == None:
            await ctx.author.voice.channel.connect()

        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        #self.queue.insert(0,player)

        if ctx.voice_client.is_playing():
            self.queue.insert(0,player)
            await ctx.send(f'Queued: `{url}`')
        else:
            def loop_play(e):
                if e:
                    print('Player error: %s' % e)
                else:
                    if len(self.queue) > 0:
                        ctx.voice_client.play(self.queue.pop(), after=loop_play)
                    else:
                        return

            ctx.voice_client.play(player, after=loop_play)
        await self.nowplaying(ctx)


    @commands.command(name='pause', description='Pause current music')
    async def pause(self,ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()


    @commands.command(name='resume', description='Resume paused music')
    async def resume(self,ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()


    @commands.command(name='stop', description='Stop playing and clear queue')
    async def stop(self,ctx):
        if ctx.voice_client.is_playing():
            self.queue = []
            ctx.voice_client.stop()

    @commands.command(name='skip', description='Stops current playing music and plays next in the queue',aliases=['s','n','next'])
    async def skip(self,ctx, next_idx=1):
        if next_idx < 0 or next_idx % int(next_idx) or next_idx > len(self.queue):
            print('invalid arg')
            return
        if ctx.voice_client.is_playing():
            if next_idx != 1:
                self.queue = self.queue[:(-1)*(next_idx-1)]
            ctx.voice_client.stop()
            print('ctx.voice_client.stop()')
        


    @commands.command(name='volume', description='Music playing audio volume', aliases=['v'])
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))


    @commands.command(name='nowplaying', description='Music playing now', aliases=['np'])
    async def nowplaying(self,ctx):
        if ctx.voice_client != None:
            tmp = f'Now playing:  `{ctx.voice_client.source.title}`' \
                if ctx.voice_client.is_playing() else 'Not playing anything!'

            embed = discord.Embed(title=tmp, color=self.bot.embed_color)
            await ctx.send(embed=embed)
            


    @commands.command(name='queue', description='List music queue', aliases=['q'])
    async def queue(self,ctx):

        if ctx.voice_client != None:
            
            
            # TODO: indicate that is paused if that's the case
            if ctx.voice_client.source != None:
                #embed = discord.Embed(title=f'Now playing:  `{ctx.voice_client.source.title}`',color=self.bot.embed_color)
                self.nowplaying(ctx)
                #if self.queue == []:
                #    await ctx.send(embed=discord.Embed(title='Sadly the queue is empty :c',color=self.bot.embed_color))
                
                _sizeq = len(self.queue)
                for i in range(_sizeq):
                    embed.add_field(name=f'**{i+1}.** `{self.queue[_sizeq-i-1].title}`', value='============================', inline=False)
                await ctx.send(embed=embed)

        
    @commands.command(name='download', description='Download youtube audio', aliases=['dl'])
    async def download(self,ctx, url):
        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=False)
        await ctx.send(file=discord.File(f'downloads/{player.id}.mp3'))
        if self.REMOVE_DOWNLOADS:
            os.remove(f'downloads/{player.id}.mp3')
            if len(os.listdir('downloads/')) == 0:
                os.rmdir('downloads/')



def setup(bot):
    bot.add_cog(Music(bot))