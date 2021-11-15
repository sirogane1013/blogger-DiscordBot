import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix='/')


@bot.event
async def on_ready():
    print('Logged in')


# write your commands here
# @bot.command()
# async def my_command(ctx):
#     await ctx.send("hello")


bot.run(TOKEN)
