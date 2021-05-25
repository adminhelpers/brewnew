import discord
from discord.ext import commands
from discord.utils import get
import datetime
import random
import re
import os
import time
import os.path
import asyncio
import json
import requests
from pymongo import MongoClient
import ffmpeg

cluster = MongoClient("mongodb+srv://dbrbase:oT4y7678BFK00Bsp@rodinadb.rhew3.mongodb.net/rodinaname?retryWrites=true&w=majority")
db = cluster["rodina"]
govs = db["gov"]
org = db["org"]

# family.insert_one({"_id": ctx.author.id, "name": "привет"}) -> Запись в базу данных(Коллекция: Family) 
# if family.count_documents({"_id": ctx.author.id}) -> Проверка, есть значение или нет в базе данных(Коллекция: Family | Поиск по графе: _id) 
# family.find_one({"_id": ctx.author.id}) -> Получение значения из базы(Коллекция: Family | Поиск по графе: _id) 
# print(family.find_one({"_id": ctx.author.id})["name"]) -> Получение отдельного значения(Коллекция: Family | Поиск по графе: _id | Значение графы: name) 
# family.update_one({"_id": ctx.author.id}, {"$set": {"name": settle}}) -> Обновление значения в базе(Коллекция: Family | По графе: _id | Аргумент: $set - Замена | Значение графы: name | Устанавливаемое значение: settle)

global otd
otd = {
    577531432461664266: 760874267407024180,
    577541219635429401: 760874121604104202,
    577532998908641280: 760874578879840306,
    748492230846578768: 760874805226111046,
    577532535819468811: 760875032313462804,
    577533519920889866: 760875237071126541,
    577533469429727232: 760875428008689666,
    577532332731269120: 760875654328745984,
    577533311556255744: 760875843249111066,
    577533194048634880: 760876076976570469,
    749218773084405840: 760876285605707797,
    752192117891268618: 760876526643314771,
    577532176115957760: 760876732382969879
}

global frac
frac = {
    577531432461664266: 'Правительство',
    577541219635429401: 'Центральный Банк',
    577532998908641280: 'Главное управление Министерства внутренних дел г.Арзамаса',
    748492230846578768: 'Школа Полиции г.Эдово',
    577532535819468811: 'Главное управление уголовного розыска г.Лыткарино',
    577533519920889866: 'Федеральная Служба Безопасности',
    577533469429727232: 'Федеральная Служба Исполнения Наказаний',
    577532332731269120: 'Армия',
    577533311556255744: 'Городская клиническая больница г.Арзамас',
    577533194048634880: 'Скорая медицинская помощь г.Эдово',
    749218773084405840: 'Государственный медицинский университет г.Лыткарино',
    752192117891268618: 'Новостное Агенство "Дождь"',
    577532176115957760: 'Радиостанция "Рокс"'
}

global frac1
frac1 = {
    577531432461664266: 'Хол правительства',
    577541219635429401: 'Здание центрального банка',
    577532998908641280: 'Здание главного управления Министерства внутренних дел г.Арзамаса',
    748492230846578768: 'Отделение школы полиции г.Эдово',
    577532535819468811: 'Отделение главного управления уголовного розыска г.Лыткарино',
    577533519920889866: 'Здание федеральной службы безопасности',
    577533469429727232: 'Хол федеральной службы исполнения наказаний',
    577532332731269120: 'Военкомат г. Батырево',
    577533311556255744: 'Здание городской клинической больницы г.Арзамас',
    577533194048634880: 'Здание скорой медицинская помощь г.Эдово',
    749218773084405840: 'Здание государственного медицинского университета г.Лыткарино',
    752192117891268618: 'Хол новостного агенства "Дождь"',
    577532176115957760: 'Хол радиостанции "Рокс"'
}

