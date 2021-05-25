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

conn = sqlite3.connect("cogs/database.db")
cursor = conn.cursor()

global chisla
chisla = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']

global chisla1
chisla1 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']

global get_role
get_role = [ ]

global role
role = ['Мафия', 'Дон мафии', 'Шериф', 'Врач', 'Мирный житель 1', 'Мирный житель 2', 'Мирный житель 3', 'Мирный житель 4', 'Мирный житель 5', 'Мирный житель 6']

global i
i = 0

class testmafia(commands.Cog):
    """mafia Cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        print('Rodina 04 | Game of Mafia by dollar ム baby#3603 - Запущен')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before = None, after = None):
        global chisla
        global chisla1

        if not member.guild.id == 577511138032484360:
            return

        if after.channel == None:
            if before.channel.id == 727111883018207303:
                for row in cursor.execute('SELECT `name`, `number` FROM `mafia` WHERE `id` = {}'.format(member.id)):
                    await member.edit(nick = row[0])
                    if row[1] == 11 or row[1] == 12:
                        if row[1] == 12:
                            await member.remove_roles(discord.utils.get(member.guild.roles, id = 727112347105099877))
                        cursor.execute('DELETE FROM `mafia` WHERE `id` = {}'.format(member.id))
                        conn.commit()
                        return

                    await member.remove_roles(discord.utils.get(member.guild.roles, id = 720958695764131850))
                    if row[1] == 10:
                        chisla.append(f'{row[1]}')
                    elif row[1] < 10:
                        chisla.append(f'0{row[1]}')
                    cursor.execute('DELETE FROM `mafia` WHERE `id` = {}'.format(member.id))
                    conn.commit()

        if (not before.channel == None) and (not after.channel == None):
            if before.channel.id == after.channel.id:
                return

            if before.channel.id == 727111883018207303:
                for row in cursor.execute('SELECT `name`, `number` FROM `mafia` WHERE `id` = {}'.format(member.id)):
                    await member.edit(nick = row[0])
                    if row[1] == 11 or row[1] == 12:
                        if row[1] == 12:
                            await member.remove_roles(discord.utils.get(member.guild.roles, id = 727112347105099877))
                        cursor.execute('DELETE FROM `mafia` WHERE `id` = {}'.format(member.id))
                        conn.commit()
                        return

                    await member.remove_roles(discord.utils.get(member.guild.roles, id = 720958695764131850))

                    if row[1] == 10:
                        chisla.append(f'{row[1]}')
                    elif row[1] < 10:
                        chisla.append(f'0{row[1]}')
                    cursor.execute('DELETE FROM `mafia` WHERE `id` = {}'.format(member.id))
                    conn.commit()
                    return

        if not after.channel == None:

            if after.channel.id == 727111883018207303:
                if discord.utils.get(member.guild.roles, id = 727112273704779797) in member.roles:
                    cursor.execute('INSERT INTO `mafia` (id, name, number, role) VALUES ({}, "{}", 11, 1)'.format(member.id, member.display_name))
                    conn.commit()
                    await member.edit(nick = '[MAFIA]: Ведущий')
                    return

                elif len(chisla) == 0:
                    cursor.execute('INSERT INTO `mafia` (id, name, number, role) VALUES ({}, "{}", 12, 1)'.format(member.id, member.display_name))
                    conn.commit()
                    await member.add_roles(discord.utils.get(member.guild.roles, id = 727112347105099877))
                    await member.edit(nick = 'SPECTATOR')
                    return

                else:
                    i = min(chisla)
                    cursor.execute('INSERT INTO `mafia` (id, name, number, role) VALUES ({}, "{}", {}, 0)'.format(member.id, member.display_name, i))
                    conn.commit()
                    chisla.remove(i)
                    await member.add_roles(discord.utils.get(member.guild.roles, id = 720958695764131850))
                    await member.edit(nick = i)

    @commands.command()
    async def mstart(self, ctx):
        global i
        global get_role
        global role
        channel = self.bot.get_channel(727111883018207303)
        rolf = discord.utils.get(ctx.guild.roles, id = 727112273704779797)
        err1 = discord.Embed(description = '**Вы не можете начать игру в мафию!\nПроверьте наличие выполнения следующих параметров:**', colour = 0xFB9E14)
        err1.add_field(name = 'Параметр №1', value = f'> `Вы являетесь ведущим и имеете роль` {rolf.mention}', inline = False)
        err1.add_field(name = 'Параметр №2', value = f'> `Вы находитесь в голосовом канале` **{channel.name}**', inline = False)
        err1.add_field(name = 'Параметр №3', value = f'> `В канале ииеется` **10** `участников с номерами от` **01** `до` **10**', inline = False)
        if not ctx.author in channel.members: 
            await ctx.send(embed = err1)
            return
        if not rolf in ctx.author.roles:
            await ctx.send(embed = err1)
            return
        if not len(channel.members) >= 10:
            await ctx.send(embed = err1)
            return

        if i == 1:
            await ctx.send(f'`[ERR]:` {ctx.author.mention}, `на данный момент игра уже проводится!`')
            return

        rved = discord.utils.get(ctx.guild.roles, id = 727112273704779797)
        rols = discord.utils.get(ctx.guild.roles, id = 720958695764131850)
        f = 0
        ath = re.split(r'\W+', str(role[4]))
        for i in channel.members:
            a = random.randint(0, len(role) - 1)
            if rols in i.roles:
                embed = discord.Embed(description = f'**Привет {i.mention}! Ты учавствуешь в мафии на сервере {ctx.guild.name} :)**', colour = 0xFB9E14)

                if role[a] == 'Дон мафии':
                    chan = self.bot.get_channel(727111728990781481)
                    await chan.set_permissions(i, read_messages = True, view_channel = True, send_messages = True, read_message_history = True)
                    embed.add_field(name = '❤️ Информация о тебе:', value = f'> `Твоя роль:` **Дон Мафии**\n> `Канал тёмной стороны:` {chan.mention}.', inline = False)
                    get_role.append(f'> 🧛‍♂ `Дон Мафии -` {i.display_name} | `ID:` {i.id}\n')
                    cursor.execute(f'UPDATE `mafia` SET `role` = "Дон мафии" WHERE `id` = {i.id}')
                    conn.commit()
                    role.remove('Дон мафии')
                elif role[a] == 'Мафия':
                    chan = self.bot.get_channel(727111728990781481)
                    await chan.set_permissions(i, read_messages = True, view_channel = True, send_messages = True, read_message_history = True)
                    await chan.send(embed = discord.Embed(description = 'Привет! Данный чат создан для тёмной стороны города! Доступ в него имеют только красные отрицательные роли: Мафия, Дон Мафии.'))
                    embed.add_field(name = '❤️ Информация о тебе:', value = f'> `Твоя роль:` **Мафия**\n> `Канал тёмной:` {chan.mention}.', inline = False)
                    get_role.append(f'> 🤵 `Мафия -` {i.display_name} | `ID:` {i.id}\n')
                    cursor.execute(f'UPDATE `mafia` SET `role` = "Мафия" WHERE `id` = {i.id}')
                    conn.commit()
                    role.remove('Мафия')
                elif role[a] == 'Шериф':
                    embed.add_field(name = '❤️ Информация о тебе:', value = f'> `Твоя роль:` **Шериф**', inline = False)
                    get_role.append(f'> 🕵 `Шериф -` {i.display_name} | `ID:` {i.id}\n')
                    cursor.execute(f'UPDATE `mafia` SET `role` = "Шериф" WHERE `id` = {i.id}')
                    conn.commit()
                    role.remove('Шериф')
                elif role[a] == 'Врач':
                    embed.add_field(name = '❤️ Информация о тебе:', value = f'> `Твоя роль:` **Врач**', inline = False)
                    get_role.append(f'> 👨‍⚕ `Врач -` {i.display_name} | `ID:` {i.id}\n')
                    cursor.execute(f'UPDATE `mafia` SET `role` = "Врач" WHERE `id` = {i.id}')
                    conn.commit()
                    role.remove('Врач')
                elif ath[0] == 'Мирный':
                    f += 1
                    embed.add_field(name = '❤️ Информация о тебе:', value = f'> `Твоя роль:` **Мирный житель**', inline = False)
                    get_role.append(f'> 👨‍💻 `Мирный житель -` {i.display_name} | `ID:` {i.id}\n')
                    cursor.execute(f'UPDATE `mafia` SET `role` = "Мирный житель {f}" WHERE `id` = {i.id}')
                    conn.commit()
                    role.remove(f'Мирный житель {f}')

                embed.add_field(name = '🛡️ Правила игры', value = '**На всё лобби раздаётся 10 ролей, каждая из них должна выполнять определённые действия.**\n> `Главная цель белой стороны:` **Раскрыть всех тёмных личностей**.\n> `Главная цель тёмной стороны:` **Убить всех белых личностей**', inline = False)
                embed.add_field(name = '🚀 В данной игре запрещено', value = '> Перебивать ведущего\n> Разговаривать в ночное время.\n> Заключать содружетсво между враждующими сторонами\n> Бездействовать\n> Оскорблять кого-либо', inline = False)
                embed.add_field(name = '🌟 `Роли игроков`', value = '> Мафия\n> Дон мафии\n> Врач\n> Шериф\n> 6 Мирных жителей\n\n', inline = False)
                embed.add_field(name = '💬 `Что делает Мафия?`', value = '**Убивает людей по ночам. Старается убирать "Красные роли", то есть шерифа или врача, для того чтобы те не смогли рассекретить мафию или исцелить её жертв. Для убийства 1 человека, необходимо согласие самой Мафии и Дона мафии. После убийства, жертва выбывает из игры, если её не исцелит Врач. Победа мафии объявляется только в том случае, если из игры выбывают все игроки имеющие красные роли**', inline = False)
                embed.add_field(name = '💬 `Что делает Шериф?`', value = '**Он является активной "Красной ролью". Задача шерифа- найти и рассекретить мафию и Дона Мафии. После действий шерифа - человек на которого были возложены обвинения выбывает из игры.**', inline = False)
                embed.add_field(name = '💬 `Что делает Врач?`', value = '**У человека с этой ролью есть возможность исцелять 1 любого человека на его выбор включая себя, каждую ночь. При этом, ему запрещается лечить себя 2 раза за игру. Если он исцеляет игрока, которого выбрала сторона мафии - игрок остаётся в игре.**', inline = False)
                embed.add_field(name = '💬 `Что делают Мирные жители?`', value = '**Задача этой роли, путём дневного обсуждения вычислить мафию. Человек с этой ролью имеет право последнего слово и может озвучить свои подозрения в сторону любого игрока.**', inline = False)
                embed.add_field(name = '🎮 `На этом мы подошли к концу`', value = f'**Наша команда желает Вам удачи в самой игре и приятного времяпровождения в Discord Канале {ctx.guild.name} ❤️**')
                embed.set_author(name = 'Мафия Информатор', url = 'https://vk.com/norimyxxxo1702', icon_url = 'https://sun9-36.userapi.com/c854428/v854428073/228488/tvUKvnDpcdk.jpg')
                embed.set_footer(text = f'С уважением команда модерации Восточного Округа!', icon_url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
                embed.set_thumbnail(url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
                await i.send(embed = embed)
        for i in channel.members:
            if rved in i.roles:
                str_a = ''.join(get_role)
                embed = discord.Embed(description = f'**Список игроков:**\n{str_a}\n**Можно начинать!**')
                embed.set_author(name = 'Информация для ведущего', url = 'https://vk.com/norimyxxxo1702', icon_url = 'https://sun9-36.userapi.com/c854428/v854428073/228488/tvUKvnDpcdk.jpg')
                embed.set_footer(text = f'С уважением команда модерации Восточного Округа!', icon_url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
                embed.set_thumbnail(url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
                await i.send(embed = embed)
        i = 1

    @commands.command()
    async def mreset(self, ctx):
        global i
        global role
        global get_role
        rolf = discord.utils.get(ctx.guild.roles, id = 727112273704779797)
        if not rolf in ctx.author.roles:
            await ctx.send('`[ERR]: Ошибка доступа.`')
            return

        i = 0
        get_role = [ ]
        role = ['Мафия', 'Дон мафии', 'Шериф', 'Врач', 'Мирный житель 1', 'Мирный житель 2', 'Мирный житель 3', 'Мирный житель 4', 'Мирный житель 5', 'Мирный житель 6']
        channel = self.bot.get_channel(727111883018207303)
        for i in channel.members:
            c = self.bot.get_channel(727111784682487888)
            await i.move_to(c)
        rol = discord.utils.get(ctx.guild.roles, id = 727112273704779797)
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel = False, read_messages=False, read_message_history = False),
            rol: discord.PermissionOverwrite(view_channel = True, read_messages=True, send_messages = True, read_message_history = True)
            }
        chan = self.bot.get_channel(727111728990781481)
        await chan.edit(overwrites = overwrites)
        await ctx.send(f'`[ACCEPT]:` {ctx.author.mention}, `рестарт Мафии прошёл успешно`.')

    @commands.command()
    async def mkill(self, ctx, member: discord.Member = None):
        global get_role
        global role

        rolf = discord.utils.get(ctx.guild.roles, id = 727112273704779797)
        if not rolf in ctx.author.roles:
            await ctx.send('`[ERR]: Ошибка доступа.`')
            return

        s = 0
        for i in cursor.execute(f'SELECT `id`, `name`, `role` FROM `mafia` WHERE `id` = {member.id}'):
            if i[0] > 0:
                s = 1

        embed = discord.Embed(description = f'**Возможно данный пользователь вышел из игры во время её проведения.', colour = member.color)
        if not s == 1:
            await ctx.send(f'`[ERR]:` {ctx.author.mention}, `данный пользователь не зарегестрирован в базе данных и не является участником игры.`', embed = embed)
            return

        await member.edit(nick = f'{member.display_name} | KILL')
        for i in cursor.execute(f'SELECT `id`, `name`, `role` FROM `mafia` WHERE `id` = {member.id}'):
            if i[2] == 0:
                await ctx.send(f'`[ERR]:` {ctx.author.mention}, `данный пользователь не зарегестрирован в базе данных и не является участником игры.`', embed = embed)
                return

            role.append(i[2])
            if i[2] == 'Мафия' or i[2] == 'Дон мафии':
                chan = self.bot.get_channel(727111728990781481)
                await chan.set_permissions(member, read_messages = False, view_channel = False, send_messages = False, read_message_history = False)
            text = f'`[System]: Игрок {i[1]}({member.display_name}) был убит.`'
            for z in self.bot.get_channel(727111883018207303).members:
                await z.send(text)

    @commands.command(pass_context = True)
    @commands.has_permissions(administrator = True)
    async def mafia(self, ctx):

        def check(m):
            return m.author == ctx.author and m.channel == ctx.author

        msg = self.bot.wait_for('message', check = check)
        if msg.content.lower() == 'отмена':
            await msg.delete()
            return await ctx.message.delete()
        
        await msg.delete()

        def check2(c):
            return c.author == ctx.author and c.channel == ctx.author

        msg2 = self.bot.wait_for('message', check = check2)
        if msg2.content.lower() == 'отмена':
            await msg2.delete()
            return await ctx.message.delete()

        await msg2.delete()
        await ctx.message.delete()
        embed = discord.Embed(description = f'**Салют всем участникам Discord Сервера {ctx.guild.name}!\n\nCовсем скоро, а именно {msg.content}, в {msg2.content} будет проведено мероприятие под названием "Мафия".\nСейчас мы расскажем о нём немного больше.**', colour = 0xFFFFF, timestamp = ctx.message.created_at)
        embed.add_field(name = '💼 `Что это такое?`', value = f'**😈 Это командная игра, в которой есть две враждующие стороны, тёмная и светлая.\nЦель каждой команды: Узнать своих противников в лицо и избавиться от них максимально быстро.**', inline = False)
        embed.add_field(name = '👼 `Белая сторона`', value = f'**👨‍⚕ Это 6 обычных ролей, в лице которых выступают мирные жители и 2 красные, а именно Врач и Шериф. **', inline = False)
        embed.add_field(name = '💬 `Что делает Шериф?`', value = '**Он является активной "Красной ролью". Задача шерифа- найти и рассекретить мафию и Дона Мафии. После действий шерифа - человек на которого были возложены обвинения выбывает из игры.**', inline = False)
        embed.add_field(name = '💬 `Что делает Врач?`', value = '**У человека с этой ролью есть возможность исцелять 1 любого человека на его выбор включая себя, каждую ночь. При этом, ему запрещается лечить себя 2 раза за игру. Если он исцеляет игрока, которого выбрала сторона мафии - игрок остаётся в игре.**', inline = False)
        embed.add_field(name = '💬 `Что делают Мирные жители?`', value = '**Задача этой роли, путём дневного обсуждения вычислить мафию. Человек с этой ролью имеет право последнего слово и может озвучить свои подозрения в сторону любого игрока.**', inline = False)
        embed.add_field(name = '🕵🏾 `Черная сторона`', value = '**Это 2 красных, ключевых роли. Они должны играть в команде и выбирать тех, кто может разрушить их коварные планы. При этом, им нужно использовать максимально стратегичную схему выступления на общих собраниях и личным минутах, что бы не раскрыть себя раньше времени.**', inline = False)
        embed.add_field(name = '💬 `Что делает Мафия?`', value = '**Убивает людей по ночам. Старается убирать "Красные роли", то есть шерифа или врача, для того чтобы те не смогли рассекретить мафию или исцелить её жертв. Для убийства 1 человека, необходимо согласие самой Мафии и Дона мафии. После убийства, жертва выбывает из игры, если её не исцелит Врач. Победа мафии объявляется только в том случае, если из игры выбывают все игроки имеющие красные роли**', inline = False)
        embed.add_field(name = '🥂 `Ставки`', value = '**Так же, для первых 20-ти человек, будет доступна базовая команда `/ставка [Светлая/Тёмная]`.\nПрописав её, Вы сможете сделать ставку на победу той или иной команды.\nКоманда людей, которые смогут угадать, какая команда наберёт больше побед в серии из `3-х` игр, разделит общий банк - 1️⃣0️⃣.0️⃣0️⃣0️⃣.0️⃣0️⃣0️⃣ единиц игровой валюты!**')
        embed.add_field(name = '🃏 `Бонус`', value = '**Один из самых умных, тактичных и отчасти везучих игроков, который проявит себя максимально хорошо, в лице участника, будет представлен к уникальной роли - <@&727112453993005118>**!')
        embed.add_field(name = '🍀 Force', value = f'**Более подробнее об этом, наш бот расскажет Вам в личных сообщениях при распределении ролей. Так же, в каждой партии, присутствует специальный человек, который проводит это мероприятие и рассказывает всем, что ему нужно делать.\n`Разработчик системы:` {ctx.author.mention}\n\nЖелаем Вам приятной игры на проекте Rodina RP | Восточный Округ ❤**', inline = False)
        embed.set_author(name = 'Discord Мероприятие', url = 'https://vk.com/norimyxxxo1702', icon_url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
        embed.set_footer(text = f'С уважением команда модерации Восточного Округа!', icon_url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
        embed.set_thumbnail(url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
        embed.set_image(url = 'https://sun4-16.userapi.com/tyMfulAo8eXkbzqmBtwuUPhT5jKSimsxh5XL2g/nckLWR6q4fc.jpg')
        msg = await ctx.send(f'╔┓┏╦━━╦┓╔┓╔━━╗ {ctx.guild.default_role}\n║┗┛║┗━╣┃║┃║╯╰║ {ctx.guild.default_role}\n║┏┓║┏━╣┗╣┗╣╰╯║ {ctx.guild.default_role}\n╚┛┗╩━━╩━╩━╩━━╝ {ctx.guild.default_role}', embed = embed)
        await msg.add_reaction('✅')
        await msg.add_reaction('❤️')
        await msg.add_reaction('❌')

def setup(bot):
    bot.add_cog(testmafia(bot))