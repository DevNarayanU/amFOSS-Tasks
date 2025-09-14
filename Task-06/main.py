import discord
import json
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from lrclib import LrcLibAPI as lrc 
api = lrc(user_agent="my-app/0.0.1") 

'''
'''
load_dotenv()

token=os.getenv('DISCORD_TOKEN')

handler=logging.FileHandler(filename='discord.org',encoding='utf-8',mode='w')
intents=discord.Intents.default()
intents.message_content=True
intents.members=True

bot=commands.Bot(command_prefix='/',intents=intents)

srole='dreamer'

@bot.event
async def on_ready():
    print("Bot is ready to operate")
@bot.event
async def on_member_join(member):
    await member.send(f"Welcome to the server {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
         return
    await bot.process_commands(message)

@bot.command()
async def hello(x):
    await x.send(f"Hello {x.author.mention} !")

@bot.command()
@commands.has_role(srole)
async def dreamer(x):
    await x.send(f"You already have {srole} title  👍" )

    
@dreamer.error
async def dreamer(x,error):
    if isinstance(error,commands.MissingRole):
        role= discord.utils.get (x.guild.roles,name=srole)
    if role:
    
        await x.author.add_roles(role)
        await x.send(f"{x.author.mention} is now to assigned to {srole}")
    
    else:
        await x.send("Role doesn't exist")

@bot.command()
@commands.has_role(srole)
async def remove(x):
    role= discord.utils.get (x.guild.roles,name=srole)
    if role:
        await x.author.remove_roles(role)
        await x.send(f"{x.author.mention} is stripped from {srole} title")

    else:
        await x.author.send("Role doesn't exist")
@remove.error
async def secret_error(x,error):
    if isinstance(error,commands.MissingRole):
        await x.send(f"You dont have {srole} title")

@bot.command()
async def dm(x,*,msg):
    await x.author.send(f"You said {msg}")

@bot.command()
async def reply(x):
    await x.reply("This is a reply to your message")
@bot.command()
@commands.has_role(srole)
async def secret(x):
    await x.send("Welcome to the club!!!")

@secret.error
async def secret_error(x,error):
    if isinstance(error,commands.MissingRole):
        await x.send("You currently don't have enough power to do that")


@bot.command()
async def track(x,*,l:str.split):
    
    results = api.search_lyrics(
    track_name=l[0]
    )

    if not results:
        await x.send("No songs for your query")
        return
    elif results:
        i=1
        for result in results[:5] :
            await x.send(f"{i} ) {result.artist_name} - {result.track_name} ({result.album_name})")
            i+=1
@bot.command()
async def insert(x, *, l: str):
    try:
        song, artist = map(str.strip, l.split('-', 1))  # safe split
    except ValueError:
        await x.send("❌ Please use format : `/insert <song> - <artist>`")
        return

    try:
        with open("users.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    user_key = str(x.author.name)  

    if user_key not in data:
        data[user_key] = []
    if f"{song} - {artist}" not in data[user_key]:
        data[user_key].append(f"{song} - {artist}")

    with open("users.json", "w") as f:
        json.dump(data, f, indent=4)

    await x.send(f"Added **{song} - {artist}** for {x.author.mention}")

@bot.command()
async def delete(x, *, l: str):
    try:
        song, artist = map(str.strip, l.split('-', 1)) 
    except ValueError:
        await x.send("Please use format : `/delete <song> - <artist>`")
        return

    try:
        with open("users.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    user_key = str(x.author.name)  
    if user_key not in data or not data[user_key]:
        await x.send(" You don’t have any songs in playlist")
        return
    try:
        data[user_key].remove(f"{song} - {artist}")
    except ValueError:
        await x.send(f"Could not find **{song} - {artist}** in your list.")
        return
    

    with open("users.json", "w") as f:
        json.dump(data, f, indent=4)

    await x.send(f"deleted **{song} - {artist}** for {x.author.mention} from playlist")

@bot.command()
async def view(x):
    
    user_key = str(x.author.name) 

    try:
        with open("users.json", "r") as f:
            data = json.load(f)
        for i in range(len(data[user_key])):
            await x.send(f"{i+1} :: {data[user_key][i]} ")
    except (FileNotFoundError, json.JSONDecodeError):        
        await x.send(f" Could not find any song in your list.")
        return
    

     
    if user_key not in data or not data[user_key]:
        await x.send(" You don’t have any songs in playlist")
        return
    
@bot.command()
@commands.has_role(srole)   
async def lyrics(x,*,l:str):
    try:
        song,artist=l.split('-')
    except ValueError:
        await x.send("❌ Please use format : `/lyrics <song> - <artist>`")
        return
    
    results = api.search_lyrics(
    track_name=song,
    artist_name=artist,
    )
    if results:
        for result in results[:1] :
                song=result.track_name
                artist=result.artist_name
                album=result.album_name
                dur=result.duration
        await x.send(f"fetching {song} by {artist}, from {album}")

        lyric = api.get_lyrics(
        track_name=song,
        artist_name=artist,
        album_name=album,
        duration=dur,

            
            
            )
        found_lyrics =  lyric.plain_lyrics or lyric.synced_lyrics 
        await x.send("\n".join(found_lyrics.split("\n")[::]))
    if not results:
        await x.send("No songs found 😔 , please try /track command for cross checking")
@lyrics.error
async def secret_error(x,error):
    if isinstance(error,commands.MissingRole):
        await x.send(f"You currently don't have {srole} title to do that 💔 ")


bot.run(token,log_handler=handler ,log_level=logging.DEBUG)