global rolek
rolek = {
    577541219635429401: 757589893131010049,
    577531432461664266: 757589904887906424,
    577532998908641280: 757589846704259114,
    748492230846578768: 757589892103536652,
    577532535819468811: 757589890153316434,
    577533519920889866: 757589821320593521,
    577533469429727232: 757589861388648448,
    577532332731269120: 757589801812754462,
    577533311556255744: 757589897858121829,
    577533194048634880: 757589870620442764,
    749218773084405840: 757589815582523443,
    752192117891268618: 757589806573158460,
    577532176115957760: 757589884851585150
}

global mp3
mp3 = {
    577541219635429401: 'C:/Users/adminhelper/Desktop/botrrp/pravvo.mp3',
    577531432461664266: 'C:/Users/adminhelper/Desktop/botrrp/bank.mp3',
    577532998908641280: 'C:/Users/adminhelper/Desktop/botrrp/mvd.mp3',
    748492230846578768: 'C:/Users/adminhelper/Desktop/botrrp/mvd.mp3',
    577532535819468811: 'C:/Users/adminhelper/Desktop/botrrp/mvd.mp3',
    577533519920889866: 'C:/Users/adminhelper/Desktop/botrrp/mvd.mp3',
    577533469429727232: 'C:/Users/adminhelper/Desktop/botrrp/mvd.mp3',
    577532332731269120: 'C:/Users/adminhelper/Desktop/botrrp/army.mp3',
    577533311556255744: 'C:/Users/adminhelper/Desktop/botrrp/minzdrav.mp3',
    577533194048634880: 'C:/Users/adminhelper/Desktop/botrrp/minzdrav.mp3',
    749218773084405840: 'C:/Users/adminhelper/Desktop/botrrp/minzdrav.mp3',
    752192117891268618: 'C:/Users/adminhelper/Desktop/botrrp/radio.mp3',
    577532176115957760: 'C:/Users/adminhelper/Desktop/botrrp/radio.mp3',
}

def lrole(member: discord.Member, arg):
    global frac
    masr = [577531432461664266, 577541219635429401, 577532998908641280, 748492230846578768, 577532535819468811, 577533519920889866, 577533469429727232, 577532332731269120, 577533311556255744, 577533194048634880, 749218773084405840, 752192117891268618, 577532176115957760]
    for i in member.roles:
        if i.id in masr:
            if arg == 1:
                return frac[i.id]
            elif arg == 2:
                return i.id
    else:
        return 0

class gov(commands.Cog):
    """MODERATION Cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        print('Rodina 04 | GOV by dollar ム baby#3603 - Запущен')

    

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def addgov(self, ctx, times = None):
        global frac1
        a = str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))).split()[1].split(':')
        await ctx.message.delete()
        if not discord.utils.get(ctx.guild.roles, id = 577528348146925571) in ctx.author.roles and not discord.utils.get(ctx.guild.roles, id = 577528943326920704) in ctx.author.roles:
            ctx.command.reset_cooldown(ctx)
            return await ctx.channel.send('`[ERROR]` `Ошибка!`', embed = discord.Embed(description = f'**Данная команда доступна только лидерам или заместителям государственных организаций!**', colour = 0xFB9E14), delete_after = 10)
        if times == None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.channel.send('`[ERROR]` `Введите команду правильно!`', embed = discord.Embed(description = f'**/gov** [Время]', colour = 0xFB9E14), delete_after = 10)
        if not ":" in list(times):
            ctx.command.reset_cooldown(ctx)
            return await ctx.channel.send('`[ERROR]` `Время указано не верно!`', embed = discord.Embed(description = f'**Примеры указания времени:**\n- `10:05`\n- `19:30`\n- `06:00`', colour = 0xFB9E14), delete_after = 10)
        mas = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']
        t = times.split(":")
        t2 = times.replace(":", "")
        if not t[::-1][1] in mas:
            ctx.command.reset_cooldown(ctx)
            return await ctx.channel.send('`[ERROR]` `Время указано не верно!`', embed = discord.Embed(description = f'**Примеры указания времени:**\n- `10:05`\n- `19:30`\n- `06:00`', colour = 0xFB9E14), delete_after = 10)
        if not list(t[1])[-1] == '5':
            ctx.command.reset_cooldown(ctx)
            return await ctx.channel.send('`[ERROR]` `Время указано не верно!`', embed = discord.Embed(description = f'**Занимать государственную волну необходимо на следующие минутные отрезки:**\n`05` -> `15` -> `25` -> `35` -> `45` -> `55`', colour = 0xFB9E14), delete_after = 10)

        a = str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))).split()[1].split(':')
        #if t[::-1][1] <= a[0] or t[1] <= a[0]:
            #return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, Произошла ошибка #270. Причины её возникновения:\n- `Время установленно Вами уже прошло.`\n- `Занимать государственную волну необходимо не менее чем за 1 минуту!`', colour = 0xFB9E14), delete_after = 15)
        if govs.count_documents({"time": t2}) == 1:
            ctx.command.reset_cooldown(ctx)
            return await ctx.channel.send(embed = discord.Embed(description = f'**Данное время уже занято организацией** {discord.utils.get(ctx.guild.roles, id = govs.find_one({"time": t2})["id"]).mention}', colour = 0xFB9E14), delete_after = 10)
        
        lid = lrole(ctx.author, 2)
        test = lrole(ctx.author, 1)
        if lid == 0:
            ctx.command.reset_cooldown(ctx)
            return await ctx.channel.send('`[ERROR]` `Ошибка!`', embed = discord.Embed(description = f'**Ошибка определения #271. Возможные причины появления ошибки:\n- `У вас отсутствует фракционная роль.`\n- `Вашей организации не доступно использование данной команды.`**', colour = 0xFB9E14), delete_after = 10)
        if org.count_documents({"id": lid}) == 0:
            org.insert_one({"id": lid, "mest": frac1[lid], "zapr": 0})

        message = await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, Вы действительно хотите занять государственную волну на {times}?\n**Место проведения установленое для фракции {test} по умолчанию:**\n> `{org.find_one({"id": lid})["mest"]}`\n\n> ❤ `- Да`\n> 💔 `- Нет`\n✏ - `Изменить место проведения и отправить`', colour = 0xFB9E14))
        await message.add_reaction('❤')
        await message.add_reaction('💔')
        await message.add_reaction('✏')
        try:
            react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in ['💔', '❤', '✏'])
        except Exception:
            ctx.command.reset_cooldown(ctx)
            return await message.delete()
        else:
            await message.delete()
            if str(react.emoji) == '💔':
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, Вы отменили действие.', colour = 0xFB9E14), delete_after = 5)
            elif str(react.emoji) == '❤' or str(react.emoji) == '✏':
                if str(react.emoji) == '✏':
                    mes1 = await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, укажите новое место для собеседования.', colour = 0xFB9E14))
                    def check(m):
                        return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
                    try:
                        msg = await self.bot.wait_for('message', timeout= 60.0, check = check)
                    except Exception:
                        await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, Вы слишком долго вводили необходимые данные.\nУстановка государственной волны отменена!', colour = 0xFB9E14), delete_after = 5)
                        ctx.command.reset_cooldown(ctx)
                        return await mes1.delete()
                    else:
                        await msg.delete()
                        await mes1.delete()
                        org.update_one({"id": lid}, {"$set": {"mest": msg.content}})
                        await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, Вы успешно установили новое место для проведения собеседований в организацию {test}\n- `Новое место:` {msg.content}', colour = 0xFB9E14), delete_after = 5)
                if govs.count_documents({"id": lid}) == 1 or govs.count_documents({"time": t2}) == 1:
                    ctx.command.reset_cooldown(ctx)
                    return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, Произошла ошибка #272. Причины её возникновения:\n- `Ваша организация заняла гос волну во время данной установки`\n- `Время установленное вами({times}) было установлено другой организацией во время данной установки!`', colour = 0xFB9E14), delete_after = 15)
                else:
                    govs.insert_one({"guild": ctx.guild.id, "id": lid, "time": t2, "naz": ctx.author.id, "mest": org.find_one({"id": lid})["mest"], "times": times})
                    return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, вы успешно заняли государственную волну новостей дискорда. \n\n**Информация о волне:**\n`Организация:` {test}\n`Время:` {times}\n`Время сейчас:` {a[0]}:{a[1]}\n`Место проведения:` {org.find_one({"id": lid})["mest"]}', colour = 0xFB9E14), delete_after = 35)

    @commands.command()
    async def removegov(self, ctx):
        await ctx.message.delete()
        if not discord.utils.get(ctx.guild.roles, id = 577528348146925571) in ctx.author.roles and not discord.utils.get(ctx.guild.roles, id = 577528943326920704) in ctx.author.roles:
            return await ctx.channel.send('`[ERROR]` `Ошибка!`', embed = discord.Embed(description = f'**Данная команда доступна только лидерам или заместителям государственных организаций!**', colour = 0xFB9E14), delete_after = 10)
        lid = lrole(ctx.author, 2)
        if govs.count_documents({"id": lid}) == 0:
            return await ctx.channel.send('`[ERROR]` `Ошибка!`', embed = discord.Embed(description = f'**Ваша организация({discord.utils.get(ctx.guild.roles, id = lid).mention}) не занимала государственную волну.**', colour = 0xFB9E14), delete_after = 10)
        else:
            message = await ctx.channel.send('`[ERROR]` `Поддтвердите действие!`', embed = discord.Embed(description = f'**Вы действительно хотите убрать государственную волну у организации {discord.utils.get(ctx.guild.roles, id = lid).mention}?\n\n> ❤ `- Да`\n> 💔 `- Нет`**', colour = 0xFB9E14))
            await message.add_reaction('❤')
            await message.add_reaction('💔')
            try:
                react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in ['💔', '❤'])
            except Exception:
                return await message.delete()
            else:
                await message.delete()
                if str(react.emoji) == '💔':
                    return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, Вы отменили действие!', colour = 0xFB9E14), delete_after = 5)
                elif str(react.emoji) == '❤':
                    govs.delete_one({"id": lid})
                    return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, Вы успешно сняли государственную волну от организации {discord.utils.get(ctx.guild.roles, id = lid).mention}', colour = 0xFB9E14), delete_after = 30)

    @commands.command()
    async def sobes(self, ctx):
        await ctx.message.delete()
        mas = [ ]
        index = 0
        for i in govs.find({"guild": ctx.guild.id}):
            index += 1
            mas.append(f'**`{index}.` Организация:** <@&{i["id"]}>\n> `Время проведения:` {i["times"]}\n> `Место проведения:` {i["mest"]}\n> `Назначил:` <@!{i["naz"]}>\n')
        a = ''.join(mas)
        return await ctx.channel.send(f'{ctx.author.mention}, список предстоящих собеседований:', embed = discord.Embed(description = f'{a}', colour = 0xFB9E14))
        
    @commands.Cog.listener()
    async def on_message(self, ctx):
        global mp3
        a = str(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))).split()[1].split(':')
        times = f'{a[0]}{a[1]}'
        for i in govs.find({"guild": 577511138032484360}):
            if i["time"] == times:
                id = i["id"]
                mest = i["mest"]
                govs.delete_one({"id": i["id"]})
                guild = self.bot.get_guild(577511138032484360)
                channel = self.bot.get_guild(577511138032484360).get_channel(577718720911376384)
                vhannel = guild.get_channel(782991570773213204)
                voice = await vhannel.connect()
                voice.play(discord.FFmpegPCMAudio(executable="C:/Users/adminhelper/Desktop/botrrp/ffmpeg.exe", source = mp3[id]))
                return await channel.send(f'✫ ✪ ☆ ★ @here ★ ☆ ✪ ✫', embed = discord.Embed(description = f'**                              |______Государственные Новости_______|**\nУважаемые жители округа! Минуточку внимания.\nВ данный момент проходит собеседование в организацию {discord.utils.get(guild.roles, id = id).mention}\n**Для вступления необходимо прибыть в** `{mest}`', colour = 0xFB9E14))

def setup(bot):
    bot.add_cog(gov(bot))
        