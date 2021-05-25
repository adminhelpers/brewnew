import discord
from discord.ext import commands
from discord.utils import get
import datetime
import random
import re
import os
import time
import os.path
import sqlite3
import asyncio
import json
import requests
from Cybernator import Paginator
import jishaku
import wikipedia

from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://dbrbase:YqxZgV1GL8s4CVxX@rodinadb.rhew3.mongodb.net/rodinaname?retryWrites=true&w=majority")
db = cluster["rodina"]
muted = db["muted"]

class debug(commands.Cog):
    """DEBUG Cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        print('Rodina 04 | Debuger by dollar ム baby#3603 - Запущен')


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return # await ctx.send(embed=discord.Embed(description=f'❗ {ctx.author.name}, Команда не найдена!', colour = 0xFB9E14))
        elif isinstance(error, commands.MissingPermissions):
            return await ctx.send(embed=discord.Embed(description=f'❗ {ctx.author.name}, У бота недостаточно прав!\n'
            f'❗ Если это не модераторская команда: то значит у бота нету права управлением сообщениями или права на установку реакций.', colour = 0xFB9E14), delete_after = 7)
        elif isinstance(error, commands.MissingPermissions) or isinstance(error, discord.Forbidden):
            return await ctx.send(embed=discord.Embed(description=f'❗ {ctx.author.name}, У вас недостаточно прав!', colour = 0xFB9E14), delete_after = 3)
        elif isinstance(error, commands.BadArgument):
            if "Member" in str(error):
                if ctx.author.id == 646573856785694721:
                    ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=discord.Embed(description=f'❗ {ctx.author.name}, Пользователь не найден!', colour = 0xFB9E14), delete_after = 3)
            if "Guild" in str(error):
                if ctx.author.id == 646573856785694721:
                    ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=discord.Embed(description=f'❗ {ctx.author.name}, Сервер не найден!', colour = 0xFB9E14), delete_after = 3)
            else:
                if ctx.author.id == 646573856785694721:
                    ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=discord.Embed(description=f'❗ {ctx.author.name}, Введён неверный аргумент!', colour = 0xFB9E14), delete_after = 3)
        elif isinstance(error, commands.MissingRequiredArgument):
            if ctx.author.id == 646573856785694721:
                ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=discord.Embed(description=f'❗ {ctx.author.name}, Пропущен аргумент с названием {error.param.name}!', colour = 0xFB9E14), delete_after = 3)
        elif isinstance(error, commands.CommandOnCooldown):
            if ctx.author.id == 646573856785694721:
                ctx.command.reset_cooldown(ctx)
            await ctx.send(embed=discord.Embed(description=f'❗ {ctx.author.name}, Воу, Воу, Не надо так быстро использовать эту функцию.\n'
            f'❗ Подожди {error.retry_after:.2f} секунд и сможешь сделать это действие повторно'), delete_after = 5)
        else:
            # await ctx.send(embed=discord.Embed(description=f'❗ {ctx.author.name}, Произошла неизвестная ошибка. Напишите разработчику в личные сообщения для её устранения:\n> `Discord:` **dollar ム baby#3603**\n> [[В]Контайте](https://vk.com/norimyxxxo1702)'), delete_after = 5)
            raise error

def setup(bot):
    bot.add_cog(debug(bot))