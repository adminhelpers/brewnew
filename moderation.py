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
import jishaku
import typing
import wikipedia
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://dbrbase:YqxZgV1GL8s4CVxX@rodinadb.rhew3.mongodb.net/rodinaname?retryWrites=true&w=majority")
db = cluster["rodina"]
moder = db["moder"]
warns = db["warns"]
muted = db["mute"]
banlist = db["ban"]

dbt = cluster["RodinaBD"]
moderr = dbt["moders"]
reports = dbt["reports"]

# family.insert_one({"_id": ctx.author.id, "name": "привет"}) -> Запись в базу данных(Коллекция: Family) 
# if family.count_documents({"_id": ctx.author.id}) -> Проверка, есть значение или нет в базе данных(Коллекция: Family | Поиск по графе: _id) 
# family.find_one({"_id": ctx.author.id}) -> Получение значения из базы(Коллекция: Family | Поиск по графе: _id) 
# print(family.find_one({"_id": ctx.author.id})["name"]) -> Получение отдельного значения(Коллекция: Family | Поиск по графе: _id | Значение графы: name) 
# family.update_one({"_id": ctx.author.id}, {"$set": {"name": settle}}) -> Обновление значения в базе(Коллекция: Family | По графе: _id | Аргумент: $set - Замена | Значение графы: name | Устанавливаемое значение: settle)

def add(member: discord.Member, arg):
  if moder.count_documents({"guild": 477547500232769536, "id": member.id}) == 0:
    moder.insert_one({"guild": 477547500232769536, "id": member.id, "close": 0, "rasm": 0, "mute": 0, "kick": 0, "warn": 0, "ban": 0, "unwarn": 0, "unmute": 0, "vmute": 0, "vunmute": 0, "rols": 0, "repa": 0, "derols": 0, "dezaprols": 0, "vig": 0, "leader": 0, "x2": 0})
    moder.update_one({"guild": 477547500232769536, "id": member.id}, {"$set": {arg: 1}})
  else:
    moder.update_one({"guild": 477547500232769536, "id": member.id}, {"$set": {arg: moder.find_one({"guild": 477547500232769536, "id": member.id})[arg] + 1}})

global log
log = 736200220311945256

global message_id
message_id = 0

class moderation(commands.Cog):
    """MODERATION Cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        print('Rodina 04 | System of Moderation by dollar ム baby#3603 - Запущен')
      
    '''
        
    @commands.command()
    async def опрос(self, ctx, arg = None, *, content = None):
      global message_id

      if arg is None or content is None:
        return await ctx.send(embed = discord.Embed(description = f'Пожалуйста, укажите все аргументы функции верно!\nДля запуска опроса необходимо указать время и суть опроса!\n`Форма:` **/опрос [длительность] [суть]**\n\n`/опрос 10m Как Ваши дела?`\n-- я запущу опрос на 10 минут\n`/опрос 25 Кто за то что бы начать караоке?`\n-- я сделаю опрос который будет длиться 25 секунд\n\n• Допустимые значения: `s, m, сек, мин`', colour = 0xFB9E14), delete_after = 15)

      if arg.endswith('s') or arg.endswith('сек'):
        if arg.endswith('s'):
          time = arg.replace('s', '')
        if arg.endswith('сек'):
          time = arg.replace('сек', '')
        sleep = int(time)
        tp = f'{int(time)} секунд'

      elif arg.endswith('m') or arg.endswith('мин'):
        if arg.endswith('m'):
          time = arg.replace('m', '')
        if arg.endswith('мин'):
          time = arg.replace('мин', '')
        sleep = int(time) * 60
        tp = f'{int(time)} минут'
      
      else:
        sleep = int(time)
        tp = f'{int(time)} секунд'

      embed = discord.Embed(title = 'Опрос', description = f'**Модератор {ctx.author.mention} запустил опрос среди участников!**', colour = 0xFB9E14, timestamp = ctx.message.created_at)
      embed.add_field(name = 'Суть', value = f'{content}', inline = False)
      embed.add_field(name = 'Время голосования', value = f'{tp}', inline = False)
      embed.set_footer(text = 'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
      embed.set_thumbnail(url = ctx.guild.icon_url)
      m = await ctx.send('`Введите первый вариант ответа на эмоджи` ✅')
      def check(check):
        return check.author == ctx.author and check.channel == ctx.channel
      try:
        msg = await self.bot.wait_for('message', check = check, timeout = 60.0)
      except Exception:
        await ctx.message.delete()
        return await m.delete()
      else:
        await m.delete()
        await msg.delete()

      m2 = await ctx.send('`Введите первый вариант ответа на эмоджи` ❎')
      def check(check):
        return check.author == ctx.author and check.channel == ctx.channel
      try:
        msg2 = await self.bot.wait_for('message', check = check, timeout = 60.0)
      except Exception:
        await ctx.message.delete()
        return await m2.delete()
      else:
        await m2.delete()
        await msg2.delete()
      await ctx.message.delete()
      embed.add_field(name = 'Варианты ответа:', value = f'> ✅ `- {msg.content}`\n> ❎ `- {msg2.content}`')
      message = await ctx.send(embed = embed)
      await message.add_reaction('✅')
      await message.add_reaction('❎')
      await asyncio.sleep(sleep)
      message2 = await ctx.channel.fetch_message(message.id)
      res = [reaction for reaction in message2.reactions if reaction.emoji in ['✅', '❎']]
      result = ''
      for reaction in res:
        if reaction.emoji == '✅':
          result += "> " + str(reaction.count - 1) + " `человек выбрали вариант ответа:` **" + msg.content + "**\n"
        elif reaction.emoji == '❎':
          result += "> " + str(reaction.count - 1) + " `человек выбрали вариант ответа:` **" + msg2.content + "**\n"
        
      await message.delete()
      return await ctx.send(embed = discord.Embed(title = f'Результат опроса от {ctx.author.display_name}', description = f'**Итоги голосования:\n\nВопрос: `{content}`**\n' + str(result)))

      '''

    @commands.command()
    async def clear(self, ctx, member: typing.Optional[discord.Member] = None, amount : int = None):
        global log

        if not discord.utils.get(ctx.guild.roles, id = 652869023599558656) in ctx.author.roles and not discord.utils.get(ctx.guild.roles, id = 817813676178407425) in ctx.author.roles:
            return await ctx.send(f'`[ERR]` {ctx.author.mention}, `вам не доступна данная команда!`', delete_after = 5)

        if amount == None and member == None:
            return await ctx.send(embed = discord.Embed(description = f'''Пожалуйста, используйте команду правильно, одним из двумя способов\n\n**1) После команды укажите кол-во удаляемых сообщений.**\n`Форма:` **{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}clear `Кол-во Сообщений`**\n```{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}clear 10\n-- я удалю 10 первых сообщений.\n{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}clear 0\n-- я не удалю ни одного сообщения.```• Область допустимых значений: От `1` до `300`\n\n**2) После команды `@упомяните` участника чьи сообщения удалить, опционально укажите кол-во сообщений.**\n`Форма:` **{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}clear [Нарушитель] [Кол-во Сообщений]**\n```{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}clear @Провокатор 10\n-- я удалю 10 последних сообщений от пользователя.\n{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}clear @провокатор\n-- я не удалю ни одного сообщения от указанного пользователя.```• Область допустимых значений: От `1` до `50`''', colour = 0xFB9E14), delete_after = 60)  

        await ctx.message.delete()
        if member == None:
            if amount > 300:
                await ctx.send(embed = discord.Embed(description = f'**Область допустимых значений: 300**', colour = 0xFB9E14), delete_after = 5)
                return await ctx.message.delete()

            try:
                await ctx.channel.purge(limit = int(amount))
            except:
                amount += 1
                await ctx.channel.purge(limit = int(amount))
            await ctx.send(embed = discord.Embed(description = f'** :white_check_mark: Удаленно {amount} сообщений**', colour = 0xFB9E14), delete_after = 5)
            logs = self.bot.get_channel(log)
            e = discord.Embed(colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
            e.set_author(name = 'Удаление сообщений в канале', icon_url = ctx.author.avatar_url)
            e.add_field(name = "Удалил", value = f"{ctx.author.display_name}({ctx.author.mention})")
            e.add_field(name = "Количество", value = f"**{amount} сообщений**", inline = False)
            e.add_field(name = "Канал", value = f"<#{ctx.channel.id}>", inline = False)
            e.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
            try:
              return await logs.send(embed = e)
            except:
              pass

        if member != None and member in ctx.guild.members:
            if amount > 50:
                await ctx.send(embed = discord.Embed(description = f'**Область допустимых значений: 50**', colour = 0xFB9E14), delete_after = 5)
                return await ctx.message.delete()

            number = 0
            def predicate(message):
                return message.author == member
            async for elem in ctx.channel.history().filter(predicate):
                if not elem == None:
                    await elem.delete()
                    number += 1
                    if number >= amount:
                        await ctx.send(embed = discord.Embed(description = f'** :white_check_mark: Удаленно {amount} сообщений от пользователя {member.mention}**', colour = 0xFB9E14), delete_after = 5)   
                        break              

            logs = self.bot.get_channel(log)
            e = discord.Embed(colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
            e.set_author(name = 'Удаление сообщений пользователя', icon_url = ctx.author.avatar_url)
            e.add_field(name = "Удалили у", value = f"{member.display_name}({member.mention})")
            e.add_field(name = "Удалил", value = f"{ctx.author.display_name}({ctx.author.mention})")
            e.add_field(name = "Количество", value = f"**{amount} сообщений**", inline = False)
            e.add_field(name = "Канал", value = f"<#{ctx.channel.id}>", inline = False)
            e.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
            try:
              return await logs.send(embed = e)
            except:
              pass

    @commands.command(aliases = ['ссылка', 'инвайт'])
    async def invite(self, ctx):
        if ctx.guild.id == 325607843547840522:
            # await ctx.send(embed = discord.Embed(title = f'Discord Helper', description = f'''**Единая ссылка на приглашения пользователей --\n https://discord.gg/TmTCP9S**''', colour = 0xFB9E14))
            return
        else:
            await ctx.send(embed = discord.Embed(title = f'Discord Helper', description = f'''**Единая ссылка на приглашения пользователей --\n https://discord.gg/anPWSdB**''', colour = 0xFB9E14))

    @commands.command()
    async def vmute(self, ctx, member: discord.Member = None):
        global log

        if not discord.utils.get(ctx.guild.roles, id = 652869023599558656) in ctx.author.roles and not discord.utils.get(ctx.guild.roles, id = 817813676178407425) in ctx.author.roles:
            return await ctx.send(f'`[ERR]` {ctx.author.mention}, `вам не доступна данная команда!`', delete_after = 5)

        if member == ctx.message.author:
            return await ctx.send(embed = discord.Embed(title = f'Система наказаний', description = f'''**:shield: {ctx.author.mention}, Вы не можете выдать голосовой мут самому себе.**''', colour = 0xFB9E14), delete_after = 5)

        if member == None:
            return await ctx.send(embed = discord.Embed(title = f'Система наказаний', description = f'''**:shield: {ctx.author.mention}, укажите пользователя.**''', colour = 0xFB9E14), delete_after = 5)

        await member.edit(mute = True)
        await ctx.send(embed = discord.Embed(title = f'Система наказаний', description = f'''**:shield: {ctx.author.mention}, Вы выдали голосовой мут пользователю {member.mention}**''', colour = 0xFB9E14))
        logs = self.bot.get_channel(834039427541631016)
        e = discord.Embed(colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
        e.set_author(name = 'Выдача голосового мута', icon_url = ctx.author.avatar_url)
        e.add_field(name = "Выдали", value = f"{member.display_name}({member.mention})")
        e.add_field(name = "Выдал", value = f"{ctx.author.display_name}({ctx.author.mention})")
        e.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        await logs.send(embed = e)
        add(ctx.author, "vmute")

    @commands.command()
    async def vunmute(self, ctx, member: discord.Member = None):
        global log

        if not discord.utils.get(ctx.guild.roles, id = 652869023599558656) in ctx.author.roles and not discord.utils.get(ctx.guild.roles, id = 817813676178407425) in ctx.author.roles:
            return await ctx.send(f'`[ERR]` {ctx.author.mention}, `вам не доступна данная команда!`', delete_after = 5)

        if member == ctx.message.author:
            return await ctx.send(embed = discord.Embed(title = f'Система наказаний', description = f'''**:shield: {ctx.author.mention}, вы не можете снять голосовой мут самому себе.**''', colour = 0xFB9E14), delete_after = 5)

        if member == None:
            return await ctx.send(embed = discord.Embed(title = f'Система наказаний', description = f'''**:shield: {ctx.author.mention}, укажите пользователя.**''', colour = 0xFB9E14), delete_after = 5)

        await member.edit(mute = False)
        await ctx.send(embed = discord.Embed(title = f'Система наказаний', description = f'''**:shield: {ctx.author.mention}, Вы сняли голосовой мут пользователю {member.mention}**''', colour = 0xFB9E14))
        logs = self.bot.get_channel(834039427541631016)
        e = discord.Embed(colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
        e.set_author(name = 'Снятие голосового мута', icon_url = ctx.author.avatar_url)
        e.add_field(name = "Сняли", value = f"{member.display_name}({member.mention})")
        e.add_field(name = "Снял", value = f"{ctx.author.display_name}({ctx.author.mention})")
        e.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        await logs.send(embed = e)
        add(ctx.author, "vunmute")

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.member)
    async def ban(self, ctx, member: discord.Member = None, reason = None):
        global log

        if not ctx.guild.id == 477547500232769536:
            return

        if ctx.author.top_role.position < discord.utils.get(ctx.guild.roles, id = 789910831868543027).position:
            return await ctx.send(f'`[ERR]` {ctx.author.mention}, `вам не доступна данная команда!`', delete_after = 5)

        if member == None:
            await ctx.send(f'`[ERR]` {ctx.author.mention}, `обязательно укажите пользователя!`', delete_after = 5)
            ctx.command.reset_cooldown(ctx)
            return

        if reason == None:
            await ctx.send(f'`[ERR]` {ctx.author.mention}, `обязательно укажите причинину бана!`', delete_after = 5)
            ctx.command.reset_cooldown(ctx)
            return

        if ctx.author.top_role.position <= member.top_role.position:
            await ctx.send(f'`[ERR]` {ctx.author.mention}, `роль этого пользователя выше Вашей!`', delete_after = 5)
            ctx.command.reset_cooldown(ctx)
            return

        if ctx.author.id == 646573856785694721:
            ctx.command.reset_cooldown(ctx)

        embed = discord.Embed(colour = member.color, timestamp = ctx.message.created_at) 
        embed.set_author(name = f'Пользователь был забанен!')
        embed.add_field(name = 'Пользователь', value = f'**{member.display_name}** ({member.id})', inline = False) 
        embed.add_field(name = 'Модератор', value = f'**{ctx.author.display_name}** ({ctx.author.mention})', inline = False)    
        embed.add_field(name = 'Причина', value = f'{reason}', inline = False)  
        embed.set_thumbnail(url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        await ctx.send(embed = embed)
        channel = self.bot.get_channel(834039427541631016)
        await channel.send(embed = embed) 
        await ctx.guild.ban(member, reason = f'BANNED by {ctx.author.display_name} | REASON: {reason}')
        add(ctx.author, "ban")
        await ctx.message.add_reaction('✅')

    @commands.command(aliases = ['bt'])
    @commands.cooldown(1, 300, commands.BucketType.member)
    async def bantime(self, ctx, member: discord.Member = None, arg = None, *, reason = None):

        global log 

        if not ctx.guild.id == 477547500232769536:
            return

        if ctx.author.top_role.position < discord.utils.get(ctx.guild.roles, id = 789910831868543027).position:
            return await ctx.send(f'`[ERR]` {ctx.author.mention}, `вам не доступна данная команда!`', delete_after = 5)

        if arg == None:
            return await ctx.send(embed = discord.Embed(description = f'Пожалуйста, `@упомяните` участника для ограничения, опционально укажите срок и/или причину.\n`Форма:` **{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}bantime @упоминание [длительность] [причина]**\n\n`{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}bantime @Провокатор#1234 3h`\n-- я забаню пользователя на 3 часа\n`{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}bantime @Провокатор#1234 5d реклама`\n-- я забаню пользователя на 5 дней с указанием причины\n\n• Допустимые значения: `h, d`\n• Вместо упоминания можно использовать `ID `участника.', colour = 0xFB9E14), delete_after = 30)  

        if member == None:
            return await ctx.send(embed = discord.Embed(description = f'Пожалуйста, `@упомяните` участника для ограничения, опционально укажите срок и/или причину.\n`Форма:` **{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}bantime @упоминание [длительность] [причина]**\n\n`{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}bantime @Провокатор#1234 3h`\n-- я забаню пользователя на 3 часа\n`{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}bantime @Провокатор#1234 5d реклама`\n-- я забаню пользователя на 5 дней с указанием причины\n\n• Допустимые значения: `h, d`\n• Вместо упоминания можно использовать `ID `участника.', colour = 0xFB9E14), delete_after = 30)  

        if not member in ctx.guild.members:
          return await ctx.send(embed = discord.Embed(description = f'**Данного пользователя нет на сервере!**', color = 0xFB9E14), delete_after = 5) 

        if ctx.author.top_role.position <= member.top_role.position:
            return await ctx.send(f'`[ERR]` {ctx.author.mention}, `роль этого пользователя выше или равна Вашей!`', delete_after = 5)

        if member == ctx.author:
            return await ctx.send(embed = discord.Embed(description = f'**Вы не можете применить эту команду к себе!**', color = 0xFB9E14), delete_after = 5) 

        if reason == None:
            reason = 'не указана'

        if arg.endswith('h') or arg.endswith('час'):
            try:
              time = arg.replace('h', '')
            except:
              time = arg.replace('час', '')
            tp = f'{int(time)} часов'
            fpl = int(time) * 2

        elif arg.endswith('d') or arg.endswith('дней'):
            try:
              time = arg.replace('d', '')
            except:
              time = arg.replace('дней', '')

            tp = f'{int(time)} дней'
            fpl = int(time) * 24 * 2
        
        else:
            try:
              time = arg.replace('h', '')
            except:
              time = arg.replace('час', '')
            tp = f'{int(time)} часов'
            fpl = int(time) * 2
            
        embed = discord.Embed(colour = member.color, timestamp = ctx.message.created_at) 
        
        if ctx.author.id == 646573856785694721:
            ctx.command.reset_cooldown(ctx)
        try:
          await ctx.guild.ban(member, reason = f'BANNED by {ctx.author.display_name} | REASON: {reason} | TIME: {tp}')
          banlist.insert_one({"guild": ctx.guild.id, "type": "bands", "id": member.id, "time": fpl, "name": f'{member.name}#{member.discriminator}'})
          add(ctx.author, "ban")
          embed = discord.Embed(colour = member.color, timestamp = ctx.message.created_at) 
          embed.set_author(name = f'Пользователь был забанен!')
          embed.add_field(name = 'Пользователь', value = f'**{member.display_name}** ({member.id})', inline = False) 
          embed.add_field(name = 'Модератор', value = f'**{ctx.author.display_name}** ({ctx.author.mention})', inline = False)    
          embed.add_field(name = 'Время', value = f'{tp}', inline = False)  
          embed.add_field(name = 'Причина', value = f'{reason}', inline = False)  
          embed.set_thumbnail(url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
          embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
          await ctx.send(embed = embed)
          channel = self.bot.get_channel(834039427541631016)
          await channel.send(embed = embed) 
          embed = discord.Embed(colour = member.color, timestamp = ctx.message.created_at) 
          embed.set_author(name = f'Вы были забанены на сервере {ctx.guild.name}!')
          embed.add_field(name = 'Модератором', value = f'**{ctx.author.display_name}** `({ctx.author})`', inline = False)    
          embed.add_field(name = 'Время', value = f'{tp}', inline = False)  
          embed.add_field(name = 'Причина', value = f'{reason}', inline = False)  
          embed.set_thumbnail(url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
          embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
          try:
            await member.send(embed = embed)
          except:
            pass
        except:
          await ctx.send(embed = discord.Embed(description = f'**Произошла неизвестная ошибка.**', color = 0xFB9E14), delete_after = 5)

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.member)
    async def kick(self, ctx, member: discord.Member = None, *, reason = None):

        if not ctx.guild.id == 477547500232769536:
            return

        if not discord.utils.get(ctx.guild.roles, id = 817813676178407425) in ctx.author.roles:
            return await ctx.send(f'`[ERR]` {ctx.author.mention}, `вам не доступна данная команда!`', delete_after = 5)

        if member == None:
            await ctx.send(f'`[ERR]` {ctx.author.mention}, `обязательно укажите пользователя!`', delete_after = 5)
            ctx.command.reset_cooldown(ctx)
            return

        if reason == None:
            await ctx.send(f'`[ERR]` {ctx.author.mention}, `обязательно укажите причинину кика!`', delete_after = 5)
            ctx.command.reset_cooldown(ctx)
            return

        if ctx.author.top_role.position <= member.top_role.position:
            await ctx.send(f'`[ERR]` {ctx.author.mention}, `роль этого пользователя выше Вашей!`', delete_after = 5)
            ctx.command.reset_cooldown(ctx)
            return

        if ctx.author.id == 646573856785694721:
            ctx.command.reset_cooldown(ctx)

        embed = discord.Embed(colour = member.color, timestamp = ctx.message.created_at) 
        embed.set_author(name = f'Пользователь был кикнут!')
        embed.add_field(name = 'Пользователь', value = f'**{member.display_name}** ({member.id})', inline = False) 
        embed.add_field(name = 'Модератор', value = f'**{ctx.author.display_name}** ({ctx.author.mention})', inline = False)    
        embed.add_field(name = 'Причина', value = f'{reason}', inline = False)  
        embed.set_thumbnail(url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        await ctx.send(embed = embed)

        channel = self.bot.get_channel(834039427541631016)
        await channel.send(embed = embed)
        await ctx.guild.kick(member, reason = f'KICKED by {ctx.author.display_name} | REASON: {reason}')
        add(ctx.author, "kick")
        await ctx.message.add_reaction('✅')

    @commands.command()
    async def mute(self, ctx, member: discord.Member = None, arg = None, *, reason = None):

        global log 

        if not ctx.guild.id == 477547500232769536:
            return

        if not discord.utils.get(ctx.guild.roles, id = 652869023599558656) in ctx.author.roles and not discord.utils.get(ctx.guild.roles, id = 817813676178407425) in ctx.author.roles:
            return await ctx.send(f'`[ERR]` {ctx.author.mention}, `вам не доступна данная команда!`', delete_after = 5)

        if arg == None:
            return await ctx.send(embed = discord.Embed(description = f'Пожалуйста, `@упомяните` участника для ограничения, опционально укажите срок и/или причину.\nДля выдачи голосового мута в конце ставьте `voice` или `v`\n`Форма:` **{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}mute @упоминание [длительность] [причина]**\n\n`{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}mute @Провокатор#1234 10s`\n-- я выдам роль мута на 10 минут\n`{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}mute @Провокатор#1234 10m за провокацию`\n-- я выдам роль мута на 10 минут с указанием причины\n`{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}mute @Провокатор#1234 10m voice`\n-- я выдам голосовой мут на 10 минут\n\n• Допустимые значения: `s, m, h, d`\n• Вместо упоминания можно использовать `ID `участника.', colour = 0xFB9E14), delete_after = 30)  

        if member == None:
            return await ctx.send(embed = discord.Embed(description = f'Пожалуйста, `@упомяните` участника для ограничения, опционально укажите срок и/или причину.\nДля выдачи голосового мута в конце ставьте `voice` или `v`\n`Форма:` **{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}mute @упоминание [длительность] [причина]**\n\n`{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}mute @Провокатор#1234 10s`\n-- я выдам роль мута на 10 минут\n`{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}mute @Провокатор#1234 10m за провокацию`\n-- я выдам роль мута на 10 минут с указанием причины\n`{reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}mute @Провокатор#1234 10m voice`\n-- я выдам голосовой мут на 10 минут\n\n• Допустимые значения: `s, m, h, d`\n• Вместо упоминания можно использовать `ID `участника.', colour = 0xFB9E14), delete_after = 30)  

        if ctx.author.top_role.position <= member.top_role.position:
            return await ctx.send(f'`[ERR]` {ctx.author.mention}, `роль этого пользователя выше или равна Вашей!`', delete_after = 5)

        if ctx.author.id == member.id:
          return await ctx.send(f'`[ERR]` {ctx.author.mention}, `нельзя выдать мут самому себе!`', delete_after = 5)

        if member == ctx.author:
            return await ctx.send(embed = discord.Embed(description = f'**Вы не можете применить эту команду к себе!**', color = 0xFB9E14), delete_after = 5) 

        if reason == None or reason == 'voice':
            reason = 'не указана'

        f = 0
        if not reason == None:
          ath = re.findall(r'\w*', reason)
          if ath[-1] == 'voice' or reason.endswith('v') or ath[0] == 'voice':
            f = 1
          else:
            f = 0
        mute_role = discord.utils.get(ctx.guild.roles, id = 800085900435652678)
        sleep = 0

        if mute_role in member.roles:
          return await ctx.send(embed = discord.Embed(description = f'**Пользователь находится в муте!**', color = 0xFB9E14), delete_after = 5) 
        
        if arg.endswith('s') or arg.endswith('сек'):
            try:
              time = arg.replace('s', '')
            except:
              time = arg.replace('сек', '')
            sleep = int(time)
            tp = f'{int(time)} секунд'

        elif arg.endswith('m') or arg.endswith('мин'):
            try:
              time = arg.replace('m', '')
            except:
              time = arg.replace('мин', '')
            sleep = int(time) * 60
            tp = f'{int(time)} минут'

        elif arg.endswith('h') or arg.endswith('час'):
            try:
              time = arg.replace('h', '')
            except:
              time = arg.replace('час', '')
            sleep = int(time) * 60 * 60
            tp = f'{int(time)} часов'

        elif arg.endswith('d') or arg.endswith('дней'):
            try:
              time = arg.replace('d', '')
            except:
              time = arg.replace('дней', '')

            sleep = int(time) * 60 * 60 * 24
            tp = f'{int(time)} дней'
        
        else:
            try:
              time = arg.replace('m', '')
            except:
              time = arg.replace('мин', '')
            sleep = int(time) * 60
            tp = f'{int(time)} минут'
            
        embed = discord.Embed(colour = member.color, timestamp = ctx.message.created_at) 
        
        if f == 1:

          try:
            await member.edit(mute = True)
          except:
            return await ctx.send(f'`[ERR]` {ctx.author.mention}, `данный пользователь не находится в голосовом канале`', delete_after = 5)
        else:
          await member.add_roles(mute_role, reason = f'По причине: {reason}\nМодератором: {ctx.author.display_name}')
        if f == 1:
          embed.set_author(name = f'Пользователь получил голосовой мут!')
          add(ctx.author, "vmute")
        else:
          embed.set_author(name = f'Пользователь получил мут!')
          add(ctx.author, "mute")
        embed.add_field(name = 'Пользователь', value = f'**{member.display_name}** ({member.mention})', inline = False) 
        embed.add_field(name = 'Модератор', value = f'**{ctx.author.display_name}** ({ctx.author.mention})', inline = False)
        embed.add_field(name = 'Время', value = f'**{tp}**')    
        embed.add_field(name = 'Причина', value = f'{reason}', inline = False)  
        embed.set_thumbnail(url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        await ctx.send(embed = embed)

        logs = self.bot.get_channel(834039427541631016)
        await ctx.message.add_reaction('✅')
        await logs.send(embed = embed)
        if f == 1:
          await asyncio.sleep(sleep)
          try:
            await member.edit(mute = False)
          except:
            pass
        else:
          muted.insert_one({"guild": ctx.guild.id, "id": member.id, "time": sleep})

    @commands.command()
    async def unmute(self, ctx, member: discord.Member = None, reason = None):
        global log 

        if not ctx.guild.id == 477547500232769536:
            return

        if not discord.utils.get(ctx.guild.roles, id = 652869023599558656) in ctx.author.roles and not discord.utils.get(ctx.guild.roles, id = 817813676178407425) in ctx.author.roles:
            return await ctx.send(f'`[ERR]` {ctx.author.mention}, `вам не доступна данная команда!`', delete_after = 5)

        if member == None:
            return await ctx.send(f'`[ERR]` {ctx.author.mention}, `укажите пользователя`', delete_after = 5)
        
        if ctx.author.id == member.id:
          return await ctx.send(f'`[ERR]` {ctx.author.mention}, `нельзя снять мут самому себе!`', delete_after = 5)

        if not reason == None:

          ath = re.findall(r'\w*', reason)

          if ath[-1] == 'voice' or reason.endswith('v') or ath[0] == 'voice':
            f = 1
        else:
          f = 0
          mute_role = discord.utils.get(ctx.guild.roles, id = 800085900435652678)
        
        logs = self.bot.get_channel(834039427541631016)

        if f == 0:
          if not mute_role in member.roles:
            return await ctx.send(embed = discord.Embed(description = f'**Пользователь не находится в муте!**', color = 0xFB9E14), delete_after =5) 
        if f == 1:
          try:
            await member.edit(mute = False)
          except:
            return await ctx.message.delete()

          await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, вы сняли голосовой мут с пользователя {member.mention}**', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow()))

          add(ctx.author, "vunmute")
          return await logs.send(embed = discord.Embed(description = f'**Модератор {ctx.author.mention}, снял голосовой мут с пользователя {member.mention}**', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow()))
        
        if muted.count_documents({"id": member.id}) == 1:
          muted.delete_one({"id": member.id})
        await member.remove_roles(mute_role)
        await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, вы сняли мут с пользователя {member.mention}**', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow()))
        await logs.send(embed = discord.Embed(description = f'**Модератор {ctx.author.mention}, снял мут с пользователя {member.mention}**', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow()))
        add(ctx.author, "unmute")

    '''

    @commands.command(aliases = ['фото'])
    async def photo(self, ctx, *, arg = None):

        if not ctx.guild.id == 477547500232769536:
            return

        if not arg:
            await ctx.message.delete()
            return await ctx.send('`[ERR]: Аргумент указан не верно.`', delete_after = 5)

        photo = {
            'гу мвд':'https://i.imgur.com/hTgd52x.jpg',
            'гуур':'https://i.imgur.com/i24Yvj9.jpg',
            'шп': 'https://i.imgur.com/daQKAFp.jpg',
            'цб':'https://i.imgur.com/QuZtM8p.jpg',
            'рц-а':'https://i.imgur.com/gjl6VEn.jpg',
            'рц-л': 'https://i.imgur.com/oNDMXcS.jpg',
            'армия':'https://i.imgur.com/uXbNp3o.jpg',
            'гкб':'https://i.imgur.com/cAgG53E.jpg',
            'гму':'https://i.imgur.com/Qqw1KmK.jpg',
            'смп':'https://i.imgur.com/lmeURNv.jpg',
            'право':'https://i.imgur.com/VSl5mcD.jpg',
            'пра-во':'https://i.imgur.com/VSl5mcD.jpg',
            'фсб': 'https://avatars.mds.yandex.net/get-pdb/2073655/5f537c6a-105a-4c55-9817-0eee4cf1afbd/s1200',
            'фсин':'https://i.imgur.com/0y073Kj.jpg',
            'мрэо': 'https://i.imgur.com/xnbVTmT.jpg'}

        f

        embed = discord.Embed(description = f'**Фотография по запросу "{arg.lower()}":**', colour = ctx.author.color, timestamp = ctx.message.created_at)
        embed.set_image(url = photo[arg.lower()])
        await ctx.send(embed = embed)

    @commands.command(aliases = ['Почистить роль', 'Начать чистку'])
    async def chistka(self, ctx, role: discord.Role = None):
        if not ctx.guild.id == 477547500232769536:
            return

        a23 = [ ]

        ROLESSNYAT = {
            577532998908641280: 'ГУ',
            577532535819468811: 'ГУУР',
            748492230846578768: 'ШП',
            577531432461664266: 'Пра',
            577532176115957760: 'РЦ',
            752192117891268618: 'РЦ',
            577532332731269120: 'Армия',
            577533469429727232: 'ФСИН',
            577533194048634880: 'СМП',
            577533311556255744: 'ГКБ',
            749218773084405840: 'ГМУ',
            577541219635429401: 'ЦБ',
            577533911886987274: 'ФМ',
            577534750911365141: 'КМ',
            577534031789424650: 'СТ',
            577534186538270731: 'СБ',
            577534584124735488: 'РМ',
            577534660645617665: 'УМ',
            577534085535105055: 'ЧК',
        }

        rolepr = discord.utils.get(ctx.guild.roles, id = 673481357657243649)
        if role == None:
            message = await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, укажите роль.**', color = 0xFB9E14), delete_after = 10)
            return

        if not rolepr in ctx.author.roles:
            message = await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, дружище, тебе не доступна данная команда!**', color = 0xFB9E14), delete_after = 10)
            return

        if not role.id in ROLESSNYAT:
            message = await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, для чистки пригодны только фракционные роли.**', color = 0xFB9E14), delete_after = 10)
            return

        message = await ctx.send(embed = discord.Embed(description = f'**Производится чистка участников с ролью {role.mention}.\nСостояние: 0 %**', color = 0xFB9E14))
        vsego = len(role.members)
        oneproc = 100 / vsego
        z = 0
        s = 0
        for i in role.members:
            s += oneproc
            proc = round(s)
            if not ROLESSNYAT[role.id] in i.display_name:
                await i.remove_roles(role)
                a23.append(f'{i.display_name} | <@!{i.id}>\n')
                z += 1
                emb = discord.Embed(description = f'**Производится чистка участников с ролью {role.mention}.\nСостояние: {proc} %\nСнято ролей: {z}**')
                await message.edit(embed = emb)
            emb2 = discord.Embed(description = f'**Производится чистка участников с ролью {role.mention}.\nСостояние: {proc} %\nСнято ролей: {z}**')
            await message.edit(embed = emb2)
        await message.delete()
        str_a = ''.join(a23)
        emb2 = discord.Embed(description = f'**Чистка успешно заверщена.\nЯ снял роль {role.mention} у {len(a23)} человек.\n\nНик на сервере | Логин дискорда\n{str_a}**')
        await ctx.send(embed = emb2)

    @commands.command()
    async def rep(self, ctx,member: discord.Member = None,*,arg = None):
        if not ctx.guild.id == 477547500232769536:
            return

        channel = self.bot.get_channel(577541992599388180) #Айди канала жалоб

        if member == None:
            return await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'), delete_after = 10)

        if arg == None:
            return await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'), delete_after = 10)

        emb = discord.Embed(description =f'**:shield: {ctx.author.mention}, Вы отправили жалобу на пользователя {member.mention}.\n:bookmark_tabs: По причине: {arg}**', color=0xFB9E14)
        emb.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        emb.set_thumbnail(url = 'https://banki-kredity.ru/wp-content/uploads/2019/11/436.jpg')
        await ctx.send(embed = emb)
        embed = discord.Embed(description =f'**:shield: На пользователя {member.mention} была отправлена жалоба.\n:bookmark_tabs: По причине: {arg}\n:bust_in_silhouette: Автор жалобы: {ctx.author.mention}**', color=0xFB9E14)
        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        embed.set_thumbnail(url = 'https://banki-kredity.ru/wp-content/uploads/2019/11/436.jpg')
        await channel.send(embed = embed)

    @commands.Cog.listener()
    async def on_message(self, ctx):

      if ctx.guild == None:
        return
        
      if not ctx.guild.id == 477547500232769536:
          return

      mute_role = discord.utils.get(ctx.guild.roles, id = 800085900435652678)
      if mute_role in ctx.author.roles:
        await ctx.delete()

      mas = [577539398271500288, 703879372993462302, 577527352884723712, 673481357657243649, 577525668061904899, 577525590769532938, 577530456870748171, 577526148330815498]

      abc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Э', 'Ю', 'Я']
      
      if ctx.guild == None:
        return

      if not ctx.guild.id == 477547500232769536:
        return

      if discord.utils.get(ctx.guild.roles, id = 817813676178407425) in ctx.author.roles:
        return

      if ctx.author.bot:
        return
      
      if ctx.author.top_role.id in mas:
        return

      z = 0
      for i in list(ctx.content):
        if i in abc:
          z += 1

      try:
        prv = (z * 100)/len(ctx.content)
      except:
        return

      if len(ctx.content) <= 8:
        return

      if prv >= 50:
          s = 0
          for i in warns.find({"id": ctx.author.id}):
            s += 1
          
          if int(s) == 2:
            await ctx.delete()
            try:
              await ctx.author.send(embed = discord.Embed(description = f"**{ctx.author}, у нас запрещено использование CapsLock'a в сообщение.\nЗа нарушение данного правила Вам было выданно предупреждение!\n\nВсего предупреждений: 3(Кик с сервера)**", colour = 0xFB9E14))
            except:
              pass
            await ctx.channel.send(embed = discord.Embed(description = f"**{ctx.author}, о-оу, Вы получили предупреждение за использование Caps Lock'a**", colour = 0xFB9E14), delete_after = 15)
            await ctx.guild.kick(ctx.author, reason = f'3/6 warns | Автомодераци: Caps Lock')
            reason = f'[{ctx.created_at.strftime("%m.%d - %H:%M:%S")}]: CapsLock'
            warns.insert_one({"proverka": 0, "numbed": warns.find_one({"proverka": 1})["numbed"], "id": ctx.author.id, "kto": "Автомодерация", "reas": reason})
            warns.update_one({"proverka": 1}, {"$set": {"numbed": warns.find_one({"proverka": 1})["numbed"] + 1}})
          elif int(s) == 5:
            await ctx.delete()
            try:
              await ctx.author.send(embed = discord.Embed(description = f"**{ctx.author}, у нас запрещено использование CapsLock'a в сообщение.\nЗа нарушение данного правила Вам было выданно предупреждение!\n\nВсего предупреждений: 6(Бан на сервере)**", colour = 0xFB9E14))
            except:
              pass

            await ctx.channel.send(embed = discord.Embed(description = f"**{ctx.author}, о-оу, Вы получили предупреждение за использование Caps Lock'a**", colour = 0xFB9E14), delete_after = 15)
            await ctx.guild.ban(ctx.author, reason = f'6/6 warns | Автомодераци: Caps Lock')
            warns.delete({"id": ctx.author.id})
          else:
            reason = f'[{ctx.created_at.strftime("%m.%d - %H:%M:%S")}]: CapsLock'
            warns.insert_one({"proverka": 0, "numbed": warns.find_one({"proverka": 1})["numbed"], "id": ctx.author.id, "kto": "Автомодерация", "reas": reason})
            warns.update_one({"proverka": 1}, {"$set": {"numbed": warns.find_one({"proverka": 1})["numbed"] + 1}})
            await ctx.delete()
            await ctx.channel.send(embed = discord.Embed(description = f"**{ctx.author}, о-оу, Вы получили предупреждение за использование Caps Lock'a**", colour = 0xFB9E14), delete_after = 15)
            try:
              await ctx.author.send(embed = discord.Embed(description = f"**{ctx.author}, у нас запрещено использование CapsLock'a в сообщение.\nЗа нарушение данного правила Вам было выданно предупреждение!\n\nСписок Ваших предупреждений можно посмотреть в /warnlog**", colour = 0xFB9E14))
            except:
              pass

    '''
    @commands.Cog.listener()  
    async def on_message(self, ctx):
      if ctx.channel.id == 805487247692005417:
        czakaz = discord.utils.get(ctx.guild.categories, id= 805486831185166386)
        prov = discord.utils.get(ctx.guild.channels, name=f'заказ-{ctx.author.id}')

        if ctx.author.bot:
            if ctx.author.id == 729309765431328799:
                return
            else:
                return await ctx.delete()
        else:
            await ctx.delete()

            if prov in czakaz.channels:
                return await ctx.channel.send(f'`[ERROR]` {ctx.author.mention}, `Вы уже имеете активный заказ! Для перехода в него нажмите на его название -` <#{prov.id}>.')

            channel = await ctx.guild.create_text_channel(f'Заказ {ctx.author.mention}', overwrites=None, category=czakaz, reason='Создание нового заказа.')
            await ctx.channel.send(embed=discord.Embed(description=f'**{ctx.author.mention}, Для вас создан канал - <#{channel.id}>!**', colour=discord.Colour.blue()), delete_after = 10)
            await channel.set_permissions(ctx.author, read_messages=True, send_messages=True, read_message_history=True)
            embed1 = discord.Embed(description=f'''**Заказ создан!**''', colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
            embed1.add_field(name='Отправитель\n', value=f'**Пользователь:** `{ctx.author.display_name}`', inline=False)
            embed1.add_field(name='Суть обращения', value=f'{ctx.content}', inline=False)
            embed1.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
            await channel.send(f'{ctx.author.mention} ожидайте ответа от <@&810858517618491394>\n', embed=embed1)
            message = await self.bot.get_channel(805487247692005417).fetch_message(839774159503753236)
            emb23 = discord.Embed(description = f'```«💸 Магазин Центральный рынок 💸» - это официальный магазин Северного Округа, вы можете приобрести:```\n\n- Роль <@&805487941899649075>, позволяющая заходить во все голосовые каналы фракций и читать их текстовые каналы, а так же разрешение находиться в канале фракции без ника по форме. Так-же у вас будет чат Элитных пользователей. **[Цена: 40 семечек.]**\n\n- Ваша личная роль с вашим названием и цветом, который хотите, находящаяся над ролями фракций. Вместе с ней вам выдается роль элитного пользователя. Если элитный пользователь уже есть, на личную роль дается скидка размером: 20 семечек. **[Цена: 60 семечек.]**\n\n- Создание вашей личной семьи **[Цена :75 семечек.]**\n\n- роль <@&805493447674036234>, которая позволяет включать музыку в музыкальных каналах. **[Цена : 10 семечек.]**\n\n- роль <@&805487952620814387>, которая позволяет включать музыку во всех каналах, даже фракций. **[Цена: 15 семечек.]**\n\n`Для заказа услуг либо отправления заказа продавцам напишите любое слово в данный текстовый канал, после чего в созданном текстовом канале вы сможете задать свой заказ.`\n`Для закрытия данного канала используйте {reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]}close_buy(cb|закрыть)`', colour=discord.Colour.blue(), timestamp=datetime.datetime.utcnow())
            emb23.set_author(name='💸 Магазин Центральный рынок 💸 | Rodina RolePlay', icon_url= 'https://i.imgur.com/s5CvtOT.png')
            emb23.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
            await message.edit(embed=emb23)

    @commands.command(aliases = ['cb', 'закрыть'])
    async def close_buy(self, ctx):
      if not ctx.guild.id == 477547500232769536:
        return

      if not 'заказ' in ctx.channel.name.split('-'):
        return await ctx.message.delete()

      if discord.utils.get(ctx.guild.roles, id = 810858517618491394) in ctx.author.roles:
        messages = await ctx.channel.history(limit=1000).flatten()
        k = -1

        for i in range(len(messages) // 2):
            messages[k], messages[i] = messages[i], messages[k]
            k -= 1

        obfile = open(f'{ctx.channel.name}.txt', 'w', encoding='utf-8')
        obfile.write(f'[System]: Создание канала заказа пользователем.\n\n')
        for i in messages:
            try:
              mas = [ ]
              if len(i.content) == 0:
                  v = f'\n-----------------------\nОтправлено Embed-сообщение\nОтправитель: {i.author}\nОтправлено: {i.created_at.strftime("%m, %d - %H:%M:%S")}\nПрочитать его можно в канале "{ctx.channel.name}" до момента его удаления.\n-----------------------\n'
                  mas.append(f'{v} ')
                  st = 1
              else:
                  text = i.content.replace('`', '')
                  for v in text.split(' '):
                      if '<@&' in v:
                          v = v.replace('<@&', '').replace('>', '').replace(',', '').replace('.', '').replace(':', '').replace('?', '').replace('!', '')
                          try:   
                              rm = discord.utils.get(ctx.guild.roles, id = int(v))
                              v = f'{rm.name}(Роль)'  
                          except:
                              v = f'"Роль с ID: {v}"'
                          mas.append(f'{v} ')

                      elif '<#' in v:
                          v = v.replace('<#', '').replace('>', '').replace(',', '').replace('.', '').replace(':', '').replace('?', '').replace('!', '')
                          try:   
                              rc = self.bot.get_channel(int(v))
                              v = f'#{rc.name}(Текстовый канал)'  
                          except:
                              v = f'"Текстовый канал с ID: {v}"'
                          mas.append(f'{v} ')

                      elif '<@' in v:
                          v = v.replace('<@', '').replace('>', '').replace(',', '').replace('.', '').replace(':', '').replace('?', '').replace('!', '')
                          try:
                              mem = discord.utils.get(ctx.guild.members, id = int(v))
                              v = f'{mem.display_name}({mem})'
                          except:
                              v = f'"Пользователь с ID: {v}"'
                          mas.append(f'{v} ')
                      else:
                          mas.append(f'{v} ')

                      st = 0
              str_a = ''.join(mas)
              if st == 1:
                  obfile.write(f'{str_a}\n')
              else:
                  obfile.write(f'[{i.created_at.strftime("%m, %d - %H:%M:%S")}]{i.author.display_name}: {str_a}\n\n')
            except:
                pass
        obfile.write(f'[System]: Закрытие канала пользователем {ctx.author.display_name}({ctx.author})')
        obfile.close()

        channel2 = self.bot.get_channel(840521240279646218)
        await channel2.send(embed=discord.Embed(description=f'\n`Заказной канал` {ctx.channel.name} `был закрыт и удалён.`\n`Источник:` {ctx.author.mention}`({ctx.author})`\n\n`Сообщения сохранены в системном файле`',colour=0xFB9E14),file=discord.File(fp=f'{ctx.channel.name}.txt'))
        os.remove(f'{ctx.channel.name}.txt')
        return await ctx.channel.delete()
      else:
        return ctx.message.delete()

    @commands.command()
    async def warn(self, ctx, member: discord.Member = None, *, reason = None):
        if not ctx.guild.id == 477547500232769536:
            return

        role = discord.utils.get(ctx.guild.roles, id = 817813676178407425)

        if not role in ctx.author.roles:
            return await ctx.send(f'`[ERR]` {ctx.author.mention}, `вам не доступна данная команда!`', delete_after = 5)

        if member == None:
            return await ctx.send(f'`[ERR]` {ctx.author.mention}, `обязательно укажите пользователя!`', delete_after = 5)
            
        if member.id == ctx.author.id:
          return await ctx.send(f'`[ERR]` {ctx.author.mention}, `нельзя выдать предупреждения самому себе!`', delete_after = 5) 

        if reason == None:
            return await ctx.send(f'`[ERR]` {ctx.author.mention}, `обязательно укажите причинину выдачи предупреждения!`', delete_after = 5)


        if ctx.author.top_role.position <= member.top_role.position:
            return await ctx.send(f'`[ERR]` {ctx.author.mention}, `вы не можете выдать предупреждение пользователю, чья роль выше/равна вашей!`', delete_after = 5)

        s = 0
        for i in warns.find({"id": member.id}):
          s += 1           

        if int(s) == 2:
          await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, вы выдали пользователю {member.mention} предупреждение.\nКол-во предупреждений: 3/6 | Пользователь кикнут.**', colour = 0xFB9E14))
          await ctx.guild.kick(member, reason = f'3/6 warns | Force by {ctx.author.display_name} => Reason: {reason}')
          chan = self.bot.get_channel(834039427541631016)
          reason = f'[{ctx.message.created_at.strftime("%m, %d - %H:%M:%S")}]: {reason}'
          warns.insert_one({"proverka": 0, "numbed": warns.find_one({"proverka": 1})["numbed"], "id": member.id, "kto": ctx.author.display_name, "reas": reason})
          warns.update_one({"proverka": 1}, {"$set": {"numbed": warns.find_one({"proverka": 1})["numbed"] + 1}})
        elif int(s) == 5:
          reason = f'[{ctx.message.created_at.strftime("%m.%d - %H:%M:%S")}]: {reason}'
          await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, вы выдали пользователю {member.mention} предупреждение.\nКол-во предупреждений: 6/6 | Пользователь забанен.**', colour = 0xFB9E14))
          await ctx.guild.ban(member, reason = f'6/6 warns | Force by {ctx.author.display_name} => Reason: {reason}')
          chan = self.bot.get_channel(834039427541631016)
          warns.delete({"id": member.id})
        else:
          reason = f'[{ctx.message.created_at.strftime("%m.%d - %H:%M:%S")}]: {reason}'
          warns.insert_one({"proverka": 0, "numbed": warns.find_one({"proverka": 1})["numbed"], "id": member.id, "kto": ctx.author.display_name, "reas": reason})
          warns.update_one({"proverka": 1}, {"$set": {"numbed": warns.find_one({"proverka": 1})["numbed"] + 1}})
          await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, вы выдали пользователю {member.mention} предупреждение.\nКол-во предупреждений: {s + 1}/3**', colour = 0xFB9E14))  
          chan = self.bot.get_channel(834039427541631016)
          embed = discord.Embed(title = 'Выдача предупреждения', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
          embed.add_field(name = 'Пользователь', value = f'**{member.display_name}**', inline = False)
          embed.add_field(name = 'Модератор', value = f'**{ctx.author.display_name}({ctx.author.mention})**', inline = False)
          embed.add_field(name = 'Количество предупреждений', value = f'**{s}/3**', inline = False)
          embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
          embed.set_thumbnail(url = ctx.guild.icon_url)
          await chan.send(embed = embed)
        add(ctx.author, "warn")

    @commands.command()
    async def warnlog(self, ctx, member: discord.Member = None):
        if not ctx.guild.id == 477547500232769536:
            return

        if member == None:
            member = ctx.author
        else:
          role = discord.utils.get(ctx.guild.roles, id = 817813676178407425)
          if not role in ctx.author.roles:
              return await ctx.send(f'`[ERR]` {ctx.author.mention}, `вам не доступна данная команда!`', delete_after = 5)

        mas = [ ]
        s = 0
        for i in warns.find({"id": member.id}):
          s += 1
          mas.append(f'\n`{i["numbed"]}` | `{i["reas"]}` -> `{i["kto"]}`')

        if not s > 0:
            embed = discord.Embed(color = 0xFB9E14)
            embed.set_author(name = f'Предупреждения пользователя {member.display_name}', icon_url = member.avatar_url)
            embed.add_field(name = 'Кол-во: 0', value = '**Данный пользователь не имеет предупреждений.**')
            embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
            return await ctx.send(embed = embed)

        str_a = ''.join(mas)
        embed = discord.Embed(color = 0xFB9E14)
        embed.set_author(name = f'Предупреждения пользователя {member.display_name}', icon_url = member.avatar_url)
        embed.add_field(name = f'Кол-во: {len(mas)}', value = f'**`№ Случая` | `Причина` -> `Кто выдал`\n{str_a}**')
        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
        embed.set_thumbnail(url = ctx.guild.icon_url)
        return await ctx.send(embed = embed)

    @commands.command()
    async def unwarn(self, ctx, numbed : int = None):
        if not ctx.guild.id == 477547500232769536:
            return

        role = discord.utils.get(ctx.guild.roles, id = 817813676178407425)
        if not role in ctx.author.roles:
            return await ctx.send(f'`[ERR]` {ctx.author.mention}, `вам не доступна данная команда!`', delete_after = 5) 

        if int(numbed) > 0:
            if warns.count_documents({"numbed": numbed}) == 1:               
              memb = discord.utils.get(ctx.guild.members, id = warns.find_one({"numbed": numbed})["id"])
              if memb.id == ctx.author.id:
                return await ctx.send(f'`[ERR]` {ctx.author.mention}, `нельзя снять предупреждения самому себе!`', delete_after = 5) 

              await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, вы сняли пользователю {memb.mention} 1 предупреждение.**', colour = 0xFB9E14))
              chan = self.bot.get_channel(834039427541631016)
              await chan.send(embed = discord.Embed(description = f'**{ctx.author.mention}, снял пользователю {memb.mention} 1 предупреждение.**', colour = 0xFB9E14))
              warns.delete_one({"numbed": numbed})
              add(ctx.author, "unwarn")
            else:
                return await ctx.send(f'`[ERR]` {ctx.author.mention}, `такого случая нету!`', delete_after = 5)

        else:
            return await ctx.send(f'`[ERR]` {ctx.author.mention}, `укажите номер случая, его можно узнать прописав команду /warnlog @пользователь#1234`', delete_after = 5)

    @commands.command()
    async def unwarns(self, ctx, member: discord.Member):
        if not ctx.guild.id == 477547500232769536:
            return

        role = discord.utils.get(ctx.guild.roles, id = 817813676178407425)
        if not role in ctx.author.roles:
            return await ctx.send(f'`[ERR]` {ctx.author.mention}, `вам не доступна данная команда!`', delete_after = 5) 

        if member is None:
          return await ctx.send(f'`[ERR]` {ctx.author.mention}, `укажите пользователя!`', delete_after = 5)

        fb = 0
        for i in warns.find({"id": member.id}):
          fb += 1

        if fb != 0:                
          if member.id == ctx.author.id:
            return await ctx.send(f'`[ERR]` {ctx.author.mention}, `нельзя снять предупреждения самому себе!`', delete_after = 5) 
          
          mas = [ ]
          mr = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣']
          msr = [ ]
          preds = [ ]
          s = 0
          for i in warns.find({"id": member.id}):
            s += 1
            mas.append(f'\n{mr[0]} `{i["numbed"]}` | `{i["reas"]}` -> `{i["kto"]}`')
            msr.append(mr[0])
            mr.remove(mr[0])
            preds.append(i["numbed"])
          
          str_a = ''.join(mas)
          embed = discord.Embed(color = 0xFB9E14)
          embed.set_author(name = f'Предупреждения пользователя {member.display_name}', icon_url = member.avatar_url)
          embed.add_field(name = f'Кол-во: {len(mas)}', value = f'**`№ Случая` | `Причина` -> `Кто выдал`\n{str_a}\n\nНажмите на необходимое эмоджи для снятия определённого предупреждения!**')
          embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
          embed.set_thumbnail(url = ctx.guild.icon_url)
          message = await ctx.send(embed = embed)
          for i in msr:
            await message.add_reaction(i)
          try:
            react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in msr)
          except Exception:
            return await message.delete()
          else:
            if str(react.emoji) == msr[0]:
              warns.delete_one({"numbed": preds[0]})
              txt = f'предупреждение `№{preds[0]}`!'
            elif str(react.emoji) == msr[1]:
              warns.delete_one({"numbed": preds[1]})
              txt = f'предупреждение `№{preds[1]}`!'
            elif str(react.emoji) == msr[2]:
              warns.delete_one({"numbed": preds[2]})
              txt = f'предупреждение `№{preds[2]}`!'
            elif str(react.emoji) == msr[3]:
              warns.delete_one({"numbed": preds[3]})
              txt = f'предупреждение `№{preds[3]}`!'
            elif str(react.emoji) == msr[4]:
              warns.delete_one({"numbed": preds[4]})
              txt = f'предупреждение `№{preds[4]}`!'
          
          await message.delete()
          await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, Вы сняли пользователю {member.mention} {txt}**', colour = 0xFB9E14))
          chan = self.bot.get_channel(834039427541631016)
          await chan.send(embed = discord.Embed(description = f'**{ctx.author.mention}, снял пользователю {member.mention} 1 {txt}**', colour = 0xFB9E14))
          add(ctx.author, "unwarn")
        else:
          return await ctx.send(f'`[ERR]` {ctx.author.mention}, `пользователь не имеет предупреждений!`', delete_after = 5)


    '''
    j = {
      Правила:
      1.1. Незнание правил не освобождает от ответственности.
      1.2. Правила в любой момент могут быть изменены или дополнены.
      1.3. В некоторых категориях/каналах некоторые правила могут не действовать.
      1.4. Изменения в правилах вступают в силу сразу же после редактирования.  

      Относитесь ко всем с уважением. На сервере категорически запрещены домогательства, преследования, сексизм, расизм и другого рода воссоздание/розжиг конфликтных ситуаций..

      Запрещается рассылать спам или заниматься самопродвижением (приглашения на сервер, реклама и т. д.) без разрешения одного из администраторов. Данное правило также распространяется на личные сообщения участникам сервера.

      Запрещается публиковать откровенный и непристойный контент. Данное правило распространяется на тексты, изображения или ссылки, содержащие или описывающие сцены секса, наготу, сцены насилия или другой шокирующий контент.

      Абсолютно каждый пользователь, начиная общаться в данном канале подписывается под условиями тем, что прочитал все пункты в канале #『📌』правила и обязуется их выполнять.


      Смайлики:
      『📢』    『📊』    『🎤』
      『📌』    『❗』     『💥』
      『🔲』    『💰』    『📀』
      『🔒』    『📑』    『 💡 』
      『📃』    『✨』    『💸』
      『🌌』    『🔳』    『🚶』
      『📺』    『🎬』    『👑』
      『📩』    『🎭』    『💬 』
      『❓』     『🌠』    『 ➊ 』
      『🎧』    『🔔』    『⛔』
      『⏳』    『🔋』     『📍』
      『 🚩』  『 🔓 』    


      Информационные: 
      『📢』    『📌』    『🔲』
      『🔒』    『📃』    『📖』
      『🌌』    『📺』    『📩』
      『❓』     『📑』    『📊』


      Мероприятия:  
      『🎭』    『🎨』    『🌠』
      『💥』    『📀』    『✨』

      
      Реквестовые:  『📩』    『🔲』    『 💡 』  『💰』

      Музыкальные:  『🎧』    『🎬』    『🎤』    『🔳』

      Обзвоны: 
      Текстовые:  『📌』
      Голосовые:  『🔔』    『⛔』    『🔋』    『⏳』  


      РП: 『📍』    『 🚩』   『📢』


      Лидеры: 
      Текстовые:  『📌』
      Голосовые:  『 🔓 』
      


      Гос-организации: 
      Текстовые: 『📃』
      Голосовые:
      Пра-во -『📈』
      ФСБ -   『🚓』    『🚨 』   『🚓』
      МВД -   『🚔』    『🚨』
      Радиоцентр - 『🎥』   『📻』
      МО - 『💂🏻』   『🔫』
      ТСР - 『🚌』
      МЗ - 『🚑』   『💉』
      ЦБ - 『💲 』   『💸』
      ЦЛ - 『📋 』


      Мафии: 『🗡』   『💀』    『🔪』
      ОПГ:   『😈』   『🕵』    『🕴』    『🧛』

      Репорт: 『🔳』  


      Модераторы:  
      Текстовые:   『💬』
      Голосовые:   『🌟』   『🎴』    『📣』    『🤡』    
      

      Тет-А-Тет:  『👥』


      Администрация: 
      『🔔』   『💎』    『🔞』
      『💰 』  『💾』    『📢』


      Хелперы: 『🧣』   『 🌹 』    『🧤』

      АФК: 『🌙』



      ...| Основной |...
      #『📩』запрос-роли   
      #『💬』общение       
      #『🪁』проверка-уровня
      #『💰』казино        
      #『🎤』медиа

      ...| Помощь и Информация |...
      #『📋』новости-сервера
      #『📢』новости-discord
      #『 🚩』information
      #『📌』правила
      #『📍』support

        ...| Общение игроков |...
      『👥』Тет-А-Тет с Главным Администратором
      『🔒』Конференция с Главным администратором
      『 🌹 』Стримы :3
      『 🔈』Общение [ I ]
      『 🔈』Общение [ II ]
      『🎭』Друзья с ЖВД

      ...| Приват общение |...
      『 📞』Создать приват

      ...| Магазин "Центральный рынок" |...
      #『 💡 』логи-заказов
      #『💸』заказ-услуг

      Турнир RDS
      #『✨』брифинг
      #『🚗』заезды
      #『🌌』чат
      #『📊』судейство
      #『 📝』регистрация
      #『🔲』результаты
      『📀』Брифинг
      『📃』Квалификация
      『👥』Парные
      『🧣』Тренировка

        ...| Обзвон |...
      『🔔』Кандидаты
      『⛔』Обзвон ГОС
      『⛔』Обзвон НЕЛ
      『⏳』Ожидание итогов ГОС
      『⏳』Ожидание итогов НЕЛ

      Обзвон на пост Администратора
      『🧾』Кандидаты
      『⛔』Обзвон Админ
      『⏳』Ожидание итогов

      ...| Мафия |...
      #『🔮』чат-игроков-мафии
      #『🔮』чат-мафии
      #『🔮』правила-игры-мафия
      『🕵』Мафия

      ...| Караоке |...
      #『🎤』караоке
      #『📃』правила-караоке
      #『🌟』заявка-на-караоке
      『 🔋 』караоке

      ...| элитка |...
      #『👑』элитка
      『💎』Канал элитных пользователей

      ...| Family |...
      #『🔳』family-chat
      Rivera_Squad
      ム dollar 💸 voice ム

      ...| Музыка |...
      #『🎵』v-i-p-music
      #『🎵』music
      『🎧』Музыкальный канал #1
      『🎧』Музыкальный канал #2

      ...| Государственные Структуры |...
      #『 🔓 』собрание-чат
      『 🚩』Глобальная RP.
      『 🚩』Собрание.

      ...| Криминальные Группировки |...
      #『📛』общение
      『📛』Глобальная RP.
      『 🔓 』Переговоры/Обсуждение.
      『 🚩』Собрание.

      ...| Правительство Округа |...
      #『📈』система-повышения
      #『📈』отчёты-на-повышение
      #『📈』общение
      #『📈』антиблат-правительство
      『🎓』Приёмная
      『🎓』Правительство [Общий]
      『🎓』Кабинет Вице - Губернатора
      『🎓』Кабинет Губернатора

      Прокуратура г. Лыткарино
      #『🚨』система-повышения
      #『🚨』отчёты-на-повышение
      #『🚨』общение
      #『🚨』антиблат-прокуратуры
      『 ⌛ 』Приемная
      『 ⌛ 』Прокуратура г. Лыткарино[Общий]
      『 ⌛ 』Кабинет Судей
      『 ⌛ 』Кабинет Зам. Ген. Прокурора
      『 ⌛ 』Кабинет Ген. Прокурора

      ...| Центральный Банк |...
      #『📃』система-повышения
      #『📃』отчёты-на-повышение
      #『📃』общение
      #『📃』антиблат-банка
      『 💲 』Приёмная
      『 💲 』Центральный Банк [Общий]
      『💳』Кабинет Заместителя Директора Банка
      『💳』Кабинет Директора Банка

      ...| ФСБ |...
      #『📃』система-повышения
      #『📃』отчёт-на-повышение
      #『📃』дела-усб
      #『📃』общение
      #『📃』антиблат-фсб
      『🚨』Приёмная
      『🚔』ФСБ [Общий]
      『🚔』Патруль №1
      『🚓』Патруль №2
      『 🔓 』Кабинет Полковника ФСБ
      『 🔓 』Кабинет Директора ФСБ

      ...| ГУВД |...
      #『📃』система-повышения
      #『📃』отчёты-на-повышение
      #『📃』общение
      #『📃』антиблат-гувд
      『🕵』Приёмная
      『🕵』ГУВД [Общий]
      『🚔』Патруль №1
      『🚔』Патруль №2
      『 🔓 』Кабинет Полковника ГУВД
      『 🔓 』Кабинет Генерала ГУВД

      ...| ГИБДД |...
      #『📃』система-повышения
      #『📃』отчёты-на-повышение
      #『📃』общение
      #『📃』антиблат-гибдд
      『🕵』Приёмная
      『🕵』ГИБДД [Общий]
      『🚔』Патруль №1
      『🚔』Патруль №2
      『 🔓 』Кабинет Полковника ГИБДД
      『 🔓 』Кабинет Генерала ГИБДД

      ...| Министерство Обороны |...
      #『📃』система-повышения
      #『📃』отчёты-на-повышение
      #『📃』общение
      #『📃』антиблат-армия
      『💂🏻』Приёмная
      『💂🏻』Армия [Общий]
      『🔫』Доставка БП
      『 🔓 』Кабинет Полковника Армии
      『 🔓 』Кабинет Генерала Армии

      ...| Тюрьма Строгого Режима |...
      #『📃』система-повышения
      #『📃』отчёт-на-повышение
      #『📃』общение
      #『📃』антиблат-тср
      『🚌』Приёмная
      『🚬』ТСР [Общий]
      『 🔓 』Кабинет Заместителя Начальника ТСР
      『 🔓 』Кабинет Начальника ТСР

      ...| Новостное Агенство  г.Арзамаса |...
      #『📃』система-повышения
      #『📃』отчёты-на-повышение
      #『📃』общение
      #『📃』антиблат-сми-а
      『🎥』Приёмная
      『🧭』Н.А.-г.Арзамас[Общий]
      『 🔓 』Кабинет Заместителя Директора Н.А. г.Арзамас
      『 🔓 』Кабинет Директора Н.А. г.Арзамас

      ...| Новостное Агенство г.Лыткарино |...
      #『📃』система-повышения
      #『📃』отчёты-на-повышение
      #『📃』общение
      #『📃』антиблат-сми-л
      『🎥』Приёмная
      『🛰』Н.А.-г.Лыткарино[Общий]
      『 🔓 』Кабинет Заместителя Директора СМИ
      『 🔓 』Кабинет Директора СМИ

      ...| Больница г. Арзамаса |...
      #『📃』система-повышения
      #『📃』антиблат-мз-а 
      #『📃』общение
      #『📃』отчёты-на-повышение
      『🚑』Приёмная
      『💉』Больница г. Арзамас [Общий]
      『 🔓 』Кабинет Зам. Глав. Врача
      『 🔓 』Кабинет Глав. Врача

      ...| Поликлиника г.Эдово |...
      #『📃』система-повышения
      #『📃』отчёты-на-повышение
      #『📃』общение
      #『📃』антиблат-мз-э
      『🚑』Приёмная
      『💉』Поликлиника г.Эдово [Общий]     
      『 🔓 』Кабинет Зам. Глав. Врача
      『 🔓 』Кабинет Глав. Врача

      ...| Поликлиника г.Лыткарино |...
      #『📃』система-повышения
      #『📃』отчёты-на-повышение
      #『📃』общение
      #『📃』антиблат-мз-л
      『🚑』Приёмная
      『💉』Поликлиника г.Лыткарино [Общий]
      『 🔓 』Кабинет Зам. Глав. Врача
      『 🔓 』Кабинет Глав. Врача

      ...| Мафии |...
      『🗡』Украинская Мафия     
      『🔪』Русская Мафия
      『💀』Кавказкая Мафия


      ...| ОПГ |...
      『😈』Фантомасы
      『🕵』Санитары
      『🕴』Чёрные Кошки
      『🧛』Солнцевская Братва

      ...| REPORT |...
      #『 ❕』логи-репорта

      ...| Раздел модераторов |...
      #『💬』модераторская
      #『💬』снятие-роли
      #『💬』requests-for-roles
      #『💬』test-channel
      #『💬』выдача-наказаний
      #『💬』модерские-логи
      『🎴』Ожидание обзвона
      『👹』Обзвон на пост модератора
      『🌍』Модераторская
      『🌍』Собрание модераторов
      『🤡』Казнь модераторов
      
      ...| Хелпера |...
      『 🛡』Ожидание аттестации
      『🧣』Аттестация [2]
      『💎』Постановление хелперов
      『💎』Собрание


      ...| Администрация |...
      #『💬』admins-chat
      『🧤』Общение Администрации.
      『🔔』Собрание Администрации.
      『👥』Приват [1]
      『👥』Приват [2]
      『👥』Приват [3]
      『🔞』Старшая Администрация.
      『💰 』Казнь
      『💾』Гл. Администрация


      Логирование
      #『💤』голосовой-log
      #『💤』каналы-log
      #『💤』изменение-ролей-log
      #『💤』сообщения-log
      #『💤』добавление-ролей-log

      ...| Прочее |...
      『🌙』АФК

      ...| Заказ |...

      ...| КОРЗИНА |...

      На рассмотрении
    }

    '''

    @commands.command(aliases = ['imd', 'модеринфо'])
    async def mstat(self, ctx, member: discord.Member = None):
        if not ctx.guild.id == 477547500232769536:
            return

        if member == None:
          member = ctx.author
          
        
        if not discord.utils.get(ctx.guild.roles, id = 652869023599558656) in member.roles and not discord.utils.get(ctx.guild.roles, id = 817813676178407425) in member.roles:
            return await ctx.send(f'`[ERR]` {ctx.author.mention}, `вам не доступна данная команда!`', delete_after = 5) 

        if not discord.utils.get(ctx.guild.roles, id = 652869023599558656) in member.roles and not discord.utils.get(ctx.guild.roles, id = 817813676178407425) in member.roles:
          return await ctx.send(f'`[ERR]` {ctx.author.mention}, `данный пользователь не является агентом поддержки!`', delete_after = 5)
        
        if moderr.count_documents({"id": member.id}) == 0 and moder.count_documents({"guild": 477547500232769536, "id": member.id}) == 0:
          return await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, данный пользователь не является модератором, либо он не сделал никаких действий.**', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow()), delete_after = 5)
        
        i, b = [], []
        ms = ['close', 'rasm', 'mute', 'kick', 'ban', 'warn', 'unwarn', 'unmute', 'vmute', 'vunmute', 'rols', 'repa', 'derols', 'dezaprols', 'vig']
        for v in ms:
          try:
            i.append(moder.find_one({"guild": ctx.guild.id, "id": member.id})[v])
          except:
            i.append(0)

        ms2 = ['close', 'rasm', 'repa', 'addme', 'addrep']
        for v in ms2:
          try:
            b.append(moderr.find_one({"guild": ctx.guild.id, "id": member.id})[v])
          except:
            b.append(0)
  
        foc = int(i[0]) + int(i[1]) + int(i[2]) + int(i[3]) + int(i[4]) + int(i[5]) + int(i[6]) + int(i[7]) + int(i[8]) + int(i[9]) + int(i[10]) + int(i[12]) + int(i[13]) + int(b[0]) + int(b[1]) + int(b[3]) + int(b[4]) 
        embed = discord.Embed(title = f'Статистика модератора 📍 {member}', description = f'**👁️ Всего действий от него: {foc}**', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
        embed.add_field(name = '❔ | `Статистика вопросов`', value = f'**Всего действий:** {int(b[0]) + int(b[1]) + int(b[3]) + int(b[4])}\n> 🔹 `Принято вопросов:` {b[3]}\n> 🔹 `Закрыто вопросов:` {b[0]}\n> 🔹 `Поставлено на рассмотрение:` {b[1]}\n> 🔹 `Добавлено людей к репортам:` {b[4]}\n\n> ➕ `Репутация:` {b[2]}', inline = False)
        embed.add_field(name = '🔰 | `Статистика модерирования`', value = f'**Всего действий: {foc - int(b[0]) - int(b[1]) - int(b[3]) - int(b[4])}\n> ✏️ | `Выдано текстовых мутов:` {i[2]}\n> 🔊 | `Выдано голосовых мутов:` {i[8]}\n> ✏️ | `Снято текстовых мутов:` {i[7]}\n> 🔊 | `Снято голосовых мутов:` {i[9]}\n\n> `Выдано предупреждений:` {i[5]}\n> `Снято предупреждений:` {i[6]}\n> `Кикнул:` {i[3]}\n> `Забанил:` {i[4]}\n\n> `Одобрено запросов на выдачу роли:` {i[10]}\n> `Отправлено запросов на снятие роли:` {i[13]}\n> `Одобрено запросов на снятие роли:` {i[12]}\n\n> ❗ `Выговоров:` {i[14]} ❗**', inline = False)
        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
        await ctx.send(embed = embed)

    '''
    @commands.command(aliases = ['imoders'])
    @commands.has_permissions(administrator = True)
    async def allmstats(self, ctx):
        if not ctx.guild.id == 477547500232769536:
            return  

        fcff = {
          0: "Первая",
          1: "Вторая",
          2: "Третья",
          3: "Четвёртая"
        } 
        
        embed = discord.Embed(title = f'Статистика модераторов сервера 📍 {ctx.guild.name}', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
        moders = []
        asb = 0
        fsc = -1
        role = discord.utils.get(ctx.guild.roles, id = 817813676178407425)
        for z in moder.find({"guild": ctx.guild.id}):
          member = discord.utils.get(ctx.guild.members, id = z["id"])
          if role in member.roles:
            i = []
            ms = ['close', 'rasm', 'mute', 'kick', 'ban', 'warn', 'unwarn', 'unmute', 'vmute', 'vunmute', 'rols', 'repa', 'derols', 'dezaprols', 'vig']
            for b in ms:
              i.append(moder.find_one({"id": member.id})[b])
          
  
            foc = int(i[0]) + int(i[1]) + int(i[2]) + int(i[3]) + int(i[4]) + int(i[5]) + int(i[6]) + int(i[7]) + int(i[8]) + int(i[9]) + int(i[10]) + int(i[12]) + int(i[13])
            moders.append(f'`Модератор:` **{member.display_name}** | `Действий:` {foc} | `Репутация:` {i[11]}\n')
            asb += 1
            if asb == 10:
              fsc += 1
              str_a = ''.join(moders)
              embed.add_field(name = f'🔰 | {fcff[fsc]} линия', value = str_a)
              asb = 0
        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
        await ctx.send(embed = embed)

    @commands.command(aliases = ['addmoderpanel'])
    async def __addmoderpanel(self, ctx, member: discord.Member = None, arg : int = None):
      if not ctx.guild.id == 477547500232769536:
          return

      await ctx.message.delete()

      if member is None:
        return await ctx.send('`Укажите пользователя.`', delete_after = 2)

      if not ctx.author.id == 646573856785694721:
        return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, данная команда не доступна для вас.', colour = 0xFB9E14), delete_after = 5)

      if not discord.utils.get(ctx.guild.roles, id = 817813676178407425) in member.roles:
        return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, данный пользователь не является модератором.', colour = 0xFB9E14), delete_after = 5)

      if arg == 1:
        if moder.find_one({"id": member.id})["leader"] == 1:
          return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, данный пользователь уже имеет доступ к панели управления модераторами.', colour = 0xFB9E14), delete_after = 5)
        message = await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, вы действительно хотите выдать доступ к панели управления модераторами пользователю {member.mention}?\n\n> ❤ `- Да`\n> 💔 `- Нет`', colour = 0xFB9E14), delete_after = 5)
        await message.add_reaction('❤')
        await message.add_reaction('💔')
        try:
          react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in ['💔', '❤'])
        except Exception:
          return await message.delete()
        else:
          await message.delete()
          if str(react.emoji) == '💔':
            return
          elif str(react.emoji) == '❤':
            if moder.count_documents({"id": member.id}) == 0:
              moder.insert_one({"id": member.id, "close": 0, "rasm": 0, "mute": 0, "kick": 0, "warn": 0, "ban": 0, "unwarn": 0, "unmute": 0, "vmute": 0, "vunmute": 0, "rols": 0, "repa": 0, "derols": 0, "dezaprols": 0, "vig": 0, "leader": 1})
            else:
              moder.update_one({"id": member.id}, {"$set": {"leader": 1}})
            return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, вы успешно выдали доступ к панели управления модераторами пользователю {member.mention}', colour = 0xFB9E14), delete_after = 5)
      elif arg == 0:
          if moder.find_one({"id": member.id})["leader"] == 0:
            return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, данный пользователь не имеет доступа к панели управления модераторами.', colour = 0xFB9E14), delete_after = 5)
          if moder.count_documents({"id": member.id}) == 0:
            moder.insert_one({"id": member.id, "close": 0, "rasm": 0, "mute": 0, "kick": 0, "warn": 0, "ban": 0, "unwarn": 0, "unmute": 0, "vmute": 0, "vunmute": 0, "rols": 0, "repa": 0, "derols": 0, "dezaprols": 0, "vig": 0, "leader": 0})
          else:
            moder.update_one({"id": member.id}, {"$set": {"leader": 0}})
          return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, вы успешно ограничили доступ к панели управления модераторами пользователю {member.mention}', colour = 0xFB9E14), delete_after = 5)

    @commands.command(aliases = ['mwarn'])
    async def warnmoder(self, ctx, member: discord.Member = None, *, reason = None):
      if not ctx.guild.id == 477547500232769536:
          return

      await ctx.message.delete()

      if member is None:
        return await ctx.send('`Укажите пользователя.`', delete_after = 2)

      if reason == None:
        reason = 'Не указана'

      if not moder.find_one({"id": ctx.author.id})["leader"] == 1 or moder.count_documents({"id": ctx.author.id}) == 0:
        return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, данная команда не доступна для вас.', colour = 0xFB9E14), delete_after = 5)

      if not discord.utils.get(ctx.guild.roles, id = 817813676178407425) in member.roles:
        return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, данный пользователь не является модератором.', colour = 0xFB9E14), delete_after = 5)

      if moder.count_documents({"id": member.id}) == 0:
        moder.insert_one({"id": member.id, "close": 0, "rasm": 0, "mute": 0, "kick": 0, "warn": 0, "ban": 0, "unwarn": 0, "unmute": 0, "vmute": 0, "vunmute": 0, "rols": 0, "repa": 0, "derols": 0, "dezaprols": 0, "vig": 0, "leader": 0})

      if moder.find_one({"id": member.id})["leader"] == 1:
          if not ctx.author.id == 646573856785694721:
            return await ctx.send('`Не-не, так дела не делаются.`', delete_after = 4)

      bal = moder.find_one({"id": member.id})["vig"] + 1
      if bal == 3:
        moder.delete_one({"id": member.id})
        return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, Вы выдали выговор модератору {member.mention}. Причина: {reason}\nСтатистика модератора была обнулена из-за трёх выговор.', colour = 0xFB9E14))
      else:
        moder.update_one({"id": member.id}, {"$set": {"vig": bal}})
        return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention} выдал выговор модератору {member.mention}. Причина: {reason}.\nСумма его выговоров: `{bal}/3`', colour = 0xFB9E14))
 
    @commands.command(aliases = ['munwarn'])
    async def unwarnmoder(self, ctx, member: discord.Member = None, *, reason = None):
      if not ctx.guild.id == 477547500232769536:
          return

      if member is None:
        return await ctx.send('`Укажите пользователя.`', delete_after = 2)

      if not moder.find_one({"id": ctx.author.id})["leader"] == 1 or moder.count_documents({"id": ctx.author.id}) == 0:
        return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, данная команда не доступна для вас.', colour = 0xFB9E14), delete_after = 5)

      if not discord.utils.get(ctx.guild.roles, id = 817813676178407425) in member.roles:
        return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, данный пользователь не является модератором.', colour = 0xFB9E14), delete_after = 5)

      if moder.count_documents({"id": member.id}) == 0 or moder.find_one({"id": member.id})["vig"] == 0:
         moder.insert_one({"id": member.id, "close": 0, "rasm": 0, "mute": 0, "kick": 0, "warn": 0, "ban": 0, "unwarn": 0, "unmute": 0, "vmute": 0, "vunmute": 0, "rols": 0, "repa": 0, "derols": 0, "dezaprols": 0, "vig": 0, "leader": 0})
         return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention} данный модератор не имеет выговоров.', colour = 0xFB9E14))

      bal = moder.find_one({"id": member.id})["vig"] - 1
      moder.update_one({"id": member.id}, {"$set": {"vig": bal}})
      return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention} снял выговор модератору {member.mention}.\nСумма его выговоров: `{bal}/3`', colour = 0xFB9E14))

    @commands.command(aliases = ['setbonus'])
    async def __setbonus(self, ctx, member: discord.Member = None, arg : int = None):
      if not ctx.guild.id == 477547500232769536:
          return

      await ctx.message.delete()

      if member is None:
        return await ctx.send('`Укажите пользователя.`', delete_after = 2)
      
      if arg == None or not arg in [1, 0]:
        return await ctx.send('`Укажите аргумент!`', embed = discord.Embed(description = f'**1 - `Установить бонус "x2 статистика"`\n2 - `Аннулировать бонус`**'), delete_after = 2)

      if moder.count_documents({"id": ctx.author.id}) == 0 or moder.find_one({"id": ctx.author.id})["leader"] == 0:
        return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, данная команда не доступна для вас.', colour = 0xFB9E14), delete_after = 5)

      if not discord.utils.get(ctx.guild.roles, id = 817813676178407425) in member.roles:
        return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, данный пользователь не является модератором.', colour = 0xFB9E14), delete_after = 5)

      if arg == 1:
        if moder.find_one({"id": member.id})["x2"] == 1:
          return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, у данного модератора уже установлен бонус.', colour = 0xFB9E14), delete_after = 5)

        message = await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, вы действительно хотите установить бонус "x2 статистика" иодератору {member.mention}?\n\n> ❤ `- Да`\n> 💔 `- Нет`', colour = 0xFB9E14), delete_after = 5)
        await message.add_reaction('❤')
        await message.add_reaction('💔')
        try:
          react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in ['💔', '❤'])
        except Exception:
          return await message.delete()
        else:
          await message.delete()
          if str(react.emoji) == '💔':
            return
          elif str(react.emoji) == '❤':
            if moder.count_documents({"id": member.id}) == 0:
              moder.insert_one({"id": member.id, "close": 0, "rasm": 0, "mute": 0, "kick": 0, "warn": 0, "ban": 0, "unwarn": 0, "unmute": 0, "vmute": 0, "vunmute": 0, "rols": 0, "repa": 0, "derols": 0, "dezaprols": 0, "vig": 0, "leader": 0, "x2": 1})
            else:
              moder.update_one({"id": member.id}, {"$set": {"x2": 1}})
            return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, вы успешно установили бонус "x2 статистика" модератору {member.mention}', colour = 0xFB9E14), delete_after = 5)
      elif arg == 0:
          if moder.find_one({"id": member.id})["x2"] == 0:
            return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, данный модератор не имеет бонуса.', colour = 0xFB9E14), delete_after = 5)
          if moder.count_documents({"id": member.id}) == 0:
            moder.insert_one({"id": member.id, "close": 0, "rasm": 0, "mute": 0, "kick": 0, "warn": 0, "ban": 0, "unwarn": 0, "unmute": 0, "vmute": 0, "vunmute": 0, "rols": 0, "repa": 0, "derols": 0, "dezaprols": 0, "vig": 0, "leader": 0, "x2": 0})
          else:
            moder.update_one({"id": member.id}, {"$set": {"x2": 0}})
          return await ctx.send(embed = discord.Embed(description = f'{ctx.author.mention}, вы успешно аннулировали бонус "x2 статистика" модератору {member.mention}', colour = 0xFB9E14), delete_after = 5)
    '''

def setup(bot):
    bot.add_cog(moderation(bot))