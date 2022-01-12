import datetime
import os
import re

import discord
import git

from discord.ext import commands
from dotenv import load_dotenv
from jinja2 import FileSystemLoader, Environment

import settings

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix='/')


@bot.event
async def on_ready():
    print('Logged in')


@bot.command()
async def new(ctx: commands.context, title: str = None, category: str = None, *tags):
    if title is None:
        title = datetime.datetime.now().strftime('%Y年%m月%d日')
    if category is None:
        category = "雑記"
    tags = set(tags)
    await ctx.send(
        "------------------\n" +
        f"title = {title}\n" +
        "date = {}\n".format(
            datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(timespec='seconds')) +
        f"category = {category}\n" +
        f"tags = {', '.join(tags)}\n"
        "------------------"
    )


@bot.command()
async def post(ctx):
    contents: [str] = []
    async with ctx.typing():
        async for message in ctx.history(limit=settings.HISTORY_LIMIT):
            if message.author == ctx.author:
                contents.append(message.content)
            elif message.author.bot:
                title, date, category, tags = extract_meta(message.content)
                break
        contents.reverse()
        contents.pop(-1)
        file_name = datetime.datetime.now().strftime('%Y-%m-%d') + "_{}.md".format(title)
        repo = git.Repo(settings.HUGO_DIR)
        origin = repo.remote(name='origin')
        origin.pull()
        with open(settings.HUGO_DIR + "/content/posts/" + file_name, "w", encoding="utf-8") as f:
            write_md(contents, title, date, category, tags, f)
        repo.git.add(settings.HUGO_DIR + "/content/posts/" + file_name)
        repo.git.commit(settings.HUGO_DIR + "/content/posts/" + file_name, message="ADD "+file_name, author="sirogane1013")
        origin = repo.remote(name='origin')
        origin.push()
    await ctx.send(
        "POSTED!"
    )


def extract_meta(message: str):
    title = re.findall('title = (.*)', message)
    date = re.findall('date = (.*)', message)
    category = re.findall('category = (.*)', message)
    tags = re.findall('tags = (.*)', message)
    if tags == ""
        tags_list = []
    else
        tags_list = tags[0].split(', ')
    return title[0], date[0], category[0], tags_list


def write_md(contents: [str], title: str, date: str, category: str, tags: [str], f):
    env = Environment(
        loader=FileSystemLoader('templates'),
        trim_blocks=True
    )
    template = env.get_template("posts.md")
    contents_flatten = "\n\n".join(contents)
    tags = ['"'+tag+'"' for tag in tags]
    f.write(template.render(contents=contents_flatten, title=title, date=date, category=category, tags=tags))


bot.run(TOKEN)
