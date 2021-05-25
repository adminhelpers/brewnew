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
import psutil as ps
import wikipedia


def bytes2human(number, typer=None):
    if typer == "system":
        symbols = ('KБ', 'МБ', 'ГБ', 'TБ', 'ПБ', 'ЭБ', 'ЗБ', 'ИБ')
    else:
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y') 

    prefix = {}

    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10

    for s in reversed(symbols):
        if number >= prefix[s]:
            value = float(number) / prefix[s]
            return '%.1f%s' % (value, s)

    return f"{number}B"

class funny(commands.Cog):
    """FUNNY Cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        print('Rodina 04 | Funny Commands Cog by dollar ム baby#3603 - Запущен')
    
    @commands.command()
    async def serverinfo(self, ctx):
        await ctx.channel.purge(limit=1)
        members = ctx.guild.members
        online = len(list(filter(lambda x: x.status == discord.Status.online, members)))
        offline = len(list(filter(lambda x: x.status == discord.Status.offline, members)))
        idle = len(list(filter(lambda x: x.status == discord.Status.idle, members)))
        dnd = len(list(filter(lambda x: x.status == discord.Status.dnd, members)))
        allchannels = len(ctx.guild.channels)
        allvoice = len(ctx.guild.voice_channels)
        alltext = len(ctx.guild.text_channels)
        allroles = len(ctx.guild.roles)

        embed = discord.Embed(title=f'🍀 Информация о сервере "{ctx.guild.name}"', colour=0xfB9E14, timestamp=ctx.guild.created_at)
        if ctx.guild.id == 577511138032484360:
            embed.add_field(name = f'<:verefication:733973297339039874> Верефикация', value = f'<:discord:733973856146030643> `Данный Discord-Сервер является оффициальным и подтвердждённым.`')
        embed.add_field(name = f'<:member:733973673614245919> Участники[{ctx.guild.member_count}]', value = f'<:bot:733975440619995187> `Ботов на сервере:` {len([m for m in members if m.bot])}\n<:online:733973364296908820> `Онлайн:` {online}\n<:idle:733973402985037856> `Не активен:` {idle}\n<:dnd:733973769219211295> `Не беспокоить:` {dnd}\n<:offline:733973444424761354> `Не в сети:` {offline}')
        embed.add_field(name = '<:owner:733973554206343168> Владелец сервер', value = f'{ctx.guild.owner.mention} `(Danil_Limanskiy | {ctx.guild.owner})`', inline = False)
        embed.add_field(name = f'<:channels:733973722305658881> Каналы[{allchannels}]', value = f"<:voice:733973591686643784> `Голосовых каналов:` {allvoice}\n<:text:733973626348371968> `Текстовых каналов:` {alltext}", inline = False)
        embed.add_field(name = 'Регион', value = f"<:region:733973506609381416> `Россия`", inline = False)
        embed.add_field(name = f"🔰 Уровень проверки", value = f'`Средний`', inline = False)
        teh1 = discord.utils.get(ctx.guild.roles, id = 703270075666268160)
        teh2 = discord.utils.get(ctx.guild.roles, id = 673481357657243649)
        ga = discord.utils.get(ctx.guild.roles, id = 577526148330815498)
        embed.add_field(name = f'💠 Роли[{allroles}]', value = f'`Высшая роль:` {ga.mention}\n`Роли агентов тех.поддержки:` {teh1.mention}({len(teh1.members)}) и {teh2.mention}', inline = False)
        embed.add_field(name = f'❔ ID', value = f'`{ctx.guild.id}`', inline = False)
        embed.set_thumbnail(url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
        embed.set_footer(text = f'Support Team by dollar ム baby#3603 | Дата создания сервера -', icon_url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
        await ctx.send(embed=embed)

    @commands.command(aliases=["bot", "botinfo", "ботинфо"],
        brief="Информация о боте",
        usage="бот <None>",
        description="Подробная информация о боте")
    async def _bot(self, ctx):
        memberbot = discord.utils.get(ctx.guild.members, id = 729309765431328799)
        await ctx.message.delete()
 
        members_count = 0
        guild_count = len(self.bot.guilds)
 
        for guild in self.bot.guilds:
            members_count += len(guild.members)
 
        embed1 = discord.Embed(title=f"Информация о боте {memberbot}",
                               description="Бот был написан для сервера Rodina RP | Восточный округ[04], но вы можете добавить его к себе на сервер!",
                               color=0xFB9E14)
        embed1.add_field(name=f'Бота создали:', value="dollar ム baby#3603", inline=True)
        embed1.add_field(name=f'Помощь в создании:', value="Google, Документация Discord.py", inline=True)
        embed1.add_field(name="‎‎‎‎", value="‎", inline=True)
        embed1.add_field(name=f'Бот написан на:', value="Discord.py", inline=True)
        embed1.add_field(name=f'Лицензия:', value="CC BY-SA-NC", inline=True)
        embed1.add_field(name="‎‎‎‎", value="‎", inline=True)
        embed1.add_field(name=f'Участников:', value=f"{members_count}", inline=True)
        embed1.add_field(name=f'Серверов:', value=f"{guild_count}", inline=True)
        embed1.add_field(name=f'Шардов:', value=f"{self.bot.shard_count}", inline=True)
        embed1.add_field(name=f'Приглашение Бота:',
                         value="[Тык](https://discord.com/api/oauth2/authorize?client_id=729309765431328799&permissions=8&scope=bot)",
                         inline=True)
        embed1.add_field(name=f'Сервер Rodina RP | Восточный округ[04]:', value="[Тык](https://discord.gg/HXA7jmT)",
                         inline=True)
        embed1.set_thumbnail(url = memberbot.avatar_url)
        
 
        # ==================
 
        mem = ps.virtual_memory()
        ping = self.bot.latency
 
        ping_emoji = "🟩🔳🔳🔳🔳"
        ping_list = [
            {"ping": 0.00000000000000000, "emoji": "🟩🔳🔳🔳🔳"},
            {"ping": 0.10000000000000000, "emoji": "🟧🟩🔳🔳🔳"},
            {"ping": 0.15000000000000000, "emoji": "🟥🟧🟩🔳🔳"},
            {"ping": 0.20000000000000000, "emoji": "🟥🟥🟧🟩🔳"},
            {"ping": 0.25000000000000000, "emoji": "🟥🟥🟥🟧🟩"},
            {"ping": 0.30000000000000000, "emoji": "🟥🟥🟥🟥🟧"},
            {"ping": 0.35000000000000000, "emoji": "🟥🟥🟥🟥🟥"}
        ]
        for ping_one in ping_list:
            if ping <= ping_one["ping"]:
                ping_emoji = ping_one["emoji"]
                break
 
        embed2 = discord.Embed(title='Статистика Бота', color=0xFB9E14)
 
        embed2.add_field(name='Использование CPU',
                         value=f'В настоящее время используется: {ps.cpu_percent()}%',
                         inline=True)
 
        embed2.add_field(name='Использование RAM',
                         value=f'Доступно: {bytes2human(mem.available, "system")}\n'
                               f'Используется: {bytes2human(mem.used, "system")} ({mem.percent}%)\n'
                               f'Всего: {bytes2human(mem.total, "system")}',
                         inline=True)
 
        embed2.add_field(name='Пинг Бота',
                         value=f'Пинг: {ping * 1000:.0f}ms\n'
                               f'`{ping_emoji}`',
                         inline=True)

        embed2.set_thumbnail(url = memberbot.avatar_url)

 
        for disk in ps.disk_partitions():
            try:
                usage = ps.disk_usage(disk.mountpoint)
                embed2.add_field(name="‎‎‎‎", value=f'```{disk.device}```',
                                inline=False)
                embed2.add_field(name='Всего на диске',
                                value=f'{bytes2human(usage.total, "system")}', inline=True)
                embed2.add_field(name='Свободное место на диске',
                                value=f'{bytes2human(usage.free, "system")}', inline=True)
                embed2.add_field(name='Используемое дисковое пространство',
                                value=f'{bytes2human(usage.used, "system")}', inline=True)
            except:
                pass

 
        embeds = [embed1, embed2]
 
        message = await ctx.send(embed=embed1)
        page = Paginator(self.bot, message, only=ctx.author, use_more=False, embeds=embeds, language="ru", footer_icon=self.bot.user.avatar_url, timeout=120, use_exit=True, delete_message=True, color=0xFB9E14, use_remove_reaction=True)
        await page.start()

    @commands.command()
    async def wiki(self, ctx, *, text = None):

        if text == None:
            return await ctx.send(embed = discord.Embed(description = f'**❌ {ctx.author.mention}, укажите что нужно искать.**'), delete_after = 5) 

        msg = await ctx.send(embed = discord.Embed(description = f'**:grey_exclamation: {ctx.author.mention}, начинаю загружать информацию, немного подождите.**'))
        wikipedia.set_lang("ru")
        new_page = wikipedia.page(text)
        summ = wikipedia.summary(text)
        try:
            emb = discord.Embed(title= f'\nСодержание запроса после парса: {new_page.title}', description= f'**\n{summ}**')
            emb.set_author(name = 'Информация из википедии', url = 'https://vk.com/norimyxxxo1702', icon_url = 'https://avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
            emb.set_footer(text = f'Информация показана для {ctx.author.display_name}', icon_url = ctx.author.avatar_url)
            await msg.edit(embed=emb)
        except:
            embed = discord.Embed(description = f'**❌ {ctx.author.mention}, мне не удалось найти информацию по запросу {text}.**')
            await msg.edit(embed=embed)

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        await ctx.channel.purge(limit=1)
        author = ctx.message.author

        user = ctx.message.author if (member == None) else member
        embed = discord.Embed( description = f'''{author.mention}, вот аватар пользователя {user.mention}:''', color= 0xFB9E14)
        embed.set_image(url=user.avatar_url_as(format = None, size = 4096))
        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        embed.set_thumbnail(url = 'https://psv4.userapi.com/c856336/u264775111/docs/d16/361841bb57ae/256kh256.png?extra=CdKRlvHHzIZQ2Sf6EZDC7xGxJeEQ7Bc_MpJF93mGTmr6OIFQK5pMldN12vqn-ofHpk_bG45rl6dqVI51r9a8Akxia5lebPhRg78DQLL9syvyA-UE70_u0VXyqUM-eQeohjgTg4YqGfov-YzS-5PMK8JxkXI')
        await ctx.send(embed=embed)

    @commands.command()
    async def га(self, ctx):

        if not ctx.guild.id == 577511138032484360:
            return

        await ctx.channel.purge(limit=1)
        author = ctx.message.author
        embed = discord.Embed(title = f'Главный Администратор', url = 'https://vk.com/limansky_danil', description = f'''{author.mention}, Главный администратор сервера - Rodina RP | Восточный Округ[04] - Danil Limanskiy\n\n💌 Ссылка на [В]Контакте - https://vk.com/limansky_danil\n\n📛 Discord Account: <@!388269410584100875>''', color=0xFB9E14)
        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        embed.set_thumbnail(url = 'https://images-ext-2.discordapp.net/external/bnUk9lweCuYaZT2wcaEVZllXV4GaWfVfwmU9WGI-5-I/https/images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
        await ctx.channel.send(embed = embed)

    @commands.command()
    async def зга(self, ctx):
        if not ctx.guild.id == 577511138032484360:
            return

        await ctx.channel.purge(limit=1)
        author = ctx.message.author
        embed = discord.Embed(title = f'Заместитель Главного Администратора', url = 'https://vk.com/id449840074', description = f'''{author.mention}, Заместитель Главного Администратора - Rodina RP | Восточный Округ[04] - Yan Kalashnikov\n\n💌 Ссылка на [В]Контакте - https://vk.com/id449840074\n📛 Discord Account: <@!435732124855828480>''', color=0xFB9E14)
        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        embed.set_thumbnail(url = 'https://images-ext-2.discordapp.net/external/bnUk9lweCuYaZT2wcaEVZllXV4GaWfVfwmU9WGI-5-I/https/images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
        await ctx.channel.send(embed = embed)

    @commands.command()
    async def куратор(self, ctx):
        if not ctx.guild.id == 577511138032484360:
            return

        await ctx.channel.purge(limit=1)
        author = ctx.message.author
        embed = discord.Embed(title = f'Куратор Сервера', url = 'https://vk.com/id218670754', description = f'''{author.mention}, Куратор сервера - Rodina RP | Восточный Округ[04] - Haruma Ramirez\n\n💌 Ссылка на [В]Контакте - https://vk.com/id218670754\n📛 Discord Account: <@!400077809478795275>''', color=0xFB9E14)
        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        embed.set_thumbnail(url = 'https://images-ext-2.discordapp.net/external/bnUk9lweCuYaZT2wcaEVZllXV4GaWfVfwmU9WGI-5-I/https/images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
        await ctx.channel.send(embed = embed)

    @commands.command()
    async def тех(self, ctx):
        if not ctx.guild.id == 577511138032484360:
            return
            
        await ctx.channel.purge(limit=1)
        author = ctx.message.author
        embed = discord.Embed(title = f'Технический Администратор', url = 'https://vk.com/norimyxxxo1702', description = f'''{author.mention}, Технический администратор Discord Channel - Daniel Moscovskiy\n\n💌 Ссылка на [В]Контакте - https://vk.com/norimyxxxo1702\n📛 Discord Account: <@!646573856785694721>''', color=0xFB9E14)
        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        embed.set_thumbnail(url = 'https://images-ext-2.discordapp.net/external/bnUk9lweCuYaZT2wcaEVZllXV4GaWfVfwmU9WGI-5-I/https/images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
        await ctx.channel.send(embed = embed)


    @commands.command(aliases=['коронавирус', 'ковид'])
    async def cov(self, ctx, country):
        for item in json.loads(requests.get("https://corona.lmao.ninja/v2/countries").text):
            if item['country'] == country: 
                embed = discord.Embed(title=f'Статистика Коронавируса | Страна: {country}')
                embed.add_field(name='👨‍⚕ Выздоровело:',          value=f'{item["recovered"]} человек')
                embed.add_field(name='🧬 Заболеваний:',          value=f'{item["cases"]} человек')
                embed.add_field(name='😲 Погибло:',              value=f'{item["deaths"]} человек')
                embed.add_field(name='🌏 Заболеваний за сутки:', value=f'+{item["todayCases"]} человек')
                embed.add_field(name='🔞 Погибло за сутки:',     value=f'+{item["todayDeaths"]} человек')
                embed.add_field(name='🔰 Проведено тестов:',     value=f'Всего {item["tests"]} штук')
                embed.add_field(name='💊 Активные зараженные:',  value=f'{item["active"]} человек')
                embed.add_field(name='🤧 В тяжелом состоянии:',  value=f'Находится {item["critical"]} человек')
                embed.set_thumbnail(url=item["countryInfo"]['flag'])
                embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')

                return await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx):
        if not ctx.guild.id == 577511138032484360:
            return

        await ctx.message.delete()
        emb = discord.Embed(title = f'Каталог команды помощи', url = 'https://vk.com/norimyxxxo1702', description = f'`Страница 1` - Каталог\n`Страница 2 | Часть 1` - Пользовательские команды\n`Страница 2 | Часть 2` - Команды модераторов/лидеров\n`Страница 2 | Часть 3` - Команды приватных каналов.\n`Страница 3` - Команды игры в Мафию\n\n➡ **Пользовательские команды.**', color=0xFB9E14)
        embed = discord.Embed(title = f'Пользовательские команды', url = 'https://vk.com/norimyxxxo1702', description = f'`/covid` - Случаи заражения в России\n`/cov <country>` - Случаи заражения в выбраной стране\n`/avatar <member>` - Посмотреть аватар пользователя.\n`/rep <member> [reason]` - Подача жалобы на пользователя\n`/warnlog` - Проверить список своих предупреждений\n\n**Информационные:**\n`/га` - Информация о главном администраторе\n`/зга` - Посмотреть информацию о заместителе главного администратора\n`/куратор` - Информация о кураторе сервера\n`/тех` - Информация о техническом администраторе Discord\n`/serverinfo` - Посмотреть информацию о сервере Discord\n`/user <member>` - Посмотреть информацию о пользователе\n`/botinfo` - Посмотреть информация о боте\n`/invite` - Получить единую ссылку на приглашение пользователей\n\n`/coins` - Проверить кол-во своих монет\n`/casino [ставка]` - Сделать ставку в казино(Монетами)\n`/pay @Пользователь#1234 [сумма]` - Передать деньги игроку\n\n`/dog` - Случайное фото собаки\n`/cat` - Случайное фото кота\n`/panda` - Случайное фото панды\n`/bird` - Случайное фото прицы\n`/fox` - Случайное фото лисы\n`/pikachu` - Случаное фото пикачу\n\n`/mem` - Случайны мем(На английском языке)\n`/gflags` - Игра "Угадай страну по фразу"\n`/теннис @Пользователь#1234 [сумма]` - Игра "Теннис"\n\nНе нашли ответ на свой вопрос? Задайте его в <#697518654140710964>\n\n⏩ **Просмотр команд модераторов.**\n⬅ **Каталог**', color=0xFB9E14)
        embedq = discord.Embed(title = f'Команды для модераторов Discord', url = 'https://vk.com/norimyxxxo1702', description = f'`/clear <amount>` - Очистить чат\n> **Указывайте пользователя после команды что бы удалить сообщения от него.**\n`/vmute` - Выдать голосовой мут.\n`/vunmute` - Снять голосовой мут.\n`/ban @Провокатор#1234 [Причина]` - Забанить пользователя на сервере\n`/kick @Провокатор#1234 [Причина]` - Выгнать пользователя с сервера\n`/mute @Провокатор#1234 [Время] [Причина]` - Выдать мут пользователю\n`/unmute @Пользователь#1234` - Снять мут пользователю.\n`/warn @Провокатор#1234 [Причина]` - Выдать предупреждение пользователю\n> `/unwarn [№ Случая]` - Снять пользователю предупреждение(/warnlog @Пользователь#1234 - Узнать номер)\n\n**Доступно для команды поддержки <@&703270075666268160>**\n\n⏩ **Просмотр информации о приватных каналах.**\n⬅ **Каталог**\n⏪ **Просмотр пользовательских команд**', color = 0xFB9E14)
        embedw = discord.Embed(title = 'Информация о приватных каналах', url = 'https://vk.com/norimyxxxo1702', description = f'`/padd <member>` - Добавить человека в свой канал\n`/rpadd <member>` - Отозвать права пользователя в вашем канале\n**Описание данной системы в канале -** <#673188188189360138>\n**Информация о командах для приватных каналов -** <#701760746685464616>\n**Для создания своего приватного канала подключитесь к каналу -** `✅ Перемещение в приват`\n\n➡ **Команды идля ведущих мафии**\n⏪ **Просмотр команд**', color = 0xFB9E14)
        embed2 = discord.Embed(title = f'Игра в мафию', url = 'https://vk.com/norimyxxxo1702', description = f'**💬 | Выдача времени:**\n> **`Ознакомительная, За столом, Предсмертная речи` - 1 Минута**\n> **`Оправдательная речь` - 30 секунд**\n> **Речь за столом после 0 круга, должна быть не менее 20 секунд.** `За нарушение выдаётся фол`\n> **События происходят в городе**\n\n💬 Список команд\n> **`/msts` - Начать игру**\n> **1. `/убить <member/memberID>` - Убить игрока**\n> **2. `/фол <member/memberID>` - Выдать фол игроку**\n> **3. `/унфол <member/memberID>` - Снять фол игроку**\n> **4. `/night` - Устанавовить режим "Ночь"(выключение микрофонов и закрытие чата)**\n> **6. `/day` - Установить режим "День"(Включение микрофонов и открытие чата, если у игрока 3 фола, мут не снимает)**\n> **7. `/mstop` - Закончить мафию**\n> **8. `/выставить <member/memberID>` - Выставить игрока на голосование**\n> **9. `/ungolos <member/memberID>` - Снять игрока с голосования**\n> **10. `/голосование` - Запустить режим голосования в канале "Чат-Мафии"**\n> **11. `/golist` - Посмотреть список проголосовавших.**\n> **12. `/линк` - Сделать упоминание о мафии(Раз в 10 минут)**\n> **13. `/heal` - Вернуть пользователя в игру(Если был убит по ошибке)**\n> **14. `/swap_ved @Пользователь#1234` - Передать права ведущего пользователю**\n> **15. `/gamerole` - Запросить список игроков мафии с описанием их ролей**\n**[P.S]: `/act` - Если игра забагалась, пишите это и после `/mstop`**\n\n**Доступно только ведущим!**\n\n⬅ **Пользовательские команды**', color=0xFB9E14)
        embeds = [emb, [embed, embedq, embedw], embed2]
        message = await ctx.send(embed = embed)
        page = Paginator(self.bot, message, only=ctx.author, use_more=True, embeds=embeds, language="ru", footer_icon=self.bot.user.avatar_url, timeout=300, use_exit=True, delete_message=True, color=0xFB9E14, use_remove_reaction=True)
        await page.start()

    @commands.command()
    async def dog(self, ctx):
        response = requests.get('https://api.thedogapi.com/v1/images/search')
        json_data = json.loads(response.text)
        url = json_data[0]['url']

        embed = discord.Embed(color = 0xFB9E14)
        embed.set_image( url = url )

        await ctx.send( embed = embed )

    @commands.command()
    async def cat(self, ctx):
        for item in json.loads(requests.get("https://api.thecatapi.com/v1/images/search").text):
            embed = discord.Embed(color = discord.Color.blue())
            embed.set_image(url = item["url"])
            await ctx.send(embed=embed)

    @commands.command()
    async def panda(self, ctx):
        response = requests.get('https://some-random-api.ml/img/panda')
        jsoninf = json.loads(response.text)
        url = jsoninf['link']
        embed = discord.Embed(color = 0xFB9E14)
        embed.set_image(url = url)
        await ctx.send(embed = embed)

    @commands.command()
    async def bird(self, ctx):
        response = requests.get('https://some-random-api.ml/img/birb')
        jsoninf = json.loads(response.text)
        url = jsoninf['link']    
        embed = discord.Embed(color = 0xFB9E14)
        embed.set_image(url = url)
        await ctx.send(embed = embed)

    @commands.command()
    async def mem(self, ctx):
        response = requests.get('https://some-random-api.ml/meme')
        jsoninf = json.loads(response.text)
        url = jsoninf['image']    
        embed = discord.Embed(color = 0xFB9E14)
        embed.set_image(url = url)
        await ctx.send(embed = embed)

    @commands.command()
    async def pikachu(self, ctx):
        response = requests.get('https://some-random-api.ml/pikachuimg')
        jsoninf = json.loads(response.text)
        url = jsoninf['link']    
        embed = discord.Embed(color = 0xFB9E14)
        embed.set_image(url = url)
        await ctx.send(embed = embed)

    @commands.command()
    async def fox(self, ctx):
        num = random.randint(1, 122)

        embed = discord.Embed(color = 0xFB9E14)
        embed.set_image( url = f'https://randomfox.ca/images/{num}.jpg' )

        await ctx.send( embed = embed )

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        if guild == None:
          return
        if not guild.id == 325607843547840522:
            return

        user = self.bot.get_user(payload.user_id)
        if user.bot:
            pass
        else:
            emoji = str(payload.emoji)
            channel = self.bot.get_channel(payload.channel_id)
            if not channel.id == 751102579290800200:
                return
            message = await channel.fetch_message(payload.message_id)
            if not message.id == 751107927783243866:
                return
            memb = discord.utils.get(message.guild.members, id=payload.user_id)
            
            if emoji == '🎊':
                return await memb.add_roles(discord.utils.get(guild.roles, id = 751105628369584138))
            elif emoji == '🧛':
                return await memb.add_roles(discord.utils.get(guild.roles, id = 751108470270460016))
            elif emoji == '🎤':
                return await memb.add_roles(discord.utils.get(guild.roles, id = 751108473755795658))
            elif emoji == '🎥':
                return await memb.add_roles(discord.utils.get(guild.roles, id = 751108473995132939))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        if guild == None:
          return
        if not guild.id == 325607843547840522:
            return

        user = self.bot.get_user(payload.user_id)
        if user.bot:
            pass
        else:
            emoji = str(payload.emoji)
            channel = self.bot.get_channel(payload.channel_id)
            if not channel.id == 751102579290800200:
                return
            message = await channel.fetch_message(payload.message_id)
            if not message.id == 751107927783243866:
                return
            memb = discord.utils.get(message.guild.members, id=payload.user_id)
            
            if emoji == '🎊':
                return await memb.remove_roles(discord.utils.get(guild.roles, id = 751105628369584138))
            elif emoji == '🧛':
                return await memb.remove_roles(discord.utils.get(guild.roles, id = 751108470270460016))
            elif emoji == '🎤':
                return await memb.remove_roles(discord.utils.get(guild.roles, id = 751108473755795658))
            elif emoji == '🎥':
                return await memb.remove_roles(discord.utils.get(guild.roles, id = 751108473995132939))


def setup(bot):
    bot.add_cog(funny(bot))