try:
    import conf
except ImportError:
    pass



 
import discord
from discord.ext import commands
import img_handler as imhl
import os, random



intense = discord.Intents.default()
intense.members = True
client = discord.Client(intents=intense)


channel = 825339546887127081
#Список зарегестированных серверов
whitelist = {
    #guild id => {channel.id => "guild_name / {channel.name}"}
    822806350886207538: {825339546887127081 : "Bots / mark-bot"},

}

#Декоратор - чекер @allowed_channel => True/False

def allowed_channel():
    async def predicate(ctx:commands.Context):
        if ctx.guild.id in whitelist:
            if ctx.channel.id in whitelist[ctx.guild.id].keys():
                return True
        await ctx.channel.send("You are on wron floor buddy")
        return False


    return commands.check(predicate)

bot = commands.Bot(command_prefix = "!", intents=intense)


    




@bot.command(name = "mka")
async def command_mka(ctx, f1:discord.Member=None, f2:discord.Member=None):
    if f1 and f2:
        msg = f'На арене непобедимый {f1.name} против бессмертного {f2.name}!'
        await imhl.vs_create_animated(f1.avatar_url, f2.avatar_url)

        await ctx.channel.send(file=discord.File(os.path.join("./img/result.gif"))  )
    else:
        msg = "Нужно два участника!"

    if msg==None:
        msg="error"


@bot.command(name = "join")
async def vc_join(ctx):
    voice_channel = ctx.author.voice.channel
    if voice_channel:
        msg = f'Подключаюсь к {voice_channel.name}'
        await ctx.channel.send(msg)
        await voice_channel.connect()

@bot.command(name = "leave")
async def vc_leave(ctx): 

    voice_channel = ctx.author.voice.channel
    msg = f'Отключаюсь от {voice_channel.name}'
    await ctx.channel.send(msg)
    await ctx.voice_client.disconnect()


@bot.command(name = "ost")
async def vc_ost(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    await ctx.channel.send(f'MORTAL COMBAT')
    await voice_client.play(discord.FFmpegPCMAudio(source="./sound/mk.mp3"))


@bot.command(name = "fight")
@allowed_channel()
async def command_fight(ctx):
    
    f1 = None
    f2 = bot.user
    voice_channel = ctx.author.voice.channel
    if voice_channel:
        await vc_join(ctx)

        voice_members = voice_channel.members
        voice_members = [m for m in voice_members if m.bot == False]
        if len(voice_members)>1:
            f1, f2 = [voice_members.pop(random.randint(0, len(voice_members)-1)), voice_members.pop(random.randint(0, len(voice_members)))]
        else:
            f1 = ctx.author
    else:
          await ctx.channel.send("Зайди в войс!")
    await imhl.vs_create_animated(f1.avatar_url, f2.avatar_url)        
    await ctx.channel.send(file=discord.File(os.path.join("./img/result.gif")))
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    await ctx.channel.send(f'MORTAL COMBAT')    
    await voice_client.play(discord.FFmpegPCMAudio(executable="./sound/ffmpeg.exe", source="./sound/mk.mp3"))



bot.run(os.environ["BOT_TOKEN"])