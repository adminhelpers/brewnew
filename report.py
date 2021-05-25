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

cluster = MongoClient("mongodb+srv://dbrbase:oT4y7678BFK00Bsp@rodinadb.rhew3.mongodb.net/rodinaname?retryWrites=true&w=majority")
db = cluster["rodina"]
report = db["report"]
moder = db["moder"]

# family.insert_one({"_id": ctx.author.id, "name": "привет"}) -> Запись в базу данных(Коллекция: Family) 
# if family.count_documents({"_id": ctx.author.id}) -> Проверка, есть значение или нет в базе данных(Коллекция: Family | Поиск по графе: _id) 
# family.find_one({"_id": ctx.author.id}) -> Получение значения из базы(Коллекция: Family | Поиск по графе: _id) 
# print(family.find_one({"_id": ctx.author.id})["name"]) -> Получение отдельного значения(Коллекция: Family | Поиск по графе: _id | Значение графы: name) 
# family.update_one({"_id": ctx.author.id}, {"$set": {"name": settle}}) -> Обновление значения в базе(Коллекция: Family | По графе: _id | Аргумент: $set - Замена | Значение графы: name | Устанавливаемое значение: settle)

def add(member: discord.Member, arg):
  if moder.count_documents({"id": member.id}) == 0:
    moder.insert_one({"guild": 577511138032484360, "id": member.id, "close": 0, "rasm": 0, "mute": 0, "kick": 0, "warn": 0, "ban": 0, "unwarn": 0, "unmute": 0, "vmute": 0, "vunmute": 0, "rols": 0, "repa": 0, "derols": 0, "dezaprols": 0, "vig": 0, "leader": 0, "x2": 0})
    moder.update_one({"id": member.id}, {"$set": {arg: 1}})
  else:
    if moder.find_one({"id": member.id})["x2"] == 0:
      moder.update_one({"id": member.id}, {"$set": {arg: moder.find_one({"id": member.id})[arg] + 1}})
    else:
      moder.update_one({"id": member.id}, {"$set": {arg: moder.find_one({"id": member.id})[arg] + 2}})

class reports(commands.Cog):
    """REPORT Cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Rodina 04 | Report by dollar ム baby#3603 - Запущен')
    
    @commands.command(aliases = ['привет', 'hello', 'хай', 'хеллоу', 'ку', 'qq']) 
    async def hi(self, ctx): 
        role = discord.utils.get(ctx.guild.roles, id = 703270075666268160) 
        if not role in ctx.author.roles: 
            return 

        await ctx.message.delete() 
        embed = discord.Embed(color = 0xFB9E14) 
        embed.set_footer(text = f'Ответ был дан модератором {ctx.author.display_name}', icon_url = self.bot.user.avatar_url) 
        return await ctx.send(f'`[MODERATOR] Здравствуйте, я агент технической поддержки - {ctx.author.display_name}, я постараюсь помочь Вам в решении вашей проблемы.`', embed = embed) 

    @commands.command(aliases = ['пока', 'bb', 'бб']) 
    async def by(self, ctx): 
        role = discord.utils.get(ctx.guild.roles, id = 703270075666268160) 
        if not role in ctx.author.roles: 
            return 

        await ctx.message.delete() 
        embed = discord.Embed(color = 0xFB9E14) 
        embed.set_footer(text = f'Ответ был дан модератором {ctx.author.display_name}', icon_url = self.bot.user.avatar_url) 
        return await ctx.send(f'`[UPDATE!] Ответ на Ваш вопрос был дан. Могу ли я поставить статус "Закрыт" вашему вопросу?`\n`Если у Вас по прежнему остались вопросы, задавайте их прямо здесь.`', embed = embed) 

    @commands.command(aliases = ['нарушитель']) 
    async def scam(self, ctx): 

        embed = discord.Embed(description = f'🌐 — [Раздел жалоб на игроков не состоящих в гос.оргагизациях](http://forum.rodina-rp.com/forums/184/)\n🌐 — [Раздел жалоб на игроков состоящих в гос.оргагизациях](http://forum.rodina-rp.com/forums/183/)\n🌐 — [Раздел жалоб на игроков не состоящих в ОПГ](http://forum.rodina-rp.com/forums/187/)\n🌐 — [Раздел жалоб на игроков не состоящих в мафиях](http://forum.rodina-rp.com/forums/186/)\n🌐 — [Раздел жалоб на участников битвы за корабль](http://forum.rodina-rp.com/forums/210/)', colour = 0xFB9E14) 
        await ctx.send(f'`[REFRESH] Если Вы стали жертвой обмана или нарушения от определённого игрока, за Вами остаётся право написать жалобу в одном из разделов:`', embed = embed) 

    @commands.command(aliases = ['донат']) 
    async def donate(self,  ctx): 

        embed = discord.Embed(description = f'🌐 — [Раздел с возможностью пополнения игрового счёта](https://rodina-rp.com/donate)', colour = 0xFB9E14) 
        await ctx.send(f'`[REFRESH] Пополнить счёт игрового аккаунта можно на форуме в разделе "Пополнить счёт".`\n\n**[ВАЖНО]:**\n`> Старайтесь заполнять все поля максимально внимательно, что бы Ваше пожертвование не пришло на аккаунт другому челочеку!`\n`> Возврата денежных средств проект не предусматривает!`\n`> Проект НЕ НЕСЕТ ответственности за утерянное имущество!`', embed = embed) 

    @commands.command(aliases = ['ресурсы']) 
    async def resource(self, ctx): 

        embed3 = discord.Embed(description = f'🌐 — [Официальный сайт](https://rodina-rp.com/)\n🌐 — [Официальное сообщество [В]Контакте](https://vk.com/rodinavost4)\n🌐 — [Беседа игроков](https://vk.cc/aBYkIk)\n🌐 — [Link in Discord | Rodina RP [04]](https://discord.gg/HXA7jmT)\n🌐 — [Раздел жалоб](http://forum.rodina-rp.com/forums/181/)\n🌐 — [Технический раздел](http://forum.rodina-rp.com/forums/199/)', colour = 0xFB9E14) 
        await ctx.send(f'`[REFRESH] Список официальных ресурсов Rodina RP | Восточный Округ[04]:`', embed = embed3) 

    @commands.command(aliases = ['техраздел']) 
    async def th(self, ctx): 

        embed = discord.Embed(description = f'🌐 — [Технический раздел](http://forum.rodina-rp.com/forums/199/)', colour = 0xFB9E14) 
        await ctx.send(f'`[REFRESH] Для решения вопросов технического характера, Вам стоит обратиться в:`', embed = embed) 

    @commands.command(aliases = ['ЖБ', 'жалоба']) 
    async def jb(self, ctx): 

        embed = discord.Embed(description = f'🌐 — [Раздел жалоб на администрацию сервера](http://forum.rodina-rp.com/forums/182/)', colour = 0xFB9E14) 
        await ctx.send(f'`[REFRESH] Если Вы не согласны с выданным наказанием, за Вами остаётся право написать жалобу в одном из разделов игровых серверов`\n\n`[Past Scriptum]:`\n`> На предоставление опровержения, администратору даётся 24 полных часа, не учитвая различные ситуации.`\n`> За обман администрации(Подделку скринов/видео) Вы будете занесены в чёрный список проекта!`', embed = embed) 

    @commands.command(aliases = ['информация', 'infa'])
    async def inf(self, ctx): 
        return await ctx.send(f'`[REFRESH] Канал со всей актуальной инфоомацией` <#673188188189360138>') 

    @commands.command(aliases = ['обзвоны', 'обзвон']) 
    async def obz(self, ctx): 
        return await ctx.send(f'`[REFRESH] Информация о обзвонах подробно описана в канале` <#673259318123954226>') 

    @commands.command(aliases = ['рполучить', 'получитьроль']) 
    async def adrole(self, ctx): 
        return await ctx.send(f'`[REFRESH] Информация о получении роли указана в канале` <#673205002189275136>') 

    @commands.command(aliases = ['Правила', 'правила']) 
    async def rule(self, ctx): 
        return await ctx.send(f'`[REFRESH] Полный свод правил действующих в этом Discod Сервере указана в канале` <#673194313466904607>.\n`Не знание правил не освобождает Вас от ответственности!`\n\n`[Past Scriptum]: Правила могут быть изменены или дополнены в любой момент без оповещения об этом участников.`') 

    @commands.command(aliases = ['ЖБМ', 'мжалоба']) 
    async def jbm(self, ctx): 

        embed = discord.Embed(description = '> 1. [[В]Контакте](https://vk.com/norimyxxxo1702) | `Discord:` @adminhelper#7777 | `Имя:` Павел\n> 2. [[В]Контакте](https://vk.com/kodiknarkotik) | `Discord:` @kodiknarkotik#6873 | `Имя:` Вадим', color = 0xFB9E14) 
        return await ctx.send(f'`[REFRESH] Если Вас не устраивает ответ на Ваш вопрос, задайте его заного.`\n`Если Вы желаете написать жалобу на сотрудника технической поддержки` <@&703270075666268160>, `обратитесь в личные сообщения куратору технической части:`\n', embed = embed) 

    @commands.command() 
    async def помощь(self, ctx): 

        return await ctx.send(f'`[REFRESH] Вот список команд которые могут Вам помочь:`\n> /техраздел - `Ссылка на технический раздел`\n> /нарушитель - `Что делать, если вы стали жертвой обмана или нарушения от игрока?`\n> /донат - `Информация о донате`\n> /ресурсы - `Информация о оффициальный платформах проекта`\n> /жалоба - `Куда писать жалобу?`\n> /информация - `Где можно узнать актуальную информацию?`\n> /рполучить - `Информация о фракционных ролях`\n> /дискорд - `Информация о данном Discord сервере?`\n> /правила - `Правила данного Discord Сервера`\n> /мжалоба - `Отправить жалобу на модератора.`')

    @commands.command()
    async def ставка(self, ctx, storona=None):

        with open("cogs/stavki.json", "r") as file:
            data = json.load(file)

        f = 0
        for i in data[str(ctx.guild.id)].keys():
            f += 1

        if f >= 20:
            with open("cogs/stavki.json", "w") as file:
                json.dump(data, file, indent=4)
            return await ctx.send(
                '`[ERR] Ставки не принимаются`.', delete_after=5)

        if storona == None:
            with open("cogs/stavki.json", "w") as file:
                json.dump(data, file, indent=4)
            return await ctx.send(
                '`[ERR] Укажите сторону за которую хотите проголосовать.`\n> `Светлая` - Мирные жители, врач, шериф\n> `Тёмная` - Мафия, Дон мафии.',
                delete_after=10)

        if str(ctx.author.id) in data[str(ctx.guild.id)].keys():
            with open("cogs/stavki.json", "w") as file:
                json.dump(data, file, indent=4)
            return await ctx.send(
                '`[ERR] Вы уже сделали свою ставку`.', delete_after=5)

        if storona.lower() == 'светлая':
            f += 1
            await ctx.send(
                f'`[ACCEPT]` {ctx.author.mention}, `вы успешно проголосовали за светлую сторону!`'
            )
            data[str(ctx.guild.id)][str(ctx.author.id)] = '1'
            member = discord.utils.get(
                ctx.guild.members, id=646573856785694721)
            await member.send(
                embed=discord.Embed(
                    description=
                    f'**Пользователь {ctx.author.display_name} | ID: {ctx.author.id} сделал ставку на `Светлую` сторону.**'
                ))

        elif storona.lower() == 'тёмная':
            f += 1
            await ctx.send(
                f'`[ACCEPT]` {ctx.author.mention}, `вы успешно проголосовали за тёмную сторону!`'
            )
            data[str(ctx.guild.id)][str(ctx.author.id)] = '2'
            member = discord.utils.get(
                ctx.guild.members, id=646573856785694721)
            await member.send(
                embed=discord.Embed(
                    description=
                    f'**Пользователь {ctx.author.display_name} | ID: {ctx.author.id} сделал ставку на `Тёмную` сторону.**'
                ))

        else:
            await ctx.send(
                '`[ERR] Укажите сторону за которую хотите проголосовать.`\n> `Светлая` - Мирные жители, врач, шериф\n> `Тёмная` - Мафия, Дон мафии.'
            )

        sdk = {'2': 'тёмную', '1': 'светлую'}
        if f == 20:
            stavka = []
            for i in data[str(ctx.guild.id)]:
                a = data[str(ctx.guild.id)][str(i)]
                stavka.append(
                    f'**Пользователь <@!{i}> выбрал `{sdk[a]}` сторону**\n')
            str_a = ''.join(stavka)
            member = discord.utils.get(
                ctx.guild.members, id=646573856785694721)
            await member.send(
                embed=discord.Embed(
                    description=f'**Пользователи сделавшие ставки:\n{str_a}**')
            )

        with open("cogs/stavki.json", "w") as file:
            json.dump(data, file, indent=4)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        cluster = MongoClient("mongodb+srv://dbrbase:oT4y7678BFK00Bsp@rodinadb.rhew3.mongodb.net/rodinaname?retryWrites=true&w=majority")
        db = cluster["rodina"]
        report = db["report"]
        role_registr = [
            'роль', 'роли', 'дайте роль', 'хочу роль', 'роль дайте',
            'выдайте роль', '-роль', 'Роль', 'Роли', 'Дайте роль', 'Хочу роль',
            'Роль дайте', 'Выдайте роль', '-Роль', '!Роль', '!роль',
            'снять роль у'
        ]
        if ctx.channel.id == 697518654140710964:
            creport = discord.utils.get(ctx.guild.categories, name='REPORT')
            prov = discord.utils.get(
                ctx.guild.channels, name=f'вопрос-{ctx.author.id}')

            msg = ctx.content.lower()
            if msg in role_registr:
                await ctx.delete()
                return await ctx.channel.send(
                    embed=discord.Embed(
                        description=
                        f'**❌ {ctx.author.name}, получать роли нужно только в канале <#577718720911376384>!**',
                        colour=0xFB9E14),
                    delete_after=5)
            if ctx.author.bot:
                if ctx.author.id == 729309765431328799:
                    return
                else:
                    await ctx.delete()
                    return
            else:
                await ctx.delete()

                if prov in creport.channels:
                    return await ctx.channel.send(
                        f'`[ERROR]` {ctx.author.mention}, `Вы уже имеете активный репорт! Для перехода в него нажмите на его название -` <#{prov.id}>.',
                        delete_after=10)

                channel = await ctx.guild.create_text_channel(
                    f'Вопрос {ctx.author.mention}',
                    overwrites=None,
                    category=creport,
                    reason='Создание нового Вопроса.')
                await ctx.channel.send(
                    embed=discord.Embed(
                        description=
                        f'**{ctx.author.mention}, Для вас создан канал - <#{channel.id}>, там Вы получите техническую поддержку от наших модераторов!**',
                        colour=0xFB9E14),
                    delete_after=20)
                await channel.set_permissions(ctx.author, read_messages=True, send_messages=True, read_message_history=True)
                embed1 = discord.Embed(description=f'''**Обращение к поддержке Discord**''', colour=0xFB9E14, timestamp=datetime.datetime.utcnow())
                embed1.add_field(name='Отправитель\n', value=f'**Пользователь:** `{ctx.author.display_name}`', inline=False)
                embed1.add_field(name='Суть обращения', value=f'{ctx.content}', inline=False)
                embed1.set_footer(text = 'Просмотр дополнительной инфоомации доступен по команде /помощь', icon_url = self.bot.user.avatar_url)
                await channel.send(
                    f'{ctx.author.mention} для команды поддержки <@&703270075666268160>\n',
                    embed=embed1)
                await channel.send(f'`[HELP]:` {ctx.author.mention}, `введя команду` **/помощь** `вы получите список информационных команд, которые возможно смогут Вам помочь!`', delete_after = 10)
                x = int(report.find_one({"proverka": "1"})["close"]) + 1
                y = int(report.find_one({"proverka": "1"})["active"]) + 1
                txt = ctx.content.replace('"', '')
                report.update_one({"proverka": "1"}, {"$set": {"vsego": x, "active": y, "last_name": ctx.author.display_name}})
                message_id = 796695355307065365
                chans = self.bot.get_channel(697518654140710964)
                message = await chans.fetch_message(message_id)
                emb23 = discord.Embed(description = f'Доброго времени суток! Вы попали в канал технической поддержки сервера **Rodina RP | Восточный округ**\nТут Вы можете узнать, как получить техническую поддержку от наших модераторов <@&703270075666268160>', colour=0xFB9E14, timestamp=datetime.datetime.utcnow())
                emb23.set_author(name='Rodina RP | Восточный округ | Support', icon_url= 'https://mydovidka.com/wp-content/uploads/2019/11/de0e202e9992854eade6f1ddf73dff49.png')
                emb23.add_field(name = 'Правила создания репорта', value = '```> Запрещены сообщения не несущие информации или вопроса.\n> Запрещено использовать ненормативную лексику.\n> Запрещено флудить @упоминаниями.\n> Запрещено создавать репорт с некорректным вопросом.\n> Запрещено оскорбительное и неадекватное поведение.\n> Для того что бы задать вопрос, вам необходимо написать его в этот канал.```', inline = False)
                emb23.add_field(name = 'Общее количество', value='\n'f'**⚙** `{x}` вопросов', inline = True)
                emb23.add_field(name = 'На рассмотрении', value = f'**⚙** `{y}` вопросов', inline = True)
                emb23.add_field(name = 'Обработано', value = f'**⚙** `{report.find_one({"proverka": "1"})["close"]}` вопросов\n', inline=True)
                emb23.add_field(name = 'Последний вопрос от:', value=f'`{ctx.author.display_name}`', inline = False)
                emb23.set_image(url=
                    'https://images-ext-2.discordapp.net/external/RoNgImbrFiwy16IZVStGaUy4ZZrJPSuVcRN1r7l-SQY/https/imgur.com/LKDbJeM.gif')
                emb23.set_footer(text=f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
                emb23.set_thumbnail(url='https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
                await message.edit(embed=emb23)
                logchan = self.bot.get_channel(735421035179933756)
                adre = await logchan.send(
                    '<@&703270075666268160>',
                    embed=discord.Embed(
                        description=
                        f'**Поступила новая жалоба от пользователя {ctx.author}.\nОна находится в канале `#{channel.name}`\n\nВам доступны команды:\n`>` /close `- Закрыть жалобу`\n`>` /active `- Поставить жалобу на рассмотрение.`\n`>` /add @Пользователь#1234 `- Добавить пользователя к вопросу`\n\nДля того, что бы взять этот вопрос нажмите на 💌 под этим сообщением!**',
                        colour=0xFB9E14))
                report.insert_one({"moder": 0, "rep_chat": channel.id, "rep_id": adre.id, "numid": ctx.author.id, "text": txt})
                await adre.add_reaction('💌')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        cluster = MongoClient("mongodb+srv://dbrbase:oT4y7678BFK00Bsp@rodinadb.rhew3.mongodb.net/rodinaname?retryWrites=true&w=majority")
        db = cluster["rodina"]
        report = db["report"]

        guild = self.bot.get_guild(payload.guild_id)
        if guild == None:
            return
        if not payload.guild_id == 577511138032484360:
            return

        user = self.bot.get_user(payload.user_id)
        if user.bot:
            return
        channel = self.bot.get_channel(payload.channel_id)
        if channel.id != 735421035179933756:
            return
        message = await channel.fetch_message(payload.message_id)
        memb = payload.member
        if not discord.utils.get(message.guild.roles, id = 703270075666268160) in memb.roles:
            return
        emoji = str(payload.emoji)
        if emoji == '💌':

            if report.count_documents({"rep_id": message.id}) == 0:
              await message.delete()
              return await channel.send(f'`[BUGTRACKER]:` `Был удалён багнутый репорт. ID: {message.id}`')

            if report.find_one({"rep_id": message.id})["moder"] > 0:
              mem = discord.utils.get(guild.members, id= report.find_one({"rep_id": message.id})["moder"])
              return await channel.send(f'`[NO ACCEPT]:` `Данный репорт был принят другим модератором({mem.display_name})`',delete_after=5)

            if report.count_documents({"moder": memb.id}) == 1:
                return await channel.send(f'`[NO ACCEPT]:` `Для начала закройте свой репорт(`<#{report.find_one({"moder": memb.id})["rep_chat"]}>`), что бы приняться за этот.`',delete_after=5)
            
            chat = guild.get_channel(report.find_one({"rep_id": message.id})["rep_chat"])
            prvvop = re.findall(r'\w*', chat.name)
            if int(prvvop[2]) == memb.id:
                return

            report.update_one({"rep_id": message.id}, {"$set": {"moder": memb.id}})
            await chat.set_permissions(memb,read_messages=True,read_message_history=True,send_messages=True)
            prvvop = re.findall(r'\w*', chat.name)
            await chat.send(f'`[NOTIFICATION]` `Агент технической поддержки` {memb.mention} `принял ваш репорт.`')
            member = guild.get_member(int(prvvop[2]))
            await message.edit(content='<@&703270075666268160>',embed=discord.Embed(description=f'**Поступила новая жалоба от пользователя {member}.\nОна находится в канале `#{chat.name}`\n\nВам доступны команды:\n`>` /close `- Закрыть жалобу`\n`>` /active `- Поставить жалобу на рассмотрение.`\n`>` /add @Пользователь#1234 `- Добавить пользователя к вопросу`\n\nМодератор {memb.display_name} принялся за данный репорт.**',colour=0xFB9E14))
            await message.clear_reactions()

    @commands.command(aliases=['close'])
    async def close_report(self, ctx):
        cluster = MongoClient("mongodb+srv://dbrbase:oT4y7678BFK00Bsp@rodinadb.rhew3.mongodb.net/rodinaname?retryWrites=true&w=majority")
        db = cluster["rodina"]
        report = db["report"]
        if not ctx.guild.id == 577511138032484360:
            return
        await ctx.message.delete()
        prvvop = re.findall(r'\w*', ctx.channel.name)
        if not prvvop[0] == 'вопрос':
            return

        member = discord.utils.get(ctx.guild.members, id=int(prvvop[2]))
        if not discord.utils.get(ctx.guild.roles, id=703270075666268160) in ctx.author.roles:
            return

        if not ctx.author.id == report.find_one({"rep_chat": ctx.channel.id})["moder"]:
          return

        if (prvvop[0] == "вопрос"):
          z = int(report.find_one({"proverka": "1"})["close"]) + 1
          y = int(report.find_one({"proverka": "1"})["active"]) - 1
          report.update_one({"proverka": "1"}, {"$set": {"close": z, "active": y, "last_name": ctx.author.display_name}})
          message_id = 796695355307065365
          chans = self.bot.get_channel(697518654140710964)
          message = await chans.fetch_message(message_id)
          emb23 = discord.Embed(description = f'Доброго времени суток! Вы попали в канал технической поддержки сервера **Rodina RP | Восточный округ**.\nТут Вы можете узнать, как получить техническую поддержку от наших модераторов <@&703270075666268160>', colour=0xFB9E14, timestamp=datetime.datetime.utcnow())
          emb23.set_author(name='Rodina RP | Восточный округ | Support', icon_url='https://mydovidka.com/wp-content/uploads/2019/11/de0e202e9992854eade6f1ddf73dff49.png')
          emb23.add_field(name = 'Правила создания репорта', value = '```> Запрещены сообщения не несущие информации или вопроса.\n> Запрещено использовать ненормативную лексику.\n> Запрещено флудить @упоминаниями.\n> Запрещено создавать репорт с некорректным вопросом.\n> Запрещено оскорбительное и неадекватное поведение.\n> Для того что бы задать вопрос, вам необходимо написать его в этот канал.```', inline = False)
          emb23.add_field(name=f'Общее количество', value=f'**⚙** `{report.find_one({"proverka": "1"})["vsego"]}` вопросов', inline = True)
          emb23.add_field(name = 'На рассмотрении', value = f'**⚙** `{y}` вопросов', inline = True)
          emb23.add_field(name = 'Обработано', value = f'**⚙** `{z}` вопросов\n', inline=True)
          emb23.add_field(name=f'Последний вопрос от:\n',value=f'`{member.display_name}`', inline = False)
          emb23.set_image(url='https://images-ext-2.discordapp.net/external/RoNgImbrFiwy16IZVStGaUy4ZZrJPSuVcRN1r7l-SQY/https/imgur.com/LKDbJeM.gif')
          emb23.set_footer(text=f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
          emb23.set_thumbnail(url='https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
          await message.edit(embed=emb23)
          await ctx.channel.send(embed=discord.Embed(description=f'**Вопросу №{int(prvvop[2])} установлен статус "Закрыт". Источник: <@!{ctx.author.id}>\n`Сообщения сохранены в системном файле`**',colour=0xFB9E14))
          await ctx.channel.set_permissions(member,read_messages=True,send_messages=False,read_message_history=True)
          await ctx.channel.set_permissions(ctx.author,read_messages=True,send_messages=False,read_message_history=True)
          messages = await ctx.channel.history(limit=1000).flatten()
          k = -1

          for i in range(len(messages) // 2):
              messages[k], messages[i] = messages[i], messages[k]
              k -= 1

          obfile = open(f'report-{member.id}.txt', 'w')
          obfile.write(f'[System]: Создание вопроса:\n\nК сообщению было добавлено: ==> {report.find_one({"rep_chat": ctx.channel.id})["text"]}\n\n\n')
          for i in messages:
            obfile.write(f'[{i.created_at.strftime("%m, %d - %H:%M:%S")}]{i.author.display_name}: {i.content}\n\n')
          obfile.close()

          channel2 = self.bot.get_channel(735421035179933756)
          await channel2.send(
          embed=discord.Embed(description=f'**Вопросу №{int(prvvop[2])} установлен статус "Закрыт". Источник: <@!{ctx.author.id}>\n`Сообщения сохранены в системном файле`**',colour=0xFB9E14),file=discord.File(fp=f'report-{member.id}.txt'))
          report.delete_one({"numid": int(prvvop[2])})
          try:
            await member.send(embed=discord.Embed(description=f'**{member.mention}, Вашему вопросу установлен статус: "Закрыт". Источник: {ctx.author.display_name}\n`Сообщения сохранены в системном файле`**',colour=0xFB9E14),file=discord.File(fp=f'report-{member.id}.txt'))
          except discord.Forbidden:
            pass
          os.remove(f'report-{member.id}.txt')
          await ctx.channel.edit(name=f'ticket-{member.id}')
          ccat = discord.utils.get(ctx.guild.categories, id=747712946305499196)
          await ctx.channel.edit(category=ccat)
          add(ctx.author, "close")
          if not member == ctx.author or not discord.utils.get(ctx.guild.roles,id=703270075666268160) in member.roles:
            mmsg = await ctx.channel.send(f'{member.mention}',embed=discord.Embed(title='Оценка ответа модератора',description=f'**На сколько хорошо ответил модератор {ctx.author.mention}?\nПожалуйста, нажмите на эмодзи с оценкой, на которую Вы оцениваете ответ модератора**'))
            r_list = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣']
            ocv = 0
            for r in r_list:
              await mmsg.add_reaction(r)
            try:
              react, user = await self.bot.wait_for('reaction_add',timeout=300,check=lambda react, user: user == member and react.message.channel == ctx.channel and react.emoji in r_list)
            except Exception:
              await mmsg.delete()
            else:
              if str(react.emoji) == r_list[0]:
                  ocv = 1
                  await mmsg.clear_reactions()
              elif str(react.emoji) == r_list[1]:
                  ocv = 2
                  await mmsg.clear_reactions()
              elif str(react.emoji) == r_list[2]:
                  ocv = 3
                  await mmsg.clear_reactions()
              elif str(react.emoji) == r_list[3]:
                  ocv = 4
                  await mmsg.clear_reactions()
              elif str(react.emoji) == r_list[4]:
                  ocv = 5
                  await mmsg.clear_reactions()
            if not ocv == 0:
                await mmsg.edit(context=f'{member.mention}',embed=discord.Embed(title='Оценка ответа модератора',description=f'**Вы оценили ответ модератора {ctx.author.mention} на `{ocv}` баллов**'))
                await channel2.send(embed=discord.Embed(title='Оценка ответа модератора',description=f'**Пользователь {member} оценил ответ модератора {ctx.author.mention} на `{ocv}` баллов**'))
                moder.update_one({"id": ctx.author.id}, {"$set": {"repa": moder.find_one({"id": ctx.author.id})["repa"] + ocv}})
            await asyncio.sleep(600)
            await ctx.channel.delete()
        else:
            return

    @commands.command(aliases=['active'])
    async def fon_active(self, ctx):
        if not ctx.guild.id == 577511138032484360:
            return
        await ctx.message.delete()
        prvvop = re.findall(r'\w*', ctx.channel.name)
        if not prvvop[0] == 'вопрос':
            return
        member = discord.utils.get(ctx.guild.members, id=int(prvvop[2]))
        if not discord.utils.get(
                ctx.guild.roles, id=703270075666268160) in ctx.author.roles:
            return
        await ctx.channel.send(
            embed=discord.Embed(
                description=
                f'**{member.mention}, Вашему вопросу №{int(prvvop[2])} установлен статус: "На рассмотрении". Источник: {ctx.author.display_name}**',
                colour=0xFB9E14,
                timestamp=datetime.datetime.utcnow()))
        channel2 = self.bot.get_channel(735421035179933756)
        await channel2.send(
            embed=discord.Embed(
                description=
                f'**Вопросу №{int(prvvop[2])} установлен статус "На рассмотрении". Источник: <@!{ctx.author.id}>**',
                colour=0xFB0E14,
                timestamp=datetime.datetime.utcnow()))
        await ctx.channel.set_permissions(
            member,
            read_messages=True,
            send_messages=False,
            read_message_history=True)
        add(ctx.author, "rasm")

    @commands.command(aliases=['add'])
    async def rep_add(self, ctx, member: discord.Member = None):
        if not ctx.guild.id == 577511138032484360:
            return
        await ctx.message.delete()

        if member == None or not member in ctx.guild.members:
            return await ctx.send(
                embed=discord.Embed(
                    description=
                    '**:grey_exclamation: Обязательно укажите: Пользователя!**'
                ),
                delete_after=10)
        prvvop = re.findall(r'\w*', ctx.channel.name)
        if not prvvop[0] == 'вопрос':
            return
        memb = discord.utils.get(ctx.guild.members, id=int(prvvop[2]))
        if not discord.utils.get(
                ctx.guild.roles, id=703270075666268160) in ctx.author.roles:
            return

        await ctx.channel.set_permissions(
            member,
            read_messages=True,
            send_messages=True,
            read_message_history=True)
        await ctx.channel.send(
            embed=discord.Embed(
                description=
                f'**{memb.mention}, к Вашему вопросу был добавлен пользователь {member.name}({member.mention})**',
                colour=0xFB9E14,
                timestamp=datetime.datetime.utcnow()))
        try:
            await member.send(
                embed=discord.Embed(
                    description=
                    f'**{member.mention}, вы были добавлены к вопросу №{int(prvvop[2])} на сервере {ctx.guild.name}.\nКанал вопроса: {ctx.channel.mention}**',
                    colour=0xFB9E14,
                    timestamp=datetime.datetime.utcnow()))
        except discord.Forbidden:
            pass


def setup(bot):
    bot.add_cog(reports(bot))
