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
form = db["forma"]
moder = db["moder"]
event = db["eventman"]
otdel = db["etdeli"]

dbd = cluster["RodinaBD"]
reports = dbd["reports"]

def setembed(title = None, thumb = None, footer = None, *, text):
    if title is None:
        embed = discord.Embed(description = f'{text}', colour=0xFB9E14)
    else:
        embed = discord.Embed(title = title, description = f'{text}', colour=0xFB9E14)
    if not thumb is None:
        embed.set_thumbnail(url = thumb)
    if footer == None:
        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
    else:
        embed.set_footer(text = f'{footer} | Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')

    return embed

class events(commands.Cog):
    """privats Cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        print('Rodina 04 | Event Manages by dollar ム baby#3603 - Запущен')

    '''
    !new_embed(nmb) + 
    !embed_text(etext) +
    !embed_name(ename) +
    !embed_thumbnail(ethumb) +
    !embed_image(eimage) +
    !embed_footer(efooter) +
    !embed_send(esend) +
    !embed_everyone(everyemb) +
    !embed_visual(evs) +
    !embed_help(ehelp) -
    !embed_use(euse) +
    !embed_color(ecolor) +
    !get_embed(gmb) +
    !my_embeds(myemb) +
    !embed_delete(edelete) - 
    '''

    @commands.command(aliases = ['nmb'])
    @commands.has_permissions(administrator = True)
    async def new_embed(self, ctx, *, name = None):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]

        if name == None:
            return await ctx.send(embed = setembed(text = f'❌ Вы не указали параметр `[название шаблона]`\n\n『🗓』**{prefix}new_embed`(nmb)`** - `Создать новый шаблон эмбеда`\n-- Пример использования: `{prefix}nmb Новости 11.05`'), delete_after = 5)

        otdel.insert_one({"guild": ctx.guild.id, "proverka": 1703, "name": name, "text": '-', "title": '-', "image": '-', "thumbnail": '-', "color": '-', "footer": '-', "everyone": 0, "goto": 0, "author": ctx.author.id, "active": 1, "number": len([i["name"] for i in otdel.find({"guild": ctx.guild.id, "proverka": 1703})]) + 1})
        return await ctx.send(embed = setembed(text = f'✅ Вы успешно создани новый шаблон `[{name}]`, он выбран **основным** по умолчанию.\n\n『🕵』 Для того что бы узнать информацию по его заполнению используйте команду: `{prefix}embed_use(euse)`\n『📋』 Список команд embed-шаблонов: `{prefix}embed_help(ehelp)`'), delete_after = 15)
   
    @commands.command(aliases = ['edelete'])
    @commands.has_permissions(administrator = True)
    async def embed_delete(self, ctx, amount: int = None):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]

        if otdel.count_documents({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Вы не имеете ни одного шаблона!\nДля того что бы его создать используйте `{prefix}new_embed(nmb)`'), delete_after = 5)
    
        if amount == None:
            return await ctx.send(embed = setembed(text = f'❌ Вы не указали параметр `[№ шаблона]`\n\n『🔳』**{prefix}embed_delete`(edelete)`** - `Удалить шаблон`\n-- Пример использования: `{prefix}edelete 1`'), delete_after = 5)

        if otdel.count_documents({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "number": int(amount)}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Шаблон под этим номером Вам не принадлежит\nДля того что бы посмотреть ваши шаблоны используйте команлу `{prefix}my_embeds(myemb)`'), delete_after = 5)

        n = otdel.find_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "number": int(amount)})
        message = await ctx.send(embed = setembed(text = f'❔ Вы действительно хотите удалить шаблон №{n["number"]}`({n["name"]})`\n\n**Для удаления нажмите** ✅\n**Для того что бы отменить действие -** ❌'))
        await message.add_reaction('✅')
        await message.add_reaction('❌')
        try:
            react, user = await self.bot.wait_for('reaction_add', timeout= 30.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
        except Exception:
            await ctx.send(embed = setembed(text = f'❌ Вы не успели принять решение, измения не были сохранены.'), delete_after = 5) 
            return await message.delete()
        else:
            await message.delete()
            if str(react.emoji) == '❌':
                return await ctx.send(embed = setembed(title = 'Отмена', text = f'❌ Вы отказались удалять шаблон'), delete_after = 5) 
            elif str(react.emoji) == '✅':
                otdel.delete_one({"_id": n["_id"]})
                return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы удалили шаблон №{n["number"]}`({n["name"]})`'), delete_after = 15) 
    
    @commands.command(aliases = ['etext'])
    @commands.has_permissions(administrator = True)
    async def embed_text(self, ctx, *, amount = None):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]

        if otdel.count_documents({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Вы не имеете ни одного шаблона!\nДля того что бы его создать используйте `{prefix}new_embed(nmb)`'), delete_after = 5)
    
        if amount == None:
            return await ctx.send(embed = setembed(text = f'❌ Вы не указали параметр `[текст]`\n\n『🔳』**{prefix}embed_text`(etext)`** - `Установить текст в embed-сообщение`\n-- Пример использования: `{prefix}etext Всем привет, сейчас я покажу Вам как работает система embed-сообщений!`'), delete_after = 5)

        n = otdel.find_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1})
        if not n["text"] == '-':
            message = await ctx.send(embed = setembed(text = f'❔ Текст embed-сообщения уже установлен:\n> `{n["text"]}\n\n**Если вы хотите изменить это значение - нажмите** ✅\n**Для того что бы оставить старое значение -** ❌'))
            await message.add_reaction('✅')
            await message.add_reaction('❌')
            try:
                react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
            except Exception:
                await ctx.send(embed = setembed(text = f'❌ Вы не успели принять решение, измения не были сохранены.'), delete_after = 5) 
                return await message.delete()
            else:
                await message.delete()
                if str(react.emoji) == '❌':
                    return await ctx.send(embed = setembed(title = 'Отмена', text = f'❌ Старая информация успешно сохранена.'), delete_after = 5) 
                elif str(react.emoji) == '✅':
                    otdel.update_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1}, {"$set": {"text": amount}})
                    return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили новый текст в embed-сообщение в шаблоне `[{n["name"]}]`:\n> {amount}'), delete_after = 15) 
        else:
            otdel.update_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1}, {"$set": {"text": amount}})
            return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили новый текст в embed-сообщение в шаблоне `[{n["name"]}]`:\n> {amount}'), delete_after = 15) 

    @commands.command(aliases = ['euse'])
    @commands.has_permissions(administrator = True)
    async def embed_use(self, ctx):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]   

        embed = discord.Embed(title = 'Информация о embed-системе', description = f'**Для редактирования шаблона Вам необходимо выбрать его основным при помощи команды `{prefix}get_embed(gmb)`**\n`[P.S]: После создания шаблона, он автоматически становится основным`\n\n**Заполнение `embed-системы`**\n**Команды используемые для этой структуры:**\n> 1. `{prefix}embed_name(ename) Новости Discord Сервера`\n> 2. `{prefix}embed_text(etext) Всем привет, сейчас я покажу Вам как работает система embed-сообщений!`\n> 3. `{prefix}embed_thumbnail(ethumb) -`\n-- Если вы указываете "-" вместо ссылки, будет использован аватар дискорд-сервера.\n> 4. `{prefix}embed_image(eimage) https://clck.ru/UkEeQ`\n-- Если Вы указываете "-" вместо ссылки, картинки в сообщении не будет.\n> 5. `{prefix}embed_color(ecolor) 0xFF0000`\n-- Если вы указываете "-" вместо кода цвета, будет использован оранжевый цвет.\n> 6. `{prefix}embed_send`', color = 0xFB9E14)
        embed.set_image(url = 'https://avatars.mds.yandex.net/get-pdb/4396727/c2019b21-9dc1-4d78-bd33-646cb1733fba/s1200')
        embed.set_thumbnail(url = ctx.guild.icon_url)
        embed.set_footer(text = 'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        await ctx.send(embed = embed)

    @commands.command(aliases = ['efooter'])
    @commands.has_permissions(administrator = True)
    async def embed_footer(self, ctx, *, amount = None):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]

        if otdel.count_documents({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Вы не имеете ни одного шаблона!\nДля того что бы его создать используйте `{prefix}new_embed(nmb)`'), delete_after = 5)
    
        if amount == None:
            return await ctx.send(embed = setembed(text = f'❌ Вы не указали параметр `[текст]`\n\n『🔳』**{prefix}embed_footer`(efooter)`** - `Установить подпись в embed-сообщение`\n-- Пример использования: `{prefix}efooter Support Team by dollar ム baby#3603`'), delete_after = 5)

        n = otdel.find_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1})
        if not n["footer"] == '-':
            message = await ctx.send(embed = setembed(text = f'❔ Подпись embed-сообщения уже установлена:\n> `{n["footer"]}\n\n**Если вы хотите изменить это значение - нажмите** ✅\n**Для того что бы оставить старое значение -** ❌'))
            await message.add_reaction('✅')
            await message.add_reaction('❌')
            try:
                react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
            except Exception:
                await ctx.send(embed = setembed(text = f'❌ Вы не успели принять решение, измения не были сохранены.'), delete_after = 5) 
                return await message.delete()
            else:
                await message.delete()
                if str(react.emoji) == '❌':
                    return await ctx.send(embed = setembed(title = 'Отмена', text = f'❌ Старая информация успешно сохранена.'), delete_after = 5) 
                elif str(react.emoji) == '✅':
                    otdel.update_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1}, {"$set": {"footer": amount}})
                    return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили новую подпись в embed-сообщение в шаблоне `[{n["name"]}]`:\n> {amount}'), delete_after = 15) 
        else:
            otdel.update_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1}, {"$set": {"footer": amount}})
            return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили новую подпись в embed-сообщение в шаблоне `[{n["name"]}]`:\n> {amount}'), delete_after = 15) 

    @commands.command(aliases = ['myemb'])
    @commands.has_permissions(administrator = True)
    async def my_embeds(self, ctx):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]

        if otdel.count_documents({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Вы не имеете ни одного шаблона!\nДля того что бы его создать используйте `{prefix}new_embed(nmb)`'), delete_after = 5)
        
        str_a = ''.join([f'> №{i["number"]} `- {i["name"]}`\n' for i in otdel.find({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id})])
        message = await ctx.send(embed = setembed(title = f'Список шаблонов пользователя', thumb = ctx.guild.icon_url, footer = '❌ - Закрыть', text = f'Список ваших шаблонов embed-сообщений:\n{str_a}\n**Для выбора шаблона используйте команду:** `{prefix}get_embed(gmd) [№ шаблона]`'))
        await message.add_reaction('❌')
        try:
            react, user = await self.bot.wait_for('reaction_add', timeout= 120.0, check= lambda react, user: user == ctx.author and react.emoji in ['❌'])
        except Exception:
            return await message.delete()
        else:
            if str(react.emoji) == '❌':
                return await message.delete()

    @commands.command(aliases = ['gmb'])
    @commands.has_permissions(administrator = True)
    async def get_embed(self, ctx, amount: int = None):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]

        if otdel.count_documents({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Вы не имеете ни одного шаблона!\nДля того что бы его создать используйте `{prefix}new_embed(nmb)`'), delete_after = 5)

        if amount == None:
            return await ctx.send(embed = setembed(text = f'❌ Вы не указали параметр `[№ шаблона]`\n\n『🔳』**{prefix}get_embed`(gmb)`** - `Выбрать основной шаблон`\n-- Пример использования: `{prefix}gmb 1`'), delete_after = 5)

        if otdel.count_documents({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "number": int(amount)}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Шаблон под этим номером Вам не принадлежит\nДля того что бы посмотреть ваши шаблоны используйте команлу `{prefix}my_embeds(myemb)`'), delete_after = 5)

        otdel.update_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1}, {"$set": {"active": 0}})
        otdel.update_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "number": int(amount)}, {"$set": {"active": 1}})

        n = otdel.find_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1})
        thumburl, title, clr, footer, text, imageurl, upom, chan = 'Не установлено' if n["thumbnail"] == '-' else ["thumbnail"], 'Не установлен' if n["title"] == '-' else n["title"], 'Не установлен' if n["color"] == '-' else n["color"], 'Не установлена' if n["footer"] == '-' else n["footer"], 'Не установлен' if n["text"] == '-' else n["text"], 'Не установлено' if n["image"] == '-' else n["image"], 'Выключено' if n["everyone"] == 0 else 'Включено', 'Не установлен' if n["goto"] == 0 else f'#{self.bot.get_channel(n["goto"]).name}'
        message = await ctx.send(embed = setembed(title = 'Успешно!', thumb = ctx.guild.icon_url, footer = '❌ - Закрыть', text = f'✅ Вы выбрали шаблон №{n["number"]}`[{n["name"]}]` основным\n\n**Его настройки:**\n> `Заголовок:` {title}\n> `Боковое изображение:` {thumburl}\n> `Изображение:` {imageurl}\n> `Подпись:` {footer}\n> `Цвет сообщения:` {clr}\n> `Упоминание @everyone:` {upom}\n> `Канал отправления:` {chan}\n> `Текст сообщения:` {text}'), delete_after = 120) 
        await message.add_reaction('❌')
        try:
            react, user = await self.bot.wait_for('reaction_add', timeout= 120.0, check= lambda react, user: user == ctx.author and react.emoji in ['❌'])
        except Exception:
            return await message.delete()
        else:
            if str(react.emoji) == '❌':
                return await message.delete()
    
    @commands.command(aliases = ['everyemb'])
    @commands.has_permissions(administrator = True)
    async def embed_everyone(self, ctx, amount: int = None):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]

        if otdel.count_documents({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Вы не имеете ни одного шаблона!\nДля того что бы его создать используйте `{prefix}new_embed(nmb)`'), delete_after = 5)
    
        if amount == None or not amount in [0, 1]:
            return await ctx.send(embed = setembed(text = f'❌ Вы не указали параметр `[значение | 1 - С упоминанием, 0 - Без упоминания @everyone]`\n\n『🔳』**{prefix}embed_everyone`(everyemb)`** - `Установить значение упоминания @everyone`\n-- Пример использования: `{prefix}everyemb 1`'), delete_after = 5)

        otdel.update_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1}, {"$set": {"everyone": int(amount)}})
        answer = {0: "Не упоминать", 1: "Упоминать"}
        return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы значение упоминания @everyone на `[{answer[int(amount)]}]`'), delete_after = 15)

    @commands.command(aliases = ['ename'])
    @commands.has_permissions(administrator = True)
    async def embed_name(self, ctx, *, amount = None):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]

        if otdel.count_documents({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Вы не имеете ни одного шаблона!\nДля того что бы его создать используйте `{prefix}new_embed(nmb)`'), delete_after = 5)
    
        if amount == None:
            return await ctx.send(embed = setembed(text = f'❌ Вы не указали параметр `[ссылка]`\n\n『🔳』**{prefix}embed_name`(ethumb)`** - `Установить заголовок embed-сообщения`\n-- Пример использования: `{prefix}ename Новости Discord Сервера` | `"-" вместо заголовка будет использован как название сервера`'), delete_after = 5)

        n = otdel.find_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1})
        if not n["title"] == '-':
            message = await ctx.send(embed = setembed(text = f'❔ Заголовок embed-сообщения уже установлен:\n> `{n["title"]}\n\n**Если вы хотите изменить это значение - нажмите** ✅\n**Для того что бы оставить старое значение -** ❌'))
            await message.add_reaction('✅')
            await message.add_reaction('❌')
            try:
                react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
            except Exception:
                await ctx.send(embed = setembed(text = f'❌ Вы не успели принять решение, измения не были сохранены.'), delete_after = 5) 
                return await message.delete()
            else:
                await message.delete()
                if str(react.emoji) == '❌':
                    return await ctx.send(embed = setembed(title = 'Отмена', text = f'❌ Старая информация успешно сохранена.'), delete_after = 5) 
                elif str(react.emoji) == '✅':
                    otdel.update_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1}, {"$set": {"title": amount}})
                    return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили новый заголовок аватар embed-сообщения в шаблоне `[{n["name"]}]`:\n> {amount}'), delete_after = 15) 
        else:
            otdel.update_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1}, {"$set": {"title": amount}})
            return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили новый боковой заголовок embed-сообщения в шаблоне `[{n["name"]}]`:\n> {amount}'), delete_after = 15) 

    @commands.command(aliases = ['ethumb'])
    @commands.has_permissions(administrator = True)
    async def set_thumbnail(self, ctx, amount = None):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]

        if otdel.count_documents({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Вы не имеете ни одного шаблона!\nДля того что бы его создать используйте `{prefix}new_embed(nmb)`'), delete_after = 5)
    
        if amount == None:
            return await ctx.send(embed = setembed(text = f'❌ Вы не указали параметр `[ссылка]`\n\n『🔳』**{prefix}embed_thumbnail`(ethumb)`** - `Установить боковую фотографию embed-сообщения`\n-- Пример использования: `{prefix}ethumb https://clck.ru/UkEeQ` | `"-" вместо ссылки будет использовать аватар сервера`'), delete_after = 5)

        n = otdel.find_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1})
        if not n["thumbnail"] == '-':
            message = await ctx.send(embed = setembed(text = f'❔ Боковой аватар embed-сообщения уже установлен:\n> `{n["thumbnail"]}\n\n**Если вы хотите изменить это значение - нажмите** ✅\n**Для того что бы оставить старое значение -** ❌'))
            await message.add_reaction('✅')
            await message.add_reaction('❌')
            try:
                react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
            except Exception:
                await ctx.send(embed = setembed(text = f'❌ Вы не успели принять решение, измения не были сохранены.'), delete_after = 5) 
                return await message.delete()
            else:
                await message.delete()
                if str(react.emoji) == '❌':
                    return await ctx.send(embed = setembed(title = 'Отмена', text = f'❌ Старая информация успешно сохранена.'), delete_after = 5) 
                elif str(react.emoji) == '✅':
                    otdel.update_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1}, {"$set": {"thumbnail": amount}})
                    return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили новый боковой аватар embed-сообщения в шаблоне `[{n["name"]}]`:\n> {amount}'), delete_after = 15) 
        else:
            otdel.update_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1}, {"$set": {"thumbnail": amount}})
            return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили новый боковой аватар embed-сообщения в шаблоне `[{n["name"]}]`:\n> {amount}'), delete_after = 15) 

    @commands.command(aliases = ['eimage'])
    @commands.has_permissions(administrator = True)
    async def embed_image(self, ctx, amount = None):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]

        if otdel.count_documents({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Вы не имеете ни одного шаблона!\nДля того что бы его создать используйте `{prefix}new_embed(nmb)`'), delete_after = 5)
    
        if amount == None:
            return await ctx.send(embed = setembed(text = f'❌ Вы не указали параметр `[ссылка]`\n\n『🔳』**{prefix}embed_image`(eimage)`** - `Установить изображение в embed-сообщение`\n-- Пример использования: `{prefix}eimage https://clck.ru/UkEeQ` | `"-" вместо ссылки уберёт картинку из сообщения`'), delete_after = 5)

        n = otdel.find_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1})
        if not n["image"] == '-':
            message = await ctx.send(embed = setembed(text = f'❔ Боковой аватар embed-сообщения уже установлен:\n> `{n["image"]}\n\n**Если вы хотите изменить это значение - нажмите** ✅\n**Для того что бы оставить старое значение -** ❌'))
            await message.add_reaction('✅')
            await message.add_reaction('❌')
            try:
                react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
            except Exception:
                await ctx.send(embed = setembed(text = f'❌ Вы не успели принять решение, измения не были сохранены.'), delete_after = 5) 
                return await message.delete()
            else:
                await message.delete()
                if str(react.emoji) == '❌':
                    return await ctx.send(embed = setembed(title = 'Отмена', text = f'❌ Старая информация успешно сохранена.'), delete_after = 5) 
                elif str(react.emoji) == '✅':
                    otdel.update_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1}, {"$set": {"image": amount}})
                    return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили новое изображение в embed-сообщение в шаблоне `[{n["name"]}]`:\n> {amount}'), delete_after = 15)  
        else:
            otdel.update_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1}, {"$set": {"image": amount}})
            return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили новое изображение в embed-сообщение в шаблоне `[{n["name"]}]`:\n> {amount}'), delete_after = 15) 

    @commands.command(aliases = ['ecolor'])
    @commands.has_permissions(administrator = True)
    async def embed_color(self, ctx, *, amount = None):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]

        if otdel.count_documents({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Вы не имеете ни одного шаблона!\nДля того что бы его создать используйте `{prefix}new_embed(nmb)`'), delete_after = 5)
    
        if amount == None:
            return await ctx.send(embed = setembed(text = f'❌ Вы не указали параметр `[цвет]`\n\n『 🌹 』**{prefix}embed_color(ecolor)** - `Установить цвет embed-сообщения`\nПример использования: `{prefix}set_embed 0xFB9E14`'), delete_after = 5)

        otdel.update_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1}, {"$set": {"color": amount}})
        return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили `[{amount}]`, как цвет embed-сообщения.'), delete_after = 15) 

    @commands.command(aliases = ['ehelp'])
    @commands.has_permissions(administrator = True)
    async def embed_help(self, ctx):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]

        embed = discord.Embed(title = 'Настройка мероприятия', description = f'**Команды доступные для Вас:**\n> 『⏳』 `{prefix}new_embed(nmb)` - Создать embed-шаблон\n> 『🗓』 `{prefix}embed_text(etext)` - Установить текст embed-сообщения\n-- Пример использования: `{prefix}etext Всем привет, сейчас я покажу Вам как работает система embed-сообщений!`\n> 『📋』 `{prefix}embed_use(euse)` - Схема использования embed-системы.\n> 『🔳』 `{prefix}embed_footer(efooter)` - Установить подпись в embed-сообщение\n-- Пример использования: `{prefix}efooter Support Team by dollar ム baby#3603`\n> 『🪁』 `{prefix}embed_image(eimage)` - Установить изображение в embed-сообщение\n-- Пример использования: `{prefix}eimage https://clck.ru/UkEeQ` | `"-" вместо ссылки уберёт картинку из сообщения`\n> 『🚩』 `{prefix}embed_everyone(everyemb)` - Установить значение упоминания @everyone\n-- Пример использования: `{prefix}everyemb 1 | [значение | 1 - С упоминанием, 0 - Без упоминания @everyone]`\n> 『🌟』 `{prefix}embed_thumbnail(ethumb)` - Установить боковую фотографию embed-сообщения\n-- Пример использования: `{prefix}ethumb https://clck.ru/UkEeQ` | `"-" вместо ссылки будет использовать аватар сервера`\n\n> 『🎭』 `{prefix}embed_visual(evs)` - Посмотреть внешний вид embed-шаблона\n> 『📌』 `{prefix}get_embed(gmb)` - Выбрать необходимый шаблон\n> 『🕵』 `{prefix}my_embeds(myemb)` - Посмотреть список ваших шаблонов\n> 『 🌹 』 `{prefix}embed_color(ecolor)` - Установить цвет embed-сообщения\n> 『🔔』 `{prefix}embed_send(esend)` - Отправить embed-сообщение в канал\n> 『🔒』 `{prefix}embed_delete(edelete)` - Удалить шаблон embed-сообщения', color = 0xFB0E14)
        embed.set_thumbnail(url = ctx.guild.icon_url)
        embed.set_footer(text = f'❌ - Закрыть | Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        message = await ctx.send(embed = embed)
        await message.add_reaction('❌')
        try:
            react, user = await self.bot.wait_for('reaction_add', timeout= 120.0, check= lambda react, user: user == ctx.author and react.emoji in ['❌'])
        except Exception:
            return await message.delete()
        else:
            if str(react.emoji) == '❌':
                return await message.delete()
    
    @commands.command(aliases = ['evs'])
    @commands.has_permissions(administrator = True)
    async def embed_visual(self, ctx):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]

        if otdel.count_documents({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Вы не имеете ни одного шаблона!\nДля того что бы его создать используйте `{prefix}new_embed(nmb)`'), delete_after = 5)

        n = otdel.find_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1})
        thumburl, title, clr, footer, text = ctx.guild.icon_url if n["thumbnail"] == '-' else ["thumbnail"], ctx.guild.name if n["title"] == '-' else n["title"], '0xFB9E14' if n["color"] == '-' else n["color"], 'Support Team by dollar ム baby#3603' if n["footer"] == '-' else n["footer"], 'Не установлен' if n["text"] == '-' else n["text"]
        embed2 = discord.Embed(title = title, description = text, color = int(clr, 16))
        if not n["image"] == '-':
            embed2.set_image(url = n["image"])
        embed2.set_thumbnail(url = thumburl)
        embed2.set_footer(text = f'❌ - Закрыть | {footer}', icon_url = ctx.guild.icon_url)
        message = await ctx.send(embed = embed2)
        await message.add_reaction('❌')
        try:
            react, user = await self.bot.wait_for('reaction_add', timeout= 120.0, check= lambda react, user: user == ctx.author and react.emoji in ['❌'])
        except Exception:
            return await message.delete()
        else:
            if str(react.emoji) == '❌':
                return await message.delete()
    
    @commands.command(aliases = ['esend'])
    @commands.has_permissions(administrator = True)
    async def embed_send(self, ctx, *, amount = None):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]

        if otdel.count_documents({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Вы не имеете ни одного шаблона!\nДля того что бы его создать используйте `{prefix}new_embed(nmb)`'), delete_after = 5)

        n = otdel.find_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1})
        if n["text"] == '-':
            return await ctx.send(embed = setembed(text = f'❌ Вам необходимо установить `текст` embed-сообщения командой `{prefix}embed_text(etext)`'), delete_after = 5)

        n = otdel.find_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1})
        thumburl, title, clr, footer = ctx.guild.icon_url if n["thumbnail"] == '-' else ["thumbnail"], ctx.guild.name if n["title"] == '-' else n["title"], '0xFB9E14' if n["color"] == '-' else n["color"], 'Support Team by dollar ム baby#3603' if n["footer"] == '-' else n["footer"]
        embed2 = discord.Embed(title = title, description = n["text"], color = int(clr, 16))
        if not n["image"] == '-':
            embed2.set_image(url = n["image"])
        embed2.set_thumbnail(url = thumburl)
        embed2.set_footer(text = footer, icon_url = ctx.guild.icon_url)
        message = await ctx.send(f'**Проверьте данные своего embed-сообщения и нажмите на ✅ для отправки сообщения**\n**Для отмены - ❌**', embed = embed2)
        await message.add_reaction('✅')
        await message.add_reaction('❌')
        try:
            react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
        except Exception:
            return await message.delete()
        else:
            await message.delete()
            if str(react.emoji) == '❌':
                return await ctx.send(embed = discord.Embed(description = f'Вы успешно отменили действие!', color = 0xFB9E14), delete_after = 3)
            elif str(react.emoji) == '✅':
                if n["goto"] == 0:
                    ever = '.' if n["everyone"] == 0 else '.\n『📢』Внимание, у вас установлено упоминание всех пользователей через @everyone'
                    message = await ctx.send(embed = setembed(text = f'Пожалуйста, выберите канал в который хотите отправить Ваше сообщение{ever}\n\n> 📋 - `#『`📋`』новости-сервера`\n> 📢 - `#『`📢`』новости-discord`\n> 🚩 - `#『`🚩`』information`'))
                    await message.add_reaction('📋')
                    await message.add_reaction('📢')
                    await message.add_reaction('🚩')
                    try:
                        react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in ['📋', '📢', '🚩'])
                    except Exception:
                        return await message.delete()
                    else:
                        await message.delete()
                        if str(react.emoji) == '📋':
                            otdel.update_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1}, {"$set": {"goto": 477875131302019105}})
                        elif str(react.emoji) == '📢':
                            otdel.update_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1}, {"$set": {"goto": 800038891611619388}})
                        elif str(react.emoji) == '🚩':
                            otdel.update_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1}, {"$set": {"goto": 816051676846358569}})

                n = otdel.find_one({"guild": ctx.guild.id, "proverka": 1703, "author": ctx.author.id, "active": 1})
                channel = self.bot.get_channel(n["goto"])
                if n["everyone"] == 0:
                    await channel.send(embed = embed2)
                    return await ctx.send(embed = setembed(title = 'Успешно!', text = f'『✅』 Вы успешно отправили своё embed-сообщение в текстовый канал `#{channel.name}`'), delete_after = 15) 
                elif n["everyone"] == 1:
                    await channel.send('@everyone', embed = embed2)
                    return await ctx.send(embed = setembed(title = 'Успешно!', text = f'『✅』 Вы успешно отправили своё embed-сообщение с упоминанием @everyone в текстовый канал `#{channel.name}`'), delete_after = 15) 

                   


    @commands.command(aliases = ['eon', 'ивент_старт'])
    async def event_on(self, ctx):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]

        if not discord.utils.get(ctx.guild.roles, id = 843138403298312212) in ctx.author.roles:
            return await ctx.send(embed = setembed(text = f'❌ Доступ к использованию этой команды ограничен.'), delete_after = 5)

        if event.count_documents({"guild": ctx.guild.id, "moderid": ctx.author.id}) > 0:
            if event.find_one({"guild": ctx.guild.id, "moderid": ctx.author.id})["channelid"] in [i.id for i in ctx.guild.text_channels]:
                return await ctx.send(embed = setembed(text = f'❌ Нельзя создавать больше 1-го канала для мероприятия.\nЗавершите предыдущее мероприятие командой `{prefix}event_off(eoff|ивент_стоп)` в канале <#{event.find_one({"guild": ctx.guild.id, "moderid": ctx.author.id})["channelid"]}>'), delete_after = 7)
            else:
                event.delete_one({"guild": ctx.guild.id, "moderid": ctx.author.id})
        mainCategory = discord.utils.get(ctx.guild.categories, id=840816866666348554)
        channel = await ctx.guild.create_text_channel(name=f"Канал настройки мероприятия",category = mainCategory)
        event.insert_one({"guild": ctx.guild.id, "channelid": channel.id, "moderid": ctx.author.id, "eventname": "-", "eventtime": "-", "eventdate": "-", "eventtext":"-", "eventpriz":"-", "roleorg": 0, "rolemember": 0, "evoice": 0, "etext": 0, "output": 0, "organize": 0, "embedcolor": "-", "theme": "-", "messageid": 0})
        await channel.send(embed = setembed(title = 'Настройка мероприятия', text = f'Приветствую тебя, юный модератор!\n`Этот канал создан специально для настройки Вашего мероприятия.`\n\n**Команды доступные для Вас:**\n> 『⏳』 `{prefix}eventtime(evt|инвент_время)` - Установить время проведения мероприятия\n-- Пример использования: `{prefix}eventtime 15:30`\n> 『🗓』 `{prefix}eventdate(evd|ивент_дата)` - Установить дату проведения мероприятия\n-- Пример использования: `{prefix}eventdate 3 мая 2021 года`\n> 『📋』 `{prefix}eventname(enm|инвент_название)` - Установить название ивента\n-- Пример использования: `{prefix}eventname Улётная Викторина`\n> 『🔳』 `{prefix}eventtext(evtx|ивент_текст)` - Установить текст эвента`(описание, ссылки, подробности и т.д)`\n> 『🪁』 `{prefix}setgive(sgv|ивент_призы)` - Установить награду за победу в мероприятии\n-- Пример использования: `{prefix}setgive 1 место - 5 долларов, 2 место - 3 доллара, 3 место - 1 доллар`\n> 『🚩』 `{prefix}eventdesc(evds|ивент_тематика)` - Установить тематику мероприяти\n-- Пример использования: `{prefix}eventdesc Эрудиция`\n> 『🌟』 `{prefix}event_role(evr|ивент_роль)` - Установить роль огранизатора мероприятия\n-- Пример использования: `{prefix}eventrole` <@&843138403298312212> `| {prefix}eventrole 0` для того что бы создать новую\n\n> 『💬』 `{prefix}event_create_text(cht|ивент_канал_т)` - Создать текстовый канал для мероприятия\n> 『 🔈』 `{prefix}event_create_voice(chv|ивент_канал_г)` - Создать голосовой канал для мероприятия\n> 『🕵』 `{prefix}set_organizer(setorg|организатор_назначить)` - Назначить организатора мероприятия\n> 『 🌹 』 `{prefix}set_embed(eve|ивент_цвет)` - Установить цвет embed-сообщения\n> 『🔔』 `{prefix}publish_event(pbe|ивент_начать)` - Публикация ивента\n> 『🎭』 `{prefix}event_visual(evis|предпросмотр)`\n> 『🔒』 `{prefix}event_off(eoff|ивент_стоп)` - Прекратить настройку мероприятия'))

        embed = discord.Embed(title = 'Пример использования', description = f'**Ниже представлен пример отправки сообщения от бота.**\n**Команды используемые для этой структуры:**\n> 1. `{prefix}eventtime 16:00`\n> 2. `{prefix}eventdate 09 Апрель 2021`\n> 3. `{prefix}eventname Новогодняя Викторина`\n> 4. `{prefix}eventtext Новогдняя викторина, на которой вы сможете получить ценные призы и провести время в компании умных и эрудированных людей...`\n> 5. `{prefix}event_create_text` `『`🔈`』Викторина`\n> 6. `{prefix}publish_event`', color = 0xFB9E14)
        embed.set_image(url = 'https://avatars.mds.yandex.net/get-pdb/2821050/9cda5d6d-e458-4fbf-a00a-9fc7832895d1/s1200')
        embed.set_thumbnail(url = ctx.guild.icon_url)
        embed.set_footer(text = 'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        await channel.send(embed = embed)
        await ctx.send(embed = setembed(text = f'✅ Для настройки Вашего мероприятия был создан текстовый канал: {channel.mention}`(#{channel.name})`\n`Дальнейшая настройка мероприятия должна проходить в нём.`'), delete_after = 10)

    ''' 
    !eventtime(evt|инвент_время) +
    !eventdate(evd|ивент_дата) +
    !eventname(enm|инвент_название) +
    !eventtext(evtx|ивент_текст) +
    !eventdesc(evds|ивент_тематика) +
    !setgive(sgv|ивент_призы) +
    !event_role(evr|ивент_роль) +
    !event_create_text(cht|ивент_канал_т) +
    !event_create_voice(chv|ивент_канал_г) +
    !set_organizer(setorg|организатор_назначить) +
    !event_visual(evis|предпросмотр) +
    !event_off(eoff|ивент_стоп) +
    !event_on(eon|ивент_старт) +
    !set_embed(eve|ивент_цвет) +

    !publish_event(pbe|ивент_начать) -
    Запись в список
    Сообщения + поздравления  + коины 
    '''
    
    @commands.command(aliases = ['pbe', 'ивент_начать'])
    async def publish_event(self, ctx, amount = None):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
        if not discord.utils.get(ctx.guild.roles, id = 843138403298312212) in ctx.author.roles:
            return await ctx.send(embed = setembed(text = f'❌ Доступ к использованию этой команды ограничен.'), delete_after = 5)

        if event.count_documents({"guild": ctx.guild.id, "channelid": ctx.channel.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Данный канал не предназначен для настройки мероприятия!\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["moderid"] != ctx.author.id:
            return await ctx.send(embed = setembed(text = f'❌ Вы не являетесь организатором мероприятия в этом канале.\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)
        
        nat = event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})

        if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventname"] == '-':
            return await ctx.send(embed = setembed(text = f'❌ Вам необходимо установить `название` мероприятия командой `{prefix}eventname(enm|инвент_название)`'), delete_after = 5)

        if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventdate"] == '-':
            return await ctx.send(embed = setembed(text = f'❌ Вам необходимо установить `дату проведения` мероприятия командой `{prefix}eventdate(evd|ивент_дата)`'), delete_after = 5)
        
        if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventtime"] == '-':
            return await ctx.send(embed = setembed(text = f'❌ Вам необходимо установить `время проведения` мероприятия командой `{prefix}eventtime(evt|инвент_время)`'), delete_after = 5)

        if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["organize"] == 0:
            return await ctx.send(embed = setembed(text = f'❌ Вам необходимо установить `огранизатора` мероприятия командой `{prefix}set_organizer(setorg|организатор_назначить)`'), delete_after = 5)

        if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventtext"] == '-':
            return await ctx.send(embed = setembed(text = f'❌ Вам необходимо установить `суть` мероприятия командой `{prefix}eventtext(evtx|ивент_текст)`'), delete_after = 5)

        if nat["rolemember"] == 0:
            clr = '0xFB9E14' if nat["embedcolor"] == '-' else nat["embedcolor"]
            try:
                role = await ctx.guild.create_role(name = f'Участник мероприятия "{event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventname"]}"')
            except:
                role = await ctx.guild.create_role(name = f'Участник мероприятия')
            await role.edit(colour = int(clr, 16))
            await ctx.guild.edit_role_positions(positions = {role: 5})
            event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"rolemember": role.id}})

        nat = event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})
        if not nat["rolemember"] in [i.id for i in ctx.guild.roles]:
            clr = '0xFB9E14' if nat["embedcolor"] == '-' else nat["embedcolor"]
            try:
                role = await ctx.guild.create_role(name = f'Участник мероприятия "{event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventname"]}"')
            except:
                role = await ctx.guild.create_role(name = f'Участник мероприятия')
            await role.edit(colour = int(clr, 16))
            await ctx.guild.edit_role_positions(positions = {role: 5})
            event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"rolemember": role.id}})

        nat = event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})

        if nat["evoice"] == 0:
            mainCategory = discord.utils.get(ctx.guild.categories, id=840816866666348554)
            channel = await ctx.guild.create_text_channel(name=f'{event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventname"]}', category = mainCategory)
            role = discord.utils.get(ctx.guild.roles, id = nat["rolemember"])
            await channel.set_permissions(role, view_channel = True, speak = True, connect = True)
            event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"etext": channel.id}})

        nat = event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})

        if nat["etext"] == 0:
            mainCategory = discord.utils.get(ctx.guild.categories, id=840816866666348554)
            channel = await ctx.guild.create_voice_channel(name=f'{event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventname"]}', category = mainCategory)
            await channel.set_permissions(ctx.guild.default_role, view_channel = True, send_messages = False, read_message_history = True, read_messages = True)
            event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"evoice": channel.id}})

        nat = event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})

        if nat["roleorg"] == 0:
            try:
                role = await ctx.guild.create_role(name = f'Организатор мероприятия "{event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventname"]}"')
            except:
                role = await ctx.guild.create_role(name = f'Организатор мероприятия')
            await role.edit(colour = 0x08ff20)
            await ctx.guild.edit_role_positions(positions = {role: 13})
            event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"roleorg": role.id}})
        
        nat = event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})
        if not nat["roleorg"] in [i.id for i in ctx.guild.roles]:
            try:
                role = await ctx.guild.create_role(name = f'Организатор мероприятия "{event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventname"]}"')
            except:
                role = await ctx.guild.create_role(name = f'Организатор мероприятия')
            await role.edit(colour = 0x08ff20)
            await ctx.guild.edit_role_positions(positions = {role: 13})
            event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"roleorg": role.id}})

        nat = event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})

        try:
            await discord.utils.get(ctx.guild.members, id = nat["organize"]).add_roles(discord.utils.get(ctx.guild.roles, id = nat["roleorg"]))
        except:
            pass

        nat = event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})
        name, org, site, ecolor = 'Не заполнено' if nat["eventname"] == '-' else nat["eventname"], 'Не указан' if nat["organize"] == 0 else f'{discord.utils.get(ctx.guild.members, id = nat["organize"]).mention}`({discord.utils.get(ctx.guild.members, id = nat["organize"])})`', 'Не установлена' if nat["eventtext"] == '-' else nat["eventtext"], '0xFB9E14' if nat["embedcolor"] == '-' else nat["embedcolor"]
        date, times, chan, thems = 'Дата не установлена' if nat["eventdate"] == '-' else nat["eventdate"], 'Время не установлено' if nat["eventtime"] == '-' else nat["eventtime"], 'Не установлен' if nat["etext"] == 0 else f'#{self.bot.get_channel(nat["etext"]).name}', 'Не установлена' if nat["theme"] == '-' else nat["theme"]
        embed = discord.Embed(title = f'Мероприятие: {name}', description = f'**Организатор:** {org}\n**Название мероприятия:** `{name}`\n\n**Тематика мероприятия:** {thems}\n**Суть мероприятия:**\n> `{site}`', color = int(ecolor, 16), timestamp = ctx.message.created_at)
        embed.add_field(name="‎‎‎‎", value="‎", inline=True)
        embed.add_field(name = f'🗓 {date}', value = '✅ __Буду точно__ `(0)`', inline = False)
        embed.add_field(name="‎‎‎‎", value="‎", inline=True)
        embed.add_field(name = f'⏰ {times} МСК', value = '❔ __Возможно буду__ `(0)`', inline = False)
        embed.add_field(name="‎‎‎‎", value="‎", inline=True)
        embed.add_field(name = f'{chan}', value = '❌ __Без меня__ `(0)`', inline = False)
        embed.set_thumbnail(url = ctx.guild.icon_url)
        embed.set_footer(text = '❌ - Закрыть | Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        message = await self.bot.get_channel(840934012637020190).send('@everyone', embed = embed)
        await message.add_reaction('✅')
        await message.add_reaction('❔')
        await message.add_reaction('❌')
        event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"messageid": message.id}})
        event.insert_one({"guild_id": ctx.guild.id, "proverka": 1703, "id": message.id, "lenmemberaccept": 0, "lenmemberdecline": 0, "lenmembermaybe": 0, "accept": [0], "decline": [0], "maybe": [0]})

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        if guild == None:
            return
        if not payload.guild_id == 477547500232769536:
            return

        user = self.bot.get_user(payload.user_id)
        if user.bot:
            pass
        else:
            channel = self.bot.get_channel(payload.channel_id)
            if not channel.id == 840934012637020190:
                return
            message = await channel.fetch_message(payload.message_id)
            if not message.id in [i["id"] for i in event.find({"guild_id": guild.id, "proverka": 1703})]:
                return
            memb = payload.member
            emoji = str(payload.emoji)
            if emoji == '✅':
                if memb.id in [i for i in event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["decline"]]:
                    return memb.send(embed = setembed(title = 'Ошибка доступа', thumb = guild.icon_url, text = '❌ К сожалению, вы не сможете учавствовать в данном мероприятии так как отказались от участия в нём ранее, ожидайте следующего мероприятия.'))
                nat = event.find_one({"guild": guild.id, "messageid": message.id})
                mas = [i for i in event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["accept"]]
                if memb.id in mas:
                    return
                mas.append(memb.id)
                event.update_one({"guild_id": guild.id, "id": message.id, "proverka": 1703}, {"$set": {"accept": mas, "lenmemberaccept": event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["lenmemberaccept"] + 1}}, upsert = True)
                if memb.id in [i for i in event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["maybe"]]:
                    mas2 = [i for i in event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["maybe"]]
                    mas2.remove(memb.id)
                    event.update_one({"guild_id": guild.id, "id": message.id, "proverka": 1703}, {"$set": {"maybe": mas2, "lenmembermaybe": event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["lenmembermaybe"] - 1}}, upsert = True)
                try:
                    await memb.send(embed = setembed(title = 'Участие в мероприятии', thumb = guild.icon_url, text = f'Вы успешно записаны в список участников мероприятия "`{nat["eventname"]}`" на сервере `{self.bot.get_guild(nat["guild"]).name}`\nСледите за новостями в канале `#{self.bot.get_channel(840934012637020190).name}`.\n\n`Дата проведения:` {nat["eventdate"]}\n`Время проведения:` {nat["eventtime"]} по московскому часовому поясу'))
                except:
                    pass
                
                try:
                    await memb.add_roles(discord.utils.get(guild.roles, id = nat["rolemember"]))
                except:
                    pass
                name, org, site, ecolor = 'Не заполнено' if nat["eventname"] == '-' else nat["eventname"], 'Не указан' if nat["organize"] == 0 else f'{discord.utils.get(guild.members, id = nat["organize"]).mention}`({discord.utils.get(guild.members, id = nat["organize"])})`', 'Не установлена' if nat["eventtext"] == '-' else nat["eventtext"], '0xFB9E14' if nat["embedcolor"] == '-' else nat["embedcolor"]
                date, times, chan, thems = 'Дата не установлена' if nat["eventdate"] == '-' else nat["eventdate"], 'Время не установлено' if nat["eventtime"] == '-' else nat["eventtime"], 'Не установлен' if nat["etext"] == 0 else f'#{self.bot.get_channel(840934012637020190).name}', 'Не установлена' if nat["theme"] == '-' else nat["theme"]
                embed = discord.Embed(title = f'Мероприятие: {name}', description = f'**Организатор:** {org}\n**Название мероприятия:** `{name}`\n\n**Тематика мероприятия:** {thems}\n**Суть мероприятия:**\n> `{site}`', color = int(ecolor, 16), timestamp = message.created_at)
                embed.add_field(name="‎‎‎‎", value="‎", inline=True)
                embed.add_field(name = f'🗓 {date}', value = f'✅ __Буду точно__ `({event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["lenmemberaccept"]})`:\n{"".join([f"`{discord.utils.get(guild.members, id = i)}`, " for i in event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["accept"] if not i == 0])}', inline = False)
                embed.add_field(name="‎‎‎‎", value="‎", inline=True)
                embed.add_field(name = f'⏰ {times} МСК', value = f'❔ __Возможно буду__ `({event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["lenmembermaybe"]})`', inline = False)
                embed.add_field(name="‎‎‎‎", value="‎", inline=True)
                embed.add_field(name = f'{chan}', value = f'❌ __Без меня__ `({event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["lenmemberdecline"]})`', inline = False)
                embed.set_thumbnail(url = guild.icon_url)
                embed.set_footer(text = '❌ - Закрыть | Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                try:
                    await message.edit(embed = embed)
                except:
                    await message.delete()
                    message = await channel.send(embed = embed)
                    await message.add_reaction('✅')
                    await message.add_reaction('❔')
                    await message.add_reaction('❌')
            elif emoji == '❌':
                if memb.id in [i for i in event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["accept"]]:
                    return
                nat = event.find_one({"guild": guild.id, "messageid": message.id})
                mas = [i for i in event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["decline"]]
                if memb.id in mas:
                    return
                mas.append(memb.id)
                event.update_one({"guild_id": guild.id, "id": message.id, "proverka": 1703}, {"$set": {"decline": mas, "lenmemberdecline": event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["lenmemberdecline"] + 1}}, upsert = True)
                if memb.id in [i for i in event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["maybe"]]:
                    mas2 = [i for i in event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["maybe"]]
                    mas2.remove(memb.id)
                    event.update_one({"guild_id": guild.id, "id": message.id, "proverka": 1703}, {"$set": {"maybe": mas2, "lenmembermaybe": event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["lenmembermaybe"] - 1}}, upsert = True)
                try:
                    await memb.send(embed = setembed(title = 'Участие в мероприятии', thumb = guild.icon_url, text = f'❌ Вы отказались от участия в мероприятии "`{nat["eventname"]}`" на сервере `{self.bot.get_guild(nat["guild"]).name}`\nТеперь вы не сможете принять участия в нём, ожидайте следующих мероприятий.'))
                except:
                    pass

                await self.bot.get_channel(840934012637020190).set_permissions(memb, view_channel = False, read_messages = False, read_message_history = False)

                name, org, site, ecolor = 'Не заполнено' if nat["eventname"] == '-' else nat["eventname"], 'Не указан' if nat["organize"] == 0 else f'{discord.utils.get(guild.members, id = nat["organize"]).mention}`({discord.utils.get(guild.members, id = nat["organize"])})`', 'Не установлена' if nat["eventtext"] == '-' else nat["eventtext"], '0xFB9E14' if nat["embedcolor"] == '-' else nat["embedcolor"]
                date, times, chan, thems = 'Дата не установлена' if nat["eventdate"] == '-' else nat["eventdate"], 'Время не установлено' if nat["eventtime"] == '-' else nat["eventtime"], 'Не установлен' if nat["etext"] == 0 else f'#{self.bot.get_channel(840934012637020190).name}', 'Не установлена' if nat["theme"] == '-' else nat["theme"]
                embed = discord.Embed(title = f'Мероприятие: {name}', description = f'**Организатор:** {org}\n**Название мероприятия:** `{name}`\n\n**Тематика мероприятия:** {thems}\n**Суть мероприятия:**\n> `{site}`', color = int(ecolor, 16), timestamp = message.created_at)
                embed.add_field(name="‎‎‎‎", value="‎", inline=True)
                embed.add_field(name = f'🗓 {date}', value = f'✅ __Буду точно__ `({event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["lenmemberaccept"]})`:\n{"".join([f"`{discord.utils.get(guild.members, id = i)}`, " for i in event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["accept"] if not i == 0])}', inline = False)
                embed.add_field(name="‎‎‎‎", value="‎", inline=True)
                embed.add_field(name = f'⏰ {times} МСК', value = f'❔ __Возможно буду__ `({event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["lenmembermaybe"]})`', inline = False)
                embed.add_field(name="‎‎‎‎", value="‎", inline=True)
                embed.add_field(name = f'{chan}', value = f'❌ __Без меня__ `({event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["lenmemberdecline"]})`', inline = False)
                embed.set_thumbnail(url = guild.icon_url)
                embed.set_footer(text = '❌ - Закрыть | Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                try:
                    await message.edit(embed = embed)
                except:
                    await message.delete()
                    message = await channel.send(embed = embed)
                    await message.add_reaction('✅')
                    await message.add_reaction('❔')
                    await message.add_reaction('❌')
            elif emoji == '❔':
                nat = event.find_one({"guild": guild.id, "messageid": message.id})
                if memb.id in [i for i in event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["accept"]] or memb.id in [i for i in event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["decline"]]:
                    return
                mas = [i for i in event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["maybe"]]
                if memb.id in mas:
                    return
                mas.append(memb.id)
                event.update_one({"guild_id": guild.id, "id": message.id, "proverka": 1703}, {"$set": {"maybe": mas, "lenmembermaybe": event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["lenmembermaybe"] + 1}}, upsert = True)
                try:
                    await memb.send(embed = setembed(title = 'Участие в мероприятии', thumb = guild.icon_url, text = f'❔ У вас есть 15 минут, для того что бы подумать, участвовать в мероприятии "`{nat["eventname"]}`" на сервере `{self.bot.get_guild(nat["guild"]).name}` или нет\nЕсли вы не нажмёте на реакцию ✅, то больше не сможете принять участие в этом мероприятии.'))
                except:
                    pass
                name, org, site, ecolor = 'Не заполнено' if nat["eventname"] == '-' else nat["eventname"], 'Не указан' if nat["organize"] == 0 else f'{discord.utils.get(guild.members, id = nat["organize"]).mention}`({discord.utils.get(guild.members, id = nat["organize"])})`', 'Не установлена' if nat["eventtext"] == '-' else nat["eventtext"], '0xFB9E14' if nat["embedcolor"] == '-' else nat["embedcolor"]
                date, times, chan, thems = 'Дата не установлена' if nat["eventdate"] == '-' else nat["eventdate"], 'Время не установлено' if nat["eventtime"] == '-' else nat["eventtime"], 'Не установлен' if nat["etext"] == 0 else f'#{self.bot.get_channel(840934012637020190).name}', 'Не установлена' if nat["theme"] == '-' else nat["theme"]
                embed = discord.Embed(title = f'Мероприятие: {name}', description = f'**Организатор:** {org}\n**Название мероприятия:** `{name}`\n\n**Тематика мероприятия:** {thems}\n**Суть мероприятия:**\n> `{site}`', color = int(ecolor, 16), timestamp = message.created_at)
                embed.add_field(name="‎‎‎‎", value="‎", inline=True)
                embed.add_field(name = f'🗓 {date}', value = f'✅ __Буду точно__ `({event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["lenmemberaccept"]})`:\n{"".join([f"`{discord.utils.get(guild.members, id = i)}`,  " for i in event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["accept"] if not i == 0])}', inline = False)
                embed.add_field(name="‎‎‎‎", value="‎", inline=True)
                embed.add_field(name = f'⏰ {times} МСК', value = f'❔ __Возможно буду__ `({event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["lenmembermaybe"]})`', inline = False)
                embed.add_field(name="‎‎‎‎", value="‎", inline=True)
                embed.add_field(name = f'{chan}', value = f'❌ __Без меня__ `({event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["lenmemberdecline"]})`', inline = False)
                embed.set_thumbnail(url = guild.icon_url)
                embed.set_footer(text = '❌ - Закрыть | Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                try:
                    await message.edit(embed = embed)
                except:
                    await message.delete()
                    message = await channel.send(embed = embed)
                    await message.add_reaction('✅')
                    await message.add_reaction('❔')
                    await message.add_reaction('❌')
                await asyncio.sleep(15*60)
                if memb.id in [i for i in event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["maybe"]]:
                    mas = [i for i in event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["decline"]]
                    if memb.id in mas or memb.id in [i for i in event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["accept"]]:
                        return
                    mas.append(memb.id)
                    mas2 = [i for i in event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["maybe"]]
                    mas2.remove(memb.id)
                    event.update_one({"guild_id": guild.id, "id": message.id, "proverka": 1703}, {"$set": {"maybe": mas2, "decline": mas, "lenmembermaybe": event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["lenmembermaybe"] - 1, "lenmemberdecline": event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["lenmemberdecline"] + 1}}, upsert = True)
                    embed = discord.Embed(title = f'Мероприятие: {name}', description = f'**Организатор:** {org}\n**Название мероприятия:** `{name}`\n\n**Тематика мероприятия:** {thems}\n**Суть мероприятия:**\n> `{site}`', color = int(ecolor, 16), timestamp = message.created_at)
                    embed.add_field(name="‎‎‎‎", value="‎", inline=True)
                    embed.add_field(name = f'🗓 {date}', value = f'✅ __Буду точно__ `({event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["lenmemberaccept"]})`:\n{"".join([f"`{discord.utils.get(guild.members, id = i)}`, " for i in event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["accept"] if not i == 0])}', inline = False)
                    embed.add_field(name="‎‎‎‎", value="‎", inline=True)
                    embed.add_field(name = f'⏰ {times} МСК', value = f'❔ __Возможно буду__ `({event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["lenmembermaybe"]})`', inline = False)
                    embed.add_field(name="‎‎‎‎", value="‎", inline=True)
                    embed.add_field(name = f'{chan}', value = f'❌ __Без меня__ `({event.find_one({"guild_id": guild.id, "id": message.id, "proverka": 1703})["lenmemberdecline"]})`', inline = False)
                    embed.set_thumbnail(url = guild.icon_url)
                    embed.set_footer(text = '❌ - Закрыть | Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                    try:
                        await message.edit(embed = embed)
                    except:
                        await message.delete()
                        message = await channel.send(embed = embed)
                        await message.add_reaction('✅')
                        await message.add_reaction('❔')
                        await message.add_reaction('❌')
                    try:
                        await memb.send(embed = setembed(title = 'Участие в мероприятии', thumb = guild.icon_url, text = f'❌ Вы не успели принять решение\nТеперь вы не сможете учавствовать в мероприятии "`{nat["eventname"]}`" на сервере `{self.bot.get_guild(nat["guild"]).name}`'))
                    except:
                        pass

    @commands.command(aliases = ['cpadd', 'приз_ивент'])
    async def event_prize_add(self, ctx, member: discord.Member = None, amount = None):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
        if not discord.utils.get(ctx.guild.roles, id = 843138403298312212) in ctx.author.roles:
            return await ctx.send(embed = setembed(text = f'❌ Доступ к использованию этой команды ограничен.'), delete_after = 5)

        if event.count_documents({"guild": ctx.guild.id, "channelid": ctx.channel.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Данный канал не предназначен для настройки мероприятия!\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["moderid"] != ctx.author.id:
            return await ctx.send(embed = setembed(text = f'❌ Вы не являетесь организатором мероприятия в этом канале.\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if member == None:
            return await ctx.send(embed = setembed(text = f'❌ Вы не указали параметр `[пользователь]`\n\n『🚩』**{prefix}event_prize_add(cpadd|приз_ивент)** - `Поздравить пользователя с установленным местом`\n-- Пример использования: `{prefix}event_prize_add @Пользователь#1234 1`'), delete_after = 5)

        if amount == None:
            return await ctx.send(embed = setembed(text = f'❌ Вы не указали параметр `[место]`\n\n『🚩』**{prefix}event_prize_add(cpadd|приз_ивент)** - `Поздравить пользователя с установленным местом`\n-- Пример использования: `{prefix}event_prize_add @Пользователь#1234 1`'), delete_after = 5)

        nat = event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})

        if nat["organize"] == 0:
            return await ctx.send(embed = setembed(text = f'❌ Вам необходимо установить `огранизатора` мероприятия командой `{prefix}set_organizer(setorg|организатор_назначить)`'), delete_after = 5)
        
        organiz = discord.utils.get(ctx.guild.members, id = nat["organize"])

        try:
            await member.send(embed = setembed(title = 'Поздравление', thumb = ctx.guild.icon_url, text = f'『💸』 **Организатор {organiz.display_name}`({organiz})` поздравляет вас с `{amount}` местом** 『💸』\nВ качестве приза, один из руководящих модераторов выдаст Вам установленный приз\nЖелаем удачи!'))
            await ctx.send(embed = setembed(title = 'Успешно', thumb = ctx.guild.icon_url, text = f'✅ Пользователю успешно отправлено поздравление!\n\n`Текст сообщение:`\n> 『💸』 **Организатор {organiz.display_name}`({organiz})` поздравляет вас с `{amount}` местом** 『💸』\nВ качестве приза, один из руководящих модераторов выдаст Вам установленный приз\nЖелаем удачи!'))
        except:
            return await ctx.send(embed = setembed(text = f'❌ Пользователь закрыл личные сообщения.'), delete_after = 5)

    @commands.command(aliases = ['eve', 'ивент_цвет'])
    async def set_embed(self, ctx, amount = None):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
        if not discord.utils.get(ctx.guild.roles, id = 843138403298312212) in ctx.author.roles:
            return await ctx.send(embed = setembed(text = f'❌ Доступ к использованию этой команды ограничен.'), delete_after = 5)

        if event.count_documents({"guild": ctx.guild.id, "channelid": ctx.channel.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Данный канал не предназначен для настройки мероприятия!\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["moderid"] != ctx.author.id:
            return await ctx.send(embed = setembed(text = f'❌ Вы не являетесь организатором мероприятия в этом канале.\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if amount == None:
            return await ctx.send(embed = setembed(text = f'❌ Вы не указали параметр `[значение]`\n\n『 🌹 』**{prefix}set_embed(eve|ивент_цвет)** - `Установить цвет embed-сообщения`\nПример использования: `{prefix}set_embed 0xFB9E14`'), delete_after = 5)

        event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"embedcolor": amount}})
        return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили `[{amount}]`, как цвет сообщения о мероприятии'), delete_after = 15) 

    @commands.command(aliases = ['evds', 'ивент_тематика'])
    async def eventdesc(self, ctx, *, amount = None):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
        if not discord.utils.get(ctx.guild.roles, id = 843138403298312212) in ctx.author.roles:
            return await ctx.send(embed = setembed(text = f'❌ Доступ к использованию этой команды ограничен.'), delete_after = 5)

        if event.count_documents({"guild": ctx.guild.id, "channelid": ctx.channel.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Данный канал не предназначен для настройки мероприятия!\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["moderid"] != ctx.author.id:
            return await ctx.send(embed = setembed(text = f'❌ Вы не являетесь организатором мероприятия в этом канале.\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if amount == None:
            return await ctx.send(embed = setembed(text = f'❌ Вы не указали параметр `[значение]`\n\n『🚩』**{prefix}eventdesc(evds|ивент_тематика)** - `Установить тематику мероприяти`\n-- Пример использования: `{prefix}eventdesc Эрудиция`'), delete_after = 5)

        if not event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["theme"] == '-':
            message = await ctx.send(embed = setembed(text = f'❔ Тематика мероприятия уже установлена: `[{event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["theme"]}]`\n\n**Если вы хотите изменить это значение - нажмите** ✅\n**Для того что бы оставить старое значение -** ❌'))
            await message.add_reaction('✅')
            await message.add_reaction('❌')
            try:
                react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
            except Exception:
                await ctx.send(embed = setembed(text = f'❌ Вы не успели принять решение, измения не были сохранены.'), delete_after = 5) 
                return await message.delete()
            else:
                await message.delete()
                if str(react.emoji) == '❌':
                    return await ctx.send(embed = setembed(title = 'Отмена', text = f'❌ Старая тематика успешно сохранена.'), delete_after = 5) 
                elif str(react.emoji) == '✅':
                    event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"theme": amount}})
                    return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили `[{amount}]`, как тематику мероприятия'), delete_after = 15) 
        else:
            event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"theme": amount}})
            return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили `[{amount}]`, как тематику мероприятия'), delete_after = 15)

    @commands.command(aliases = ['eoff', 'ивент_стоп'])
    async def event_off(self, ctx):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]

        if not discord.utils.get(ctx.guild.roles, id = 843138403298312212) in ctx.author.roles:
            return await ctx.send(embed = setembed(text = f'❌ Доступ к использованию этой команды ограничен.'), delete_after = 5)
        
        if event.count_documents({"guild": ctx.guild.id, "channelid": ctx.channel.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Данный канал не предназначен для настройки мероприятия!\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["moderid"] != ctx.author.id:
            return await ctx.send(embed = setembed(text = f'❌ Вы не являетесь организатором мероприятия в этом канале.\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        nat = event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})
        if nat["roleorg"] != 0:
            if nat["roleorg"] in [i.id for i in ctx.guild.roles]:
                role = discord.utils.get(ctx.guild.roles, id = nat["roleorg"])
                message = await ctx.send(embed = setembed(text = f'❔ Была найдена роль огранизатора {role.mention}\n\n`Если хотите её удалить нажмите` ✅\n`Если же Вы хотите оставить её нажмите` ❌'))
                await message.add_reaction('❌')
                await message.add_reaction('✅')
                try:
                    react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in ['❌', '✅'])
                except Exception:
                    await message.delete()
                else:
                    if str(react.emoji) == '❌':
                        await message.delete()
                    elif str(react.emoji) == '✅':
                        await message.delete()
                        await role.delete()

        if nat["evoice"] != 0:
            if nat["evoice"] in [i.id for i in ctx.guild.voice_channels]:
                await self.bot.get_channel(nat["evoice"]).delete()

        if nat["etext"] != 0:
            if nat["etext"] in [i.id for i in ctx.guild.text_channels]:
                await self.bot.get_channel(nat["etext"]).delete()

        if nat["rolemember"] != 0:
            if nat["rolemember"] in [i.id for i in ctx.guild.roles]:
                await discord.utils.get(ctx.guild.roles, id = nat["rolemember"]).delete()

        if event.count_documents({"guild_id": ctx.guild.id, "proverka": 1703, "id": nat["messageid"]}) != 0:
            event.delete_one({"guild_id": ctx.guild.id, "proverka": 1703, "id": nat["messageid"]})

        message = await self.bot.get_channel(840934012637020190).fetch_message(nat["messageid"])
        await message.delete()

        event.delete_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})
        await ctx.channel.delete()
        overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(view_channel = True, read_messages=True, read_message_history = True, send_messages = False), discord.utils.get(ctx.guild.roles, id = 843138403298312212): discord.PermissionOverwrite(view_channel = True, read_messages=True, read_message_history = True, send_messages = True, attach_files = True, mention_everyone = True, embed_links = True, external_emojis = True, use_external_emojis = True)}

        await self.bot.get_channel(840934012637020190).edit(overwrites = overwrites)

    @commands.command(aliases = ['setorg', 'организатор_назначить'])
    async def set_organizer(self, ctx, member: discord.Member = None):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
        if not discord.utils.get(ctx.guild.roles, id = 843138403298312212) in ctx.author.roles:
            return await ctx.send(embed = setembed(text = f'❌ Доступ к использованию этой команды ограничен.'), delete_after = 5)

        if event.count_documents({"guild": ctx.guild.id, "channelid": ctx.channel.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Данный канал не предназначен для настройки мероприятия!\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["moderid"] != ctx.author.id:
            return await ctx.send(embed = setembed(text = f'❌ Вы не являетесь организатором мероприятия в этом канале.\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if member == None:
            return await ctx.send(embed = setembed(text = f'❌ Вы не указали параметр `[пользователь]`\n\n『🕵』**{prefix}set_organizer(setorg|организатор_назначить)** - `Назначить организатора мероприятия`\nПример использования: `{prefix}set_organizer` <@!646573856785694721>'), delete_after = 5)

        if not event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["organize"] == 0:
            if discord.utils.get(ctx.guild.members, id = event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["organize"]) in [i.id for i in ctx.guild.members]:
                member2 = discord.utils.get(ctx.guild.members, id = event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["organize"])
                message = await ctx.send(embed = setembed(text = f'❔ Организатором этого мероприятия уже назначен {member2.mention}`({member2})`\n\n**Если вы хотите изменить это значение - нажмите** ✅\n**Для того что бы оставить старое значение -** ❌'))
                await message.add_reaction('✅')
                await message.add_reaction('❌')
                try:
                    react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
                except Exception:
                    await ctx.send(embed = setembed(text = f'❌ Вы не успели принять решение, измения не были сохранены.'), delete_after = 5) 
                    return await message.delete()
                else:
                    await message.delete()
                    if str(react.emoji) == '❌':
                        return await ctx.send(embed = setembed(title = 'Отмена', text = f'❌ Позиция организатора была сохранена.'), delete_after = 5) 
                    elif str(react.emoji) == '✅':
                        event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"organize": member.id}})
                        return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы назначили {member.mention}`({member})` организатором данного мероприятия'), delete_after = 15) 

        event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"organize": member.id}})
        return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы назначили {member.mention}`({member})` организатором данного мероприятия'), delete_after = 15) 

    @commands.command(aliases = ['evt', 'инвент_время'])
    async def eventtime(self, ctx, *, amount = None):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
        if not discord.utils.get(ctx.guild.roles, id = 843138403298312212) in ctx.author.roles:
            return await ctx.send(embed = setembed(text = f'❌ Доступ к использованию этой команды ограничен.'), delete_after = 5)

        if event.count_documents({"guild": ctx.guild.id, "channelid": ctx.channel.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Данный канал не предназначен для настройки мероприятия!\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["moderid"] != ctx.author.id:
            return await ctx.send(embed = setembed(text = f'❌ Вы не являетесь организатором мероприятия в этом канале.\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if amount == None:
            return await ctx.send(embed = setembed(text = f'❌ Вы не указали параметр `[значение]`\n\n『⏳』**{prefix}eventtime`(evt|инвент_время)`** - `Установливает время проведения мероприятия`\n-- Пример использования: `{prefix}eventtime 15:30`'), delete_after = 5)

        if not event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventtime"] == '-':
            message = await ctx.send(embed = setembed(text = f'❔ Время на это мероприятие уже установлено: `[{event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventtime"]}]`\n\n**Если вы хотите изменить это значение - нажмите** ✅\n**Для того что бы оставить старое значение -** ❌'))
            await message.add_reaction('✅')
            await message.add_reaction('❌')
            try:
                react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
            except Exception:
                await ctx.send(embed = setembed(text = f'❌ Вы не успели принять решение, измения не были сохранены.'), delete_after = 5) 
                return await message.delete()
            else:
                await message.delete()
                if str(react.emoji) == '❌':
                    return await ctx.send(embed = setembed(title = 'Отмена', text = f'❌ Старое время успешно сохранено.'), delete_after = 5) 
                elif str(react.emoji) == '✅':
                    event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"eventtime": amount}})
                    return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили `[{amount}]`, как время проведения мероприятия'), delete_after = 15) 
        else:
            event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"eventtime": amount}})
            return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили `[{amount}]`, как время проведения мероприятия'), delete_after = 15)

    @commands.command(aliases = ['evd', 'ивент_дата'])
    async def eventdate(self, ctx, *, amount = None):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
        if not discord.utils.get(ctx.guild.roles, id = 843138403298312212) in ctx.author.roles:
            return await ctx.send(embed = setembed(text = f'❌ Доступ к использованию этой команды ограничен.'), delete_after = 5)

        if event.count_documents({"guild": ctx.guild.id, "channelid": ctx.channel.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Данный канал не предназначен для настройки мероприятия!\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["moderid"] != ctx.author.id:
            return await ctx.send(embed = setembed(text = f'❌ Вы не являетесь организатором мероприятия в этом канале.\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if amount == None:
            return await ctx.send(embed = setembed(text = f'❌ Вы не указали параметр `[значение]`\n\n『🗓』**{prefix}eventdate`(evd|ивент_дата)`** - `Установить дату проведения мероприятия`\n-- Пример использования: `{prefix}eventdate 3 мая 2021 года`'), delete_after = 5)

        if not event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventdate"] == '-':
            message = await ctx.send(embed = setembed(text = f'❔ Дата на это мероприятие уже запланирована: `[{event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventdate"]}]`\n\n**Если вы хотите изменить это значение - нажмите** ✅\n**Для того что бы оставить старое значение -** ❌'))
            await message.add_reaction('✅')
            await message.add_reaction('❌')
            try:
                react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
            except Exception:
                await ctx.send(embed = setembed(text = f'❌ Вы не успели принять решение, измения не были сохранены.'), delete_after = 5) 
                return await message.delete()
            else:
                await message.delete()
                if str(react.emoji) == '❌':
                    return await ctx.send(embed = setembed(title = 'Отмена', text = f'❌ Старая дата успешно сохранена.'), delete_after = 5) 
                elif str(react.emoji) == '✅':
                    event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"eventdate": amount}})
                    return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили `[{amount}]`, как дату проведения мероприятия'), delete_after = 15) 
        else:
            event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"eventdate": amount}})
            return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили `[{amount}]`, как дату проведения мероприятия'), delete_after = 15) 

    @commands.command(aliases = ['enm', 'инвент_название'])
    async def eventname(self, ctx, *, amount = None):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
        if not discord.utils.get(ctx.guild.roles, id = 843138403298312212) in ctx.author.roles:
            return await ctx.send(embed = setembed(text = f'❌ Доступ к использованию этой команды ограничен.'), delete_after = 5)

        if event.count_documents({"guild": ctx.guild.id, "channelid": ctx.channel.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Данный канал не предназначен для настройки мероприятия!\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["moderid"] != ctx.author.id:
            return await ctx.send(embed = setembed(text = f'❌ Вы не являетесь организатором мероприятия в этом канале.\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if amount == None:
            return await ctx.send(embed = setembed(text = f'❌ Вы не указали параметр `[название]`\n\n『📋』**{prefix}eventname`(enm|инвент_название)`** - `Установить название ивента`\n-- Пример использования: `{prefix}eventname Улётная Викторина`'), delete_after = 5)

        if not event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventname"] == '-':
            message = await ctx.send(embed = setembed(text = f'❔ Название на это мероприятие уже установлено: `[{event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventname"]}]`\n\n**Если вы хотите изменить это значение - нажмите** ✅\n**Для того что бы оставить старое значение -** ❌'))
            await message.add_reaction('✅')
            await message.add_reaction('❌')
            try:
                react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
            except Exception:
                await ctx.send(embed = setembed(text = f'❌ Вы не успели принять решение, измения не были сохранены.'), delete_after = 5) 
                return await message.delete()
            else:
                await message.delete()
                if str(react.emoji) == '❌':
                    return await ctx.send(embed = setembed(title = 'Отмена', text = f'❌ Старое название успешно сохранено.'), delete_after = 5) 
                elif str(react.emoji) == '✅':
                    event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"eventname": amount}})
                    return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили `[{amount}]`, как название мероприятия'), delete_after = 15) 
        else:
            event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"eventname": amount}})
            return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили `[{amount}]`, как название мероприятия'), delete_after = 15) 

    @commands.command(aliases = ['cht', 'ивент_канал_т'])
    async def event_create_text(self, ctx):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
        if not discord.utils.get(ctx.guild.roles, id = 843138403298312212) in ctx.author.roles:
            return await ctx.send(embed = setembed(text = f'❌ Доступ к использованию этой команды ограничен.'), delete_after = 5)

        if event.count_documents({"guild": ctx.guild.id, "channelid": ctx.channel.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Данный канал не предназначен для настройки мероприятия!\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["moderid"] != ctx.author.id:
            return await ctx.send(embed = setembed(text = f'❌ Вы не являетесь организатором мероприятия в этом канале.\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventname"] == '-':
            return await ctx.send(embed = setembed(text = f'❌ Для начала установите название мероприятия командой `{prefix}eventname`'), delete_after = 5)

        if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["etext"] != 0:
            if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["etext"] in [i.id for i in ctx.guild.text_channels]:
                channel = self.bot.get_channel(event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["etext"])
                return await ctx.send(embed = setembed(text = f'❌ Текстовый канал для Вашего мероприятия уже создан: `[`{channel.mention}`({channel.name})]`'), delete_after = 5)

        mainCategory = discord.utils.get(ctx.guild.categories, id=840816866666348554)
        channel = await ctx.guild.create_text_channel(name=f'{event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventname"]}', category = mainCategory)
        event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"etext": channel.id}})
        return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Для Вашего мероприятия создан текстовый канал: {channel.mention}`({channel.name})`'), delete_after = 15) 

    @commands.command(aliases = ['chv', 'ивент_канал_г'])
    async def event_create_voice(self, ctx):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
        if not discord.utils.get(ctx.guild.roles, id = 843138403298312212) in ctx.author.roles:
            return await ctx.send(embed = setembed(text = f'❌ Доступ к использованию этой команды ограничен.'), delete_after = 5)

        if event.count_documents({"guild": ctx.guild.id, "channelid": ctx.channel.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Данный канал не предназначен для настройки мероприятия!\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["moderid"] != ctx.author.id:
            return await ctx.send(embed = setembed(text = f'❌ Вы не являетесь организатором мероприятия в этом канале.\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventname"] == '-':
            return await ctx.send(embed = setembed(text = f'❌ Для начала установите название мероприятия командой `{prefix}eventname`'), delete_after = 5)

        if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["evoice"] != 0:
            if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["evoice"] in [i.id for i in ctx.guild.voice_channels]:
                channel = self.bot.get_channel(event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["evoice"])
                return await ctx.send(embed = setembed(text = f'❌ Голосовой канал для Вашего мероприятия уже создан: `[`{channel.mention}`({channel.name})]`'), delete_after = 5)

        mainCategory = discord.utils.get(ctx.guild.categories, id=840816866666348554)
        channel = await ctx.guild.create_voice_channel(name=f'{event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventname"]}', category = mainCategory)
        event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"evoice": channel.id}})
        return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Для Вашего мероприятия создан голосовой канал: {channel.mention}`({channel.name})`'), delete_after = 15) 

    @commands.command(aliases = ['evtx', 'ивент_текст'])
    async def eventtext(self, ctx, *, amount = None):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
        if not discord.utils.get(ctx.guild.roles, id = 843138403298312212) in ctx.author.roles:
            return await ctx.send(embed = setembed(text = f'❌ Доступ к использованию этой команды ограничен.'), delete_after = 5)

        if event.count_documents({"guild": ctx.guild.id, "channelid": ctx.channel.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Данный канал не предназначен для настройки мероприятия!\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["moderid"] != ctx.author.id:
            return await ctx.send(embed = setembed(text = f'❌ Вы не являетесь организатором мероприятия в этом канале.\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if amount == None:
            return await ctx.send(embed = setembed(text = f'❌ Вы не указали параметр `[текст]`\n\n『🔳』**{prefix}eventtext`(evtx|ивент_текст)`** - `Установить текст эвента (описание, ссылки, подробности и т.д)`\n-- Пример использования: `{prefix}eventtext Новогдняя викторина, на которой вы сможете получить ценные призы и провести время в компании умных и эрудированных людей...`'), delete_after = 5)

        if not event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventtext"] == '-':
            message = await ctx.send(embed = setembed(text = f'❔ Информация о мероприятии уже установлена:\n> `{event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventtext"]}`\n\n**Если вы хотите изменить это значение - нажмите** ✅\n**Для того что бы оставить старое значение -** ❌'))
            await message.add_reaction('✅')
            await message.add_reaction('❌')
            try:
                react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
            except Exception:
                await ctx.send(embed = setembed(text = f'❌ Вы не успели принять решение, измения не были сохранены.'), delete_after = 5) 
                return await message.delete()
            else:
                await message.delete()
                if str(react.emoji) == '❌':
                    return await ctx.send(embed = setembed(title = 'Отмена', text = f'❌ Старая информация успешно сохранена.'), delete_after = 5) 
                elif str(react.emoji) == '✅':
                    event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"eventtext": amount}})
                    return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили новый информационный текст:\n> `{amount}`'), delete_after = 15) 
        else:
            event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"eventtext": amount}})
            return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили новый информационный текст:\n> `{amount}`'), delete_after = 15) 

    @commands.command(aliases = ['sgv', 'ивент_призы'])
    async def setgive(self, ctx, *, amount = None):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
        if not discord.utils.get(ctx.guild.roles, id = 843138403298312212) in ctx.author.roles:
            return await ctx.send(embed = setembed(text = f'❌ Доступ к использованию этой команды ограничен.'), delete_after = 5)

        if event.count_documents({"guild": ctx.guild.id, "channelid": ctx.channel.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Данный канал не предназначен для настройки мероприятия!\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["moderid"] != ctx.author.id:
            return await ctx.send(embed = setembed(text = f'❌ Вы не являетесь организатором мероприятия в этом канале.\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if amount == None:
            return await ctx.send(embed = setembed(text = f'❌ Вы не указали параметр `[призы]`\n\n『🪁』**{prefix}setgive`(sgv|ивент_призы)`** - `Установить награду за победу в мероприятии`\n-- Пример использования: `{prefix}setgive 1 место - 5 долларов, 2 место - 3 доллара, 3 место - 1 доллар`'), delete_after = 5)

        if not event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventpriz"] == '-':
            message = await ctx.send(embed = setembed(text = f'❔ Призы на это мероприятие уже установлены:\n> `{event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventpriz"]}`\n\n**Если вы хотите изменить это значение - нажмите** ✅\n**Для того что бы оставить старое значение -** ❌'))
            await message.add_reaction('✅')
            await message.add_reaction('❌')
            try:
                react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
            except Exception:
                await ctx.send(embed = setembed(text = f'❌ Вы не успели принять решение, измения не были сохранены.'), delete_after = 5) 
                return await message.delete()
            else:
                await message.delete()
                if str(react.emoji) == '❌':
                    return await ctx.send(embed = setembed(title = 'Отмена', text = f'❌ Старые призы успешно сохранены.'), delete_after = 5) 
                elif str(react.emoji) == '✅':
                    event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"eventpriz": amount}})
                    return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили новые призы на мероприятие:\n> `{amount}`'), delete_after = 15) 
        else:
            event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"eventpriz": amount}})
            return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы установили новые призы на мероприятие:\n> `{amount}`'), delete_after = 15)

    @commands.command(aliases = ['evr', 'ивент_роль'])
    async def event_role(self, ctx, *, amount = None):
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
        if not discord.utils.get(ctx.guild.roles, id = 843138403298312212) in ctx.author.roles:
            return await ctx.send(embed = setembed(text = f'❌ Доступ к использованию этой команды ограничен.'), delete_after = 5)

        if event.count_documents({"guild": ctx.guild.id, "channelid": ctx.channel.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Данный канал не предназначен для настройки мероприятия!\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["moderid"] != ctx.author.id:
            return await ctx.send(embed = setembed(text = f'❌ Вы не являетесь организатором мероприятия в этом канале.\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        if amount == None:
            return await ctx.send(embed = setembed(text = f'❌ Вы не указали параметр `[роль]`\n\n『🌟』**{prefix}event_role`(evr|ивент_роль)`** - `Установить роль огранизатора мероприятия`\n-- Пример использования: `{prefix}eventrole` <@&843138403298312212>\n-- Для создания новой роли мероприятия: `{prefix}eventrole 0`'), delete_after = 5)

        if not amount == '0':
            role = discord.utils.get(ctx.guild.roles, id = int(amount.split(' ')[0].replace('<@&', '').replace('>', '').replace('.', '')))

        if not event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["roleorg"] == 0:
            if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["roleorg"] in [i.id for i in ctx.guild.roles]:
                message = await ctx.send(embed = setembed(text = f'❔ Роль организатора этого мероприятия уже установлена: `[{discord.utils.get(ctx.guild.roles, id = event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["roleorg"]).name}]`\n\n**Если вы хотите изменить это значение - нажмите** ✅\n**Для того что бы оставить старое значение -** ❌'))
                await message.add_reaction('✅')
                await message.add_reaction('❌')
                try:
                    react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
                except Exception:
                    await ctx.send(embed = setembed(text = f'❌ Вы не успели принять решение, измения не были сохранены.'), delete_after = 5) 
                    return await message.delete()
                else:
                    await message.delete()
                    if str(react.emoji) == '❌':
                        return await ctx.send(embed = setembed(title = 'Отмена', text = f'❌ Старая роль успешно сохранена.'), delete_after = 5) 
                    elif str(react.emoji) == '✅':
                        if amount == '0':
                            if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventname"] == '-':
                                return await ctx.send(embed = setembed(text = f'❌ Для начала установите название мероприятия командой `{prefix}eventname`'), delete_after = 5)
                            try:
                                role = await ctx.guild.create_role(name = f'Организатор мероприятия "{event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventname"]}"')
                                await role.edit(colour = 0x08ff20)
                                await ctx.guild.edit_role_positions(positions = {role: 13})
                            except:
                                role = await ctx.guild.create_role(name = f'Организатор мероприятия')
                                await role.edit(colour = 0x08ff20)
                                await ctx.guild.edit_role_positions(positions = {role: 13})
                        event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"roleorg": role.id}})
                        return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы назначили новой ролью организацитора мероприятия роль `[{role.name}]`'), delete_after = 15)

        if amount == '0':
            if event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventname"] == '-':
                return await ctx.send(embed = setembed(text = f'❌ Для начала установите название мероприятия командой `{prefix}eventname`'), delete_after = 5)
            try:
                role = await ctx.guild.create_role(name = f'Организатор мероприятия {event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})["eventname"]}')
            except:
                return await ctx.send(embed = setembed(text = f'❌ Не удалось создать роль, возможно название мероприятия слишком велико'), delete_after = 5) 
        event.update_one({"guild": ctx.guild.id, "channelid": ctx.channel.id}, {"$set": {"roleorg": role.id}})
        return await ctx.send(embed = setembed(title = 'Успешно!', text = f'✅ Вы назначили новой ролью организацитора мероприятия роль `[{role.name}]`'), delete_after = 15) 

    @commands.command(aliases = ['evis', 'предпросмотр'])
    async def event_visual(self, ctx):
        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
        if not discord.utils.get(ctx.guild.roles, id = 843138403298312212) in ctx.author.roles:
            return await ctx.send(embed = setembed(text = f'❌ Доступ к использованию этой команды ограничен.'), delete_after = 5)

        if event.count_documents({"guild": ctx.guild.id, "channelid": ctx.channel.id}) == 0:
            return await ctx.send(embed = setembed(text = f'❌ Данный канал не предназначен для настройки мероприятия!\nДля того что бы создать своё мероприятие используйте `{prefix}event_on(eon|ивент_старт)`'), delete_after = 5)

        ent = event.find_one({"guild": ctx.guild.id, "channelid": ctx.channel.id})
        name, org, site, ecolor = 'Не заполнено' if ent["eventname"] == '-' else ent["eventname"], 'Не указан' if ent["organize"] == 0 else f'{discord.utils.get(ctx.guild.members, id = ent["organize"]).mention}`({discord.utils.get(ctx.guild.members, id = ent["organize"])})`', 'Не установлена' if ent["eventtext"] == '-' else ent["eventtext"], '0xFB9E14' if ent["embedcolor"] == '-' else ent["embedcolor"]
        date, times, chan, thems = 'Дата не установлена' if ent["eventdate"] == '-' else ent["eventdate"], 'Время не установлено' if ent["eventtime"] == '-' else ent["eventtime"], 'Не установлен' if ent["etext"] == 0 else f'#{self.bot.get_channel(ent["etext"]).name}', 'Не установлена' if ent["theme"] == '-' else ent["theme"]
        embed = discord.Embed(title = f'Мероприятие: {name}', description = f'**Организатор:** {org}\n**Название мероприятия:** `{name}`\n\n**Тематика мероприятия:** {thems}\n**Суть мероприятия:**\n> `{site}`', color = int(ecolor, 16), timestamp = ctx.message.created_at)
        embed.add_field(name="‎‎‎‎", value="‎", inline=True)
        embed.add_field(name = f'🗓 {date}', value = '✅ __Буду точно__ `(0)`', inline = False)
        embed.add_field(name="‎‎‎‎", value="‎", inline=True)
        embed.add_field(name = f'⏰ {times} МСК', value = '❔ __Возможно буду__ `(0)`', inline = False)
        embed.add_field(name="‎‎‎‎", value="‎", inline=True)
        embed.add_field(name = f'{chan}', value = '❌ __Без меня__ `(0)`', inline = False)
        embed.set_thumbnail(url = ctx.guild.icon_url)
        embed.set_footer(text = '❌ - Закрыть | Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        message = await ctx.send(embed = embed, delete_after = 120)
        await message.add_reaction('❌')
        try:
            react, user = await self.bot.wait_for('reaction_add', timeout= 120.0, check= lambda react, user: user == ctx.author and react.emoji in ['❌'])
        except Exception:
            return await message.delete()
        else:
            if str(react.emoji) == '❌':
                return await message.delete()



    '''
    @commands.command()
    async def pkz(self, ctx):
        
        embed = discord.Embed(title = 'Мероприятие: Новогоднаяя Викторина', description = f'**Организатор:** {ctx.author.mention}`({ctx.author})` - `ID: {ctx.author.id}`\n**Название мероприятия:** `Новогоднаяя Викторина`\n\n**Суть мероприятия:**\n> `Новогдняя викторина, на которой вы сможете получить ценные призы и провести время в компании умных и эрудированных людей...`', color = 0xFB9E14, timestamp = ctx.message.created_at)
        embed.add_field(name="‎‎‎‎", value="‎", inline=True)
        embed.add_field(name = '🗓 09 Апрель 2021', value = '✅ __Буду точно__ `(0)`', inline = False)
        embed.add_field(name="‎‎‎‎", value="‎", inline=True)
        embed.add_field(name = '⏰ 16:00 МСК', value = '❔ __Возможно буду__ `(0)`', inline = False)
        embed.add_field(name="‎‎‎‎", value="‎", inline=True)
        embed.add_field(name = '『 🔈』Викторина', value = '❌ __Без меня__ `(0)`', inline = False)
        embed.set_thumbnail(url = ctx.guild.icon_url)
        embed.set_footer(text = 'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        message = await ctx.send(embed = embed)
        await message.add_reaction('✅')
        await message.add_reaction('❔')
        await message.add_reaction('❌')
    '''



def setup(bot):
    bot.add_cog(events(bot))