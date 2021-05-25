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
import wikipedia
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://rodinadb:nbsGK02riO3PkygA@cluster0.cdvgc.mongodb.net/rodina?retryWrites=true&w=majority")
db = cluster["rodina"]
coins = db["coins"]
users = db["users"]

# family.insert_one({"_id": ctx.author.id, "name": "привет"}) -> Запись в базу данных(Коллекция: 
# if family.count_documents({"_id": ctx.author.id}) -> Проверка, есть значение или нет в базе данных(Коллекция: Family | Поиск по графе: _iFamily) d) 
# family.find_one({"_id": ctx.author.id}) -> Получение значения из базы(Коллекция: Family | Поиск по графе: _id) 
# print(family.find_one({"_id": ctx.author.id})["name"]) -> Получение отдельного значения(Коллекция: Family | Поиск по графе: _id | Значение графы: name) 
# family.update_one({"_id": ctx.author.id}, {"$set": {"name": settle}}) -> Обновление значения в базе(Коллекция: Family | По графе: _id | Аргумент: $set - Замена | Значение графы: name | Устанавливаемое значение: settle)

global tens
tens = [ ]

def addbt(member: discord.Member, arg : int):
  if coins.count_documents({"id": member.id}) == 0:
    coins.insert_one({"guild": member.guild.id, "id": member.id, "coins": arg})
    return arg
  else:
    bal = arg + coins.find_one({"id": member.id})["coins"]
    coins.update_one({"id": member.id}, {"$set": {"coins": bal}})
    return bal

def rebt(member: discord.Member, arg : int):
  bal = coins.find_one({"id": member.id})["coins"] - arg
  coins.update_one({"id": member.id}, {"$set": {"coins": bal}})
  return bal

def proverka(member, stv : int):
  if coins.count_documents({"id": member.id}) == 0:
    return 0

  else:
    if coins.find_one({"id": member.id})["coins"] < stv:
      return 0
    else:
      return 1

def proc(args):
  s = 0
  if args >= 10 and args <= 30:
    s = 1
  elif args > 30 and args <= 50: 
    s = 2
  elif args > 50 and args <= 70: 
    s = 3
  elif args > 70 and args <= 90: 
    s = 4
  elif args > 90 and args <= 150: 
    s = 5
  elif args > 150: 
    s = 10

  return s


class econom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prev = []

    @commands.command()
    async def topcoins(self, ctx):
      coins = db["coins"]
      zb = 0

      m = [ ]
      m2 = [ ]
      m3 = [ ]
      c = [ ]
      c2 = [ ]
      cz = [ ]
      cz2 = [ ]
      fr = 0
      zb = 50
      for i in coins.find({"guild": ctx.guild.id}):
        mname = discord.utils.get(ctx.guild.members, id = i["id"])
        if mname == None:
          continue
        m.append(i["coins"])
        cz.append(mname.name)

        coins = i["coins"]

        c.append(f'**Семечек:** `{coins}`')
        fr += 1
        if fr >= 50:
          break
      
      m2 = m
      m3 = m
      c2 = c
      cz2 = cz
      t = sorted(m)[::-1]

      frf = 0
      frfz = 0
      stra = 1
      zbs = zb//10
      if zbs == 0:
        zbs = 1
      embed = discord.Embed(title = f'Таблица лидеров', description = None, colour = 0x09F2C8)
      for v in t:
        frfz += 1
        frf += 1
        f = m2.index(v)
        if frf == 1:
          frs = f'🥇 1. {cz[f]}'
        elif frf == 2:
          frs = f'🥈 2. {cz[f]}'
        elif frf == 3:
          frs = f'🥉 3. {cz[f]}'
        else:
          frs = f'{frf}. {cz[f]}'
        embed.add_field(name = frs, value = c[f], inline = False)
        c.remove(c[f])
        cz.remove(cz[f])
        m2.remove(m2[f])
        if frfz == 10:
          frfz = 0
          break     

      mes = await ctx.send(embed = embed)
		
    @commands.command()
    async def coins(self, ctx, member: discord.Member = None):
      if not ctx.guild.id == 477547500232769536:
            return

      if member == None:
        member = ctx.author

      if coins.count_documents({"id": member.id}) == 0:
        return await ctx.send(embed = discord.Embed(title = 'Северный Округ | Семечки', description = f'Никнейм: {member.mention}\nСемечки: `0`', colour = 0x09F2C8))

      else:
        return await ctx.send(embed = discord.Embed(title = 'Северный Округ | Семечки', description = f'Никнейм: {member.mention}\nСемечки: `{coins.find_one({"id": member.id})["coins"]}`', colour = 0x09F2C8))

    @commands.command()
    @commands.has_any_role(661284961428701209, id, id, '★ Продавец ★', id, id, id, '★ Technical Administrator Discord ★', id, id, id, '☆ Developer Discord ☆', id, id, id, '☆ Глав. Модерация Discord ☆')
    async def addcoins(self, ctx, member: discord.Member = None, amount:int = None):
      if not ctx.guild.id == 477547500232769536:
            return

      if member == None:
        return await ctx.send(embed = discord.Embed(title = 'Северный Округ | Семечки', description = f'**Укажите пользователя**', colour = 0x09F2C8), delete_after = 5)
      if amount == None:
        return await ctx.send(embed = discord.Embed(title = 'Северный Округ | Семечки', description = f'**{member.mention}, укажите кол-во добавляемых семечек**', colour = 0x09F2C8), delete_after = 5)

      if coins.count_documents({"id": member.id}) == 0:
        a = addbt(member, amount)
        await ctx.send(embed = discord.Embed(title = 'Северный Округ | Семечки', description = f'**{ctx.author.mention}, вы добавили пользователю {member.mention} `{amount}` семечек.\nЕго баланс: `{a}` семечек**', colour = 0x09F2C8))
      else:
        a = addbt(member, amount)
        channel = self.bot.get_channel(841588696334598154)
        try:
          await channel.send(embed = discord.Embed(title = 'Выдача', description = f'**Модератор {ctx.author.mention} выдал семечек пользователю {member.mention} в размере `{amount}`**', colour = 0x25f20a, timestamp = ctx.message.created_at))
        except:
          pass
        await ctx.send(embed = discord.Embed(title = 'Северный Округ | Семечки', description = f'**{ctx.author.mention}, вы добавили пользователю {member.mention} `{amount}` семечек.\nЕго баланс: `{a}` семечек**', colour = 0x09F2C8), delete_after = 10)

    @commands.command()
    @commands.has_any_role(661284961428701209, id, id, '★ Продавец ★', id, id, id, '★ Technical Administrator Discord ★', id, id, id, '☆ Developer Discord ☆', id, id, id, '☆ Глав. Модерация Discord ☆')
    async def removecoins(self, ctx, member: discord.Member = None, amount:int = None):
      if not ctx.guild.id == 477547500232769536:
            return

      await ctx.message.delete()
      if member == None:
        return await ctx.send(embed = discord.Embed(title = 'Северный Округ | Семечки', description = f'**{ctx.author.mention}, укажите пользователя**', colour = 0x09F2C8), delete_after = 5)
      if amount == None:
        return await ctx.send(embed = discord.Embed(title = 'Северный Округ | Семечки', description = f'**{ctx.author.mention}, укажите кол-во убираемых cемечек**', colour = 0x09F2C8), delete_after = 5)
      
      a = proverka(member, amount)
      if a == 0:
        await ctx.send(embed = discord.Embed(title = 'Северный Округ | Семечки', description = f'**{ctx.author.mention}, пользователь не имеет такого кол-ва cемечек!**', colour = 0x09F2C8))
      else:
        bal = rebt(member, amount)
        channel = self.bot.get_channel(841588696334598154)
        await channel.send(embed = discord.Embed(title = 'Снятие', description = f'**Модератор {ctx.author.mention} снял семечек пользователю {member.mention} в размере `{amount}`**', colour = 0x25f20a, timestamp = ctx.message.created_at))
        await ctx.send(embed = discord.Embed(title = 'Северный Округ | Семечки', description = f'**{ctx.author.mention}, вы удалили у пользователя {member.mention} `{amount}` монет.\nЕго баланс: `{bal}` cемечек**', colour = 0x09F2C8), delete_after = 10)    

    @commands.command()
    async def pay(self, ctx, member: discord.Member = None, amount:int = None):
      if not ctx.guild.id == 477547500232769536:
            return

      if member == None:
        return await ctx.send(embed = discord.Embed(title = 'Северный Округ | Семечки', description = f'**{ctx.author.mention}, укажите пользователя**', colour = 0x09F2C8), delete_after = 5)
      
      if member == ctx.author or member.bot:
        return

      if amount == None:
        return await ctx.send(embed = discord.Embed(title = 'Северный Округ | Семечки', description = f'**{ctx.author.mention}, укажите сумму монет которую нужно передать!**', colour = 0x09F2C8), delete_after = 5)

      if amount <= 0:
        return await ctx.send(embed = discord.Embed(title = 'Северный Округ | Семечки', description = f'**{ctx.author.mention}, указан неверный аргумент!**', colour = 0x09F2C8), delete_after = 5)


      a = proverka(ctx.author, amount)
      if a == 0:
        await ctx.send(embed = discord.Embed(title = 'Северный Округ | Семечки', description = f'**{ctx.author.mention}, Вы не можете передать такую сумму!**', colour = 0x09F2C8))

      else:
        bal = addbt(member, amount)
        bal2 = rebt(ctx.author, amount)
        channel = self.bot.get_channel(841588696334598154)
        await channel.send(embed = discord.Embed(title = 'Перевод', description = f'**Пользователь {ctx.author.mention}, передал семечки пользователю {member.mention} в размере `{amount}`**', colour = 0x25f20a, timestamp = ctx.message.created_at))
        await ctx.send(embed = discord.Embed(title = 'Северный Округ | Семечки', description = f'**{ctx.author.mention}, Вы передали пользователю {member.mention} `{amount}` семечек.\nЕго баланс: `{bal}` cемечек\nВаш баланс: `{bal2}` cемечек**', colour = 0x09F2C8))
        
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def casino(self, ctx, amount : int = None):
      if not ctx.guild.id == 477547500232769536:
            return

      if not ctx.channel.id == 818222772215349328:
        await ctx.message.delete()
        return await ctx.send(embed = discord.Embed(description = f'**Команда `/casino` доступна только в канале <#818222772215349328>**', colour = 0x09F2C8), delete_after = 5)
        
      if amount == None:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(embed = discord.Embed(title = 'Северный Округ | Семечки', description = f'**{ctx.author.mention}, укажите кол-во семечек которое необходимо поставить!**', colour = 0x09F2C8))

      if amount <= 0:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(embed = discord.Embed(title = 'Северный Округ | Семечки', description = f'**{ctx.author.mention}, неверный аргумент!**', colour = 0x09F2C8))

      a = proverka(ctx.author, amount)
      if a == 0:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(embed = discord.Embed(title = 'Северный Округ | Семечки', description = f'**{ctx.author.mention}, Вы не можете сделать такую ставку!**', colour = 0x09F2C8))
      else:
        await ctx.send(embed = discord.Embed(title = f'Северный Округ | Семечки', description = f'**{ctx.author.mention}, Отдохни минутку и получешь результат!**', colour = 0x09F2C8))
        a = random.randint(1, 2)
        if a == 1:
        	await asyncio.sleep(5)
        	bal = rebt(ctx.author, amount)
        	await ctx.send(embed = discord.Embed(title = 'Северный Округ | Семечки', description = f'**{ctx.author.mention}, к сожалению, вы проиграли!\nТеперь Ваш баланс составляет: `{bal}` семечек!**', colour = 0xff0000))
        if a == 2:
        	amount *= 1
        	await asyncio.sleep(5)
        	f = amount
        	bal = addbt(ctx.author, f)
        	return await ctx.send(embed = discord.Embed(title = 'Северный Округ | Семечки', description = f'**{ctx.author.mention}, Вам повезло, вы удвоили свою ставку!!\nТеперь Ваш баланс составляет: `{bal}` семечек!**', colour = 0x25f20a))

    @commands.command()
    @commands.has_any_role(661284961428701209, id, id, '★ Продавец ★', id, id, id, '★ Technical Administrator Discord ★', id, id, id, '☆ Developer Discord ☆', id, id, id, '☆ Глав. Модерация Discord ☆')
    async def reset_coins(self, ctx, member: discord.Member = None):
      if not ctx.guild.id == 477547500232769536:
            return

      if not member:
        return await ctx.send(f'{ctx.author.mention}, ```Укажите пользователя!```', delete_after = 5)

      if ctx.author.top_role.position <= member.top_role.position:
        return

      if coins.count_documents({"id": member.id}) != 0:
        coins.update_one({"id": member.id}, {"$set": {"coins": 0}})
      else:
        pass
      channel = self.bot.get_channel(841588696334598154)
      await channel.send(embed = discord.Embed(title = 'Обнуление', description = f'**Модератор {ctx.author.mention} обнулил семечки пользователю {member.mention}!**', colour = 0x25f20a, timestamp = ctx.message.created_at))
      return await ctx.send(embed = discord.Embed(title = 'Обнуление', description = f'**Модератор {ctx.author.mention} обнулил семечки пользователю {member.mention}!**', colour = 0x25f20a), delete_after = 10)      
            
    @commands.Cog.listener()
    async def on_message(self, ctx):
    	if users.count_documents({"id": ctx.author.id}) == 0:
    		users.insert_one({"id": ctx.author.id, "messages": 0})
    		a = users.find_one({"id": ctx.author.id})["messages"]
    		users.update_one({"id": ctx.author.id}, {"$set": {"messages": a + 1}})
    	else:
    		a = users.find_one({"id": ctx.author.id})["messages"]
    		users.update_one({"id": ctx.author.id}, {"$set": {"messages": a + 1}})

    	st = 0
    	if len(list(ctx.content)) >= 1:
    		msgs = users.find_one({"id": ctx.author.id})["messages"]
    		if msgs == 2000:
    			await ctx.channel.send(embed = discord.Embed(title = 'Новое достижение!', description = f'**🎉 {ctx.author.mention}, вы получили новое достижение: `Написать 2000 сообщений!`\n🎉Вам добавлен бонус в размере 5 семечек <3**', colour = discord.Colour.blue()))
    			st += 5
    		if msgs == 5000:
    			await ctx.channel.send(embed = discord.Embed(title = 'Новое достижение!', description = f'**🎉 {ctx.author.mention}, вы получили новое достижение: `Написать 5000 сообщений!`\n🎉 Вам добавлен бонус в размере 15 семечек <3**', colour = discord.Colour.blue()))
    			st += 15

    		if st > 0:
    			addbt(ctx.author, st)

    @commands.command(aliases = ["messages", "сообщения"])
    async def __message(self, ctx, member: discord.Member = None):
      if not ctx.guild.id == 477547500232769536:
        return

      if member == None:
        member = ctx.author

      if users.count_documents({"id": member.id}) == 0:
        return await ctx.send(embed = discord.Embed(title = '🏆Северный Округ | Сообщений', description = f'Никнейм: {member.mention}\nСообщений: `0`', colour = 0x09F2C8))

      else:
        return await ctx.send(embed = discord.Embed(title = f'🏆 Северный Округ | Сообщений', description = f'Никнейм: {member.mention}\nСообщений: `{users.find_one({"id": member.id})["messages"]}`', colour = 0x09F2C8))

    @commands.command()
    async def achive(self, ctx):
    	if not ctx.guild.id == 477547500232769536:
            return
            
    	achive = []
    	msgs = users.find_one({"id": ctx.author.id})["messages"]

    	if msgs >= 2000:
    		achive.append('[✅] Написать `2000` сообщений\n')
    	else:
    		achive.append('[❌] Написать `2000` сообщений\n')
    	if msgs >= 5000:
    		achive.append('[✅] Написать `5000` сообщений\n')
    	else:
    		achive.append('[❌] Написать `5000` сообщений\n')

    	str_a = ''.join(achive)
    	embed = discord.Embed(title = f"`💰 Ачивки пользователя {ctx.author.name}`", colour = discord.Colour.blue())
    	embed.add_field(name = '♦ Сообщения:', value = f'{str_a}')
    	embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
    	await ctx.send(embed = embed)
      
def setup(bot):
    bot.add_cog(econom(bot))



'''
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
from pymongo import Mongobot

cluster = Mongobot("mongodb+srv://dbrbase:oT4y7678BFK00Bsp@rodinadb.rhew3.mongodb.net/rodinaname?retryWrites=true&w=majority")
db = cluster["rodina"]
report = db["report"]
coins = db["coins"]
users = db["users"]

def addbs(member, arg):
  if users.count_documents({"id": member}) == 0:
    users.insert_one({"id": member, "vsv": 0, "messages": 0})
    bal = 1 + users.find_one({"id": member})[arg]
    users.update_one({"id": member}, {"$set": {arg: bal}})
    return bal
  else:
    bal = 1 + users.find_one({"id": member})[arg]
    users.update_one({"id": member}, {"$set": {arg: bal}})
    return bal

# family.insert_one({"_id": ctx.author.id, "name": "привет"}) -> Запись в базу данных(Коллекция: Family) 
# if family.count_documents({"_id": ctx.author.id}) -> Проверка, есть значение или нет в базе данных(Коллекция: Family | Поиск по графе: _id) 
# family.find_one({"_id": ctx.author.id}) -> Получение значения из базы(Коллекция: Family | Поиск по графе: _id) 
# print(family.find_one({"_id": ctx.author.id})["name"]) -> Получение отдельного значения(Коллекция: Family | Поиск по графе: _id | Значение графы: name) 
# family.update_one({"_id": ctx.author.id}, {"$set": {"name": settle}}) -> Обновление значения в базе(Коллекция: Family | По графе: _id | Аргумент: $set - Замена | Значение графы: name | Устанавливаемое значение: settle)

global tens
tens = [ ]

def addbt(member: discord.Member, arg : int):
  if coins.count_documents({"id": member.id}) == 0:
    coins.insert_one({"guild": member.guild.id, "id": member.id, "coins": arg})
    return arg
  else:
    bal = arg + coins.find_one({"id": member.id})["coins"]
    coins.update_one({"id": member.id}, {"$set": {"coins": bal}})
    return bal

def rebt(member: discord.Member, arg : int):
  bal = coins.find_one({"id": member.id})["coins"] - arg
  coins.update_one({"id": member.id}, {"$set": {"coins": bal}})
  return bal

def proverka(member, stv : int):
  if coins.count_documents({"id": member.id}) == 0:
    return 0

  else:
    if coins.find_one({"id": member.id})["coins"] < stv:
      return 0
    else:
      return 1

def proc(args):
  s = 0
  if args >= 10 and args <= 30:
    s = 1
  elif args > 30 and args <= 50: 
    s = 2
  elif args > 50 and args <= 70: 
    s = 3
  elif args > 70 and args <= 90: 
    s = 4
  elif args > 90 and args <= 150: 
    s = 5
  elif args > 150: 
    s = 10

  return s


class econom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prev = []
    
    @commands.command()
    async def topcoins(self, ctx):
      if not ctx.guild.id == 577511138032484360:
        return

      if ctx.channel.id == 756183285188788306:
        return await ctx.message.delete()

      await ctx.message.delete()

      usr = db["users"]
      coins = db["coins"]
      zb = 0

      m = [ ]
      m2 = [ ]
      m3 = [ ]
      c = [ ]
      c2 = [ ]
      cz = [ ]
      cz2 = [ ]
      fr = 0
      zb = 50
      for i in coins.find({"guild": ctx.guild.id}):
        mname = discord.utils.get(ctx.guild.members, id = i["id"])
        if mname == None:
          continue
        m.append(i["coins"])
        cz.append(mname.name)

        coins = i["coins"]

        if usr.count_documents({"id": mname.id}) == 1:
          if usr.find_one({"id": mname.id})["messages"] < 0:
            msgs = 0
          else:
            msgs = usr.find_one({"id": mname.id})["messages"]
          
          if usr.find_one({"id": mname.id})["vsv"] < 0:
            voices = f'00:00:00'
          else:
            seconds = usr.find_one({"id": mname.id})["vsv"]
            seconds = seconds % (24 * 3600)
            hours = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            voices = f'{hours}:{minutes}:{seconds}'
        else:
          voices = f'00:00:00'
          msgs = 0

        c.append(f'**Коинов:** {coins} | **Сообщений:** {msgs} | 🎤 **{voices}**')
        fr += 1
        if fr >= 50:
          break
      
      m2 = m
      m3 = m
      c2 = c
      cz2 = cz
      t = sorted(m)[::-1]

      frf = 0
      frfz = 0
      stra = 1
      zbs = zb//10
      if zbs == 0:
        zbs = 1
      embed = discord.Embed(title = f'Таблица лидеров', description = f'**Страница `{stra}` из `5`**', colour = 0xFB9E14)
      for v in t:
        frfz += 1
        frf += 1
        f = m2.index(v)
        if frf == 1:
          frs = f'🥇 #1. {cz[f]}'
        elif frf == 2:
          frs = f'🥈 #2. {cz[f]}'
        elif frf == 3:
          frs = f'🥉 #3. {cz[f]}'
        else:
          frs = f'#{frf}. {cz[f]}'
        embed.add_field(name = frs, value = c[f], inline = False)
        c.remove(c[f])
        cz.remove(cz[f])
        m2.remove(m2[f])
        if frfz == 10:
          frfz = 0
          break     

      mes = await ctx.send(embed = embed)
      r_list = ['⬅', '➡', '⏺']
      for g in r_list:
        await mes.add_reaction(g)
      for i in range(100):
        try:
          react, user = await self.bot.wait_for('reaction_add', timeout= 100.0, check = lambda react, user: user == ctx.author and react.emoji in r_list)
        except Exception:
          try:
            await mes.delete()
          except:
            pass
        else:
          if react.emoji == '⏺':
            try:
              await mes.delete()
            except: 
              pass
          elif react.emoji == '➡':
            if stra == zbs:
              await self.bot.http.remove_reaction(ctx.channel.id, mes.id, react.emoji, ctx.author.id)
            else:
              m2 = []
              for fl in m3:
                m2.append(fl)

              c = []
              for fk in c2:
                c.append(fk)

              cz = []
              for fk in cz2:
                cz.append(fk)

              stra += 1
              embed = discord.Embed(title = f'Таблица лидеров', description = f'**Страница `{stra}` из `{zbs}`**', colour = 0xFB9E14)
              frf = (stra * 10) - 10
              for v in t:
                frfz += 1
                frf += 1
                s = frf - 1
                try:
                  f = m2.index(t[s])
                except:
                  frf -= 1
                  continue
                if frf == 1:
                  frs = f'🥇 #1. {cz[f]}'
                elif frf == 2:
                  frs = f'🥈 #2. {cz[f]}'
                elif frf == 3:
                  frs = f'🥉 #3. {cz[f]}'
                else:
                  frs = f'#{frf}. {cz[f]}'
                embed.add_field(name = frs, value = c[f], inline = False)
                c.remove(c[f])
                cz.remove(cz[f])
                m2.remove(m2[f])
                if frfz == 10:
                  frfz = 0
                  break 

              try:
                await mes.edit(embed = embed)   
              except:
                pass
              await self.bot.http.remove_reaction(ctx.channel.id, mes.id, react.emoji, ctx.author.id)

          elif react.emoji == '⬅':
            if stra == 1:
              await self.bot.http.remove_reaction(ctx.channel.id, mes.id, react.emoji, ctx.author.id)
            else:
              m2 = [ ]
              for fl in m3:
                m2.append(fl)
              
              c = []
              for fk in c2:
                c.append(fk)

              cz = []
              for fk in cz2:
                cz.append(fk)
              stra -= 1
              embed = discord.Embed(title = f'Таблица лидеров', description = f'**Страница `{stra}` из `{zbs}`**', colour = 0xFB9E14)
              frf = (stra * 10) - 10
              frfz = 0
              for v in t:
                frfz += 1
                frf += 1
                s = frf - 1
                try:
                  f = m2.index(t[s])
                except:
                  frf += 1
                  continue
                if frf == 1:
                  frs = f'🥇 #1. {cz[f]}'
                elif frf == 2:
                  frs = f'🥈 #2. {cz[f]}'
                elif frf == 3:
                  frs = f'🥉 #3. {cz[f]}'
                else:
                  frs = f'#{frf}. {cz[f]}'
                embed.add_field(name = frs, value = c[f], inline = False)
                c.remove(c[f])
                cz.remove(cz[f])
                m2.remove(m2[f])
                if frfz == 10:
                  frfz = 0
                  break 
              try:
                await mes.edit(embed = embed)   
              except:
                pass 
              await self.bot.http.remove_reaction(ctx.channel.id, mes.id, react.emoji, ctx.author.id)
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        guild = self.bot.get_guild(payload.guild_id)
        if guild == None:
          return
        if not guild.id == 325607843547840522:
            return
        if payload.member.bot:
            pass
        else:
            emoji = str(payload.emoji)
            channel = self.bot.get_channel(payload.channel_id)
            if not channel.id == 757601724122005616:
                return
            message = await channel.fetch_message(payload.message_id)
            if not message.id == 758135039094685709:
                return
            memb = discord.utils.get(message.guild.members, id=payload.user_id)
            
            if emoji == '🎊':
                return await memb.add_roles(discord.utils.get(guild.roles, id = 757589865180430458))
            elif emoji == '🧛':
                return await memb.add_roles(discord.utils.get(guild.roles, id = 757589810314739774))
            elif emoji == '🎤':
                return await memb.add_roles(discord.utils.get(guild.roles, id = 757589889133838386))
            elif emoji == '🎥':
                return await memb.add_roles(discord.utils.get(guild.roles, id = 757589809353981962))

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        if guild == None:
          return
        if not guild.id == 325607843547840522:
            return

        if payload.member.bot:
            pass
        else:
            emoji = str(payload.emoji)
            channel = self.bot.get_channel(payload.channel_id)
            if not channel.id == 757601724122005616:
                return
            message = await channel.fetch_message(payload.message_id)
            if not message.id == 758135039094685709:
                return
            memb = discord.utils.get(message.guild.members, id=payload.user_id)
            
            if emoji == '🎊':
                return await memb.remove_roles(discord.utils.get(guild.roles, id = 757589865180430458))
            elif emoji == '🧛':
                return await memb.remove_roles(discord.utils.get(guild.roles, id = 757589810314739774))
            elif emoji == '🎤':
                return await memb.remove_roles(discord.utils.get(guild.roles, id = 757589889133838386))
            elif emoji == '🎥':
                return await memb.remove_roles(discord.utils.get(guild.roles, id = 757589809353981962))

    @commands.command()
    async def coins(self, ctx, member: discord.Member = None):
      if not ctx.guild.id == 577511138032484360:
          return

      if member == None:
        member = ctx.author

      if coins.count_documents({"id": member.id}) == 0:
        return await ctx.send(embed = discord.Embed(title = 'Система монет', description = f'**{member.mention}, на вашем счету `0` коинов**', colour = 0xFB9E14))

      else:
        return await ctx.send(embed = discord.Embed(title = 'Система монет', description = f'**{member.mention}, на вашем счету `{coins.find_one({"id": member.id})["coins"]}` коинов**', colour = 0xFB9E14))

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def addcoins(self, ctx, member: discord.Member = None, amount:int = None):
      if not ctx.guild.id == 577511138032484360:
          return
      await ctx.message.delete()
      if member == None:
        return await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'**{ctx.author.name}, укажите пользователя**', colour = 0xFB9E14), delete_after = 5)
      if amount == None:
        return await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'**{ctx.author.name}, укажите кол-во добавляемых монет**', colour = 0xFB9E14), delete_after = 5)

      if coins.count_documents({"id": member.id}) == 0:
        a = addbt(member, amount)
        await ctx.send(embed = discord.Embed(title = 'Система монет', description = f'**{ctx.author.name}, вы добавили пользователю {member.mention} `{amount}` монет.\nЕго баланс: `{a}` коинов**', colour = 0xFB9E14))
      else:
        a = addbt(member, amount)
        await ctx.send(embed = discord.Embed(title = 'Система монет', description = f'**{ctx.author.name}, вы добавили пользователю {member.mention} `{amount}` монет.\nЕго баланс: `{a}` коинов**', colour = 0xFB9E14))

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def removecoins(self, ctx, member: discord.Member = None, amount:int = None):
      if not ctx.guild.id == 577511138032484360:
          return
      await ctx.message.delete()
      if member == None:
        return await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'**{ctx.author.name}, укажите пользователя**', colour = 0xFB9E14), delete_after = 5)
      if amount == None:
        return await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'**{ctx.author.name}, укажите кол-во убираемых монет**', colour = 0xFB9E14), delete_after = 5)
      
      a = proverka(member, amount)
      if a == 0:
        await ctx.send(embed = discord.Embed(title = 'Система монет', description = f'**{ctx.author.name}, пользователь не имеет такого кол-ва монет!**', colour = 0xFB9E14))
      else:
        bal = rebt(member, amount)
        await ctx.send(embed = discord.Embed(title = 'Система монет', description = f'**{ctx.author.name}, вы удалили у пользователя {member.mention} `{amount}` монет.\nЕго баланс: `{bal}` коинов**', colour = 0xFB9E14))    

    @commands.command()
    async def pay(self, ctx, member: discord.Member = None, amount:int = None):
      if not ctx.guild.id == 577511138032484360:
          return

      if ctx.channel.id == 756183285188788306:
        return await ctx.message.delete()

      await ctx.message.delete()
      if member == None:
        return await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'**{ctx.author.name}, укажите пользователя**', colour = 0xFB9E14), delete_after = 5)
      
      if member == ctx.author or member.bot:
        return

      if amount == None:
        return await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'**{ctx.author.name}, укажите сумму монет которую нужно передать!**', colour = 0xFB9E14), delete_after = 5)

      if amount <= 0:
        return await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'**{ctx.author.name}, указан неверный аргумент!**', colour = 0xFB9E14), delete_after = 5)


      a = proverka(ctx.author, amount)
      if a == 0:
        await ctx.send(embed = discord.Embed(title = 'Система монет', description = f'**{ctx.author.mention}, Вы не можете передать такую сумму!**', colour = 0xFB9E14))

      else:
        bal = addbt(member, amount)
        bal2 = rebt(ctx.author, amount)
        await ctx.send(embed = discord.Embed(title = 'Система монет', description = f'**{ctx.author.name}, Вы передали пользователю {member.mention} `{amount}` монет.\nЕго баланс: `{bal}` коинов\nВаш баланс: `{bal2}` коинов**', colour = 0xFB9E14))
        
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.member)
    async def casino(self, ctx, amount : int = None):
      if not ctx.guild.id == 577511138032484360:
        return

      if not ctx.channel.id == 756183285188788306:
        await ctx.message.delete()
        return await ctx.send(embed = discord.Embed(description = f'**Команда `/casino` доступна только в канале <#756183285188788306>**', colour = 0xFB9E14), delete_after = 5)
        
      if amount == None:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'**{ctx.author.name}, укажите кол-во монет которое необходимо поставить!**', colour = 0xFB9E14), delete_after = 5)

      if amount <= 0:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(embed = discord.Embed(title = 'Ошибка', description = f'**{ctx.author.name}, неверный аргумент!**', colour = 0xFB9E14), delete_after = 5)

      a = proverka(ctx.author, amount)
      if a == 0:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(embed = discord.Embed(title = 'Система монет', description = f'**{ctx.author.mention}, Вы не можете сделать такую ставку!**', colour = 0xFB9E14))
      else:
        await ctx.send(embed = discord.Embed(title = 'Система монет', description = f'**{ctx.author.name}, что же нам выпадет...**', colour = 0xFB9E14), delete_after = 5)
        a = random.randint(1, 2)
        if a == 1:
          await asyncio.sleep(5)
          bal = rebt(ctx.author, amount)
          await ctx.send(embed = discord.Embed(title = 'Система монет', description = f'**{ctx.author.mention}, к сожалению, вы проиграли!\nТеперь Ваш баланс составляет: `{bal}` коинов!**', colour = 0xFB9E14))
        if a == 2:
          af = random.choices([1, 2, 3, 4], weights=[80, 15, 5, 0.1])[0]
          if af == 1:
            text = 'Вам повезло, вы удвоили свою ставку!'
          elif af == 2:
            amount *= 5
            text = 'Ничего себе, Вы на столько везучий, что увеличили свою ставку в 5 раз!'
          elif af == 3:
            amount *= 10
            text = 'ВООООООООУ!!! Вам очень сильно повезло и фортуна увеличила вашу ставку в 10 раз!'
          elif af == 4:
            amount *= 100
            text = f'Я просто промолчу.... Этот счастливчик сорвал СУПЕР КУШ и умножил свою ставку В СТО РАЗ!!! Он получил целых `{amount}` коинов!'
          await asyncio.sleep(5)
          f = amount
          bal = addbt(ctx.author, f)
          return await ctx.send(embed = discord.Embed(title = 'Система монет', description = f'**{ctx.author.mention}, {text}\nТеперь Ваш баланс составляет: `{bal}` коинов!**', colour = 0xFB9E14))
            
    @commands.Cog.listener()
    async def on_message(self, ctx):
      if ctx.guild == None:
        return
        
      if not ctx.guild.id == 577511138032484360:
          return
      global mas

      if ctx.guild == None:
        return

      if not ctx.guild.id == 577511138032484360:
        return

      ath2 = re.findall(r'\w*', ctx.content.lower())

      rekl = ['http', 'https', 'www', '.ru', '.com', '.xxx']
      for i in ath2:
        if i in rekl:
          if not 'rodina' in ath2 and not 'hxa7jmt' in ath2:
            await ctx.delete()
            return await ctx.channel.send(embed = discord.Embed(description = f"**{ctx.author.mention}, ваше сообщение было удалено по подозрению в рекламе.**", colour = 0xFB9E14), delete_after = 10)



      if discord.utils.get(ctx.guild.roles, id = 736949012065943592) in ctx.author.roles:
        return

      if ctx.content.startswith('/') or ctx.content.startswith('!') or ctx.content.startswith('+'):
        return

      if ctx.author.bot:
        return

      st = 0
      if len(list(ctx.content)) >= 2:
        a = addbs(ctx.author.id, "messages")
        if a == 1000:
          await ctx.channel.send(embed = discord.Embed(title = 'Новое достижение!', description = f'**🎉 {ctx.author.mention}, вы получили новое достижение: `Написать 1000 сообщений!` 🎉\nВам добавлен бонус в размере 5000 коинов <3**', colour = 0xFB9E14))
          st = 5000
        if a == 3000:
          await ctx.channel.send(embed = discord.Embed(title = 'Новое достижение!', description = f'**🎉 {ctx.author.mention}, вы получили новое достижение: `Написать 3000 сообщений!` 🎉\nВам добавлен бонус в размере 10000 коинов <3**', colour = 0xFB9E14))
          st = 10000
        

        if st > 0:
          addbt(ctx.author, st)


        
      role_registr = [ 'роль', 'роли', 'дайте роль', 'хочу роль', 'роль дайте', 'выдайте роль', '-роль', 'Роль', 'Роли', 'Дайте роль', 'Хочу роль', 'Роль дайте', 'Выдайте роль', '-Роль', '!Роль', '!роль' ]
      if ctx.channel.id == 756183285188788306:
        if not ctx.content == '/casino' and not ctx.content.lower() in role_registr:
          return await ctx.delete()

      a = proc(len(list(ctx.content)))
      addbt(ctx.author, a)

    @commands.command()
    async def user(self, ctx, member: discord.Member = None):

      CHAS = {
        1: '1 час ночи',
        2: '2 часа ночи',
        3: '3 часа ночи',
        4: '4 часа ночи',
        5: '5 часов утра',
        6: '6 часов утра',
        7: '7 часов утра',
        8: '8 часов утра',
        9: '9 часов утра',
        10: '10 часов утра',
        11: '11 часов утра',
        12: '12 часов дня',
        13: '1 час дня',
        14: '2 часа дня',
        15: '3 часа дня',
        16: '4 часа дня',
        17: '5 часов вечера',
        18: '6 часов вечера',
        19: '7 часов вечера',
        20: '8 часов вечера',
        21: '9 часов вечера',
        22: '10 часов вечера',
        23: '11 часов вечера',
        00: 'первом часу ночи'
      }

      FCH = {
        1: 'Января', 
        2: 'Февраля', 
        3: 'Марта', 
        4: 'Апреля', 
        5: 'Мая', 
        6: 'Июня', 
        7: 'Июля', 
        8: 'Августа', 
        9: 'Сентября', 
        10: 'Октября', 
        11: 'Ноября',
        12: 'Декабря',
      }
      
      accept = [451410256736550918]
      rolid = [577524866320826368, 577524754798346261, 577524969051914262, 577523815890944007, 577525668061904899]
      member = ctx.author if not member else member
      roles = [ ]
      
      if not len(member.roles) == 1:
          f = 0
          for i in member.roles:
              if not i.id == ctx.guild.default_role.id:
                  f += 1
                  s = len(member.roles) - f
                  roles.append(f'`{s}.` <@&{i.id}>\n')
      embed = discord.Embed(colour = member.color, timestamp = ctx.message.created_at)

      embed.set_author(name = f"🍀 Информация о пользователе - {member}")
      embed.set_thumbnail(url = member.avatar_url)

      embed.add_field(name = "🔻 `Имя`", value = f'{member.display_name}', inline = False)
      if member.id == 646573856785694721 or member.id in accept:
          embed.add_field(name = f'♦ `Аккаунт`', value = f'{member.mention} <:verefication:733973297339039874> | Является оффициально подтверждённым', inline = False)
      else:
          embed.add_field(name = f'♦ `Аккаунт`', value = member.mention, inline = False)
      embed.add_field(name = "🔹 `ID`", value = f'{member.id}', inline = False)

      ath = re.split(r'\W+', str(member.created_at))

      vr = CHAS[int(ath[3])]
      fo = re.split(r'\W+', str(vr))

      embed.add_field(name = "⌚ `Зарегистрирован`", value = f'{ath[2]} {FCH[int(ath[1])]} {ath[0]} года в {fo[0]} {fo[1]} {fo[2]}', inline = False)

      ath = re.split(r'\W+', str(member.joined_at))

      vr = CHAS[int(ath[3])]
      fo = re.split(r'\W+', str(vr))

      embed.add_field(name = "⌚ `Вошел на сервер`", value = f'{ath[2]} {FCH[int(ath[1])]} {ath[0]} года в {fo[0]} {fo[1]} {fo[2]}', inline = False)

      if ctx.guild.id == 577511138032484360:
        if users.count_documents({"id": member.id}) == 1:
          if users.find_one({"id": member.id})["messages"] < 0:
            msgs = 0
          else:
            msgs = users.find_one({"id": member.id})["messages"]
          
          if users.find_one({"id": member.id})["vsv"] < 0:
            voices = f'00:00:00'
          else:
            seconds = users.find_one({"id": member.id})["vsv"]
            seconds = seconds % (24 * 3600)
            days = seconds // (60 * 60 * 24)
            hours = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            voices = f'{days} дн. {hours} ч. {minutes} мин. {seconds} cек'
        else:
          voices = f'00:00:00'
          msgs = 0
  
        embed.add_field(name = '🗣 Голосовая активность', value = f"`{voices}`", inline = False)
          
        embed.add_field(name = '✏ Всего сообщений', value = f'`Сообщений в чатах:` **{msgs}**')

        achive = []
        if msgs >= 1000:
          achive.append('[✅] Написать `1000` сообщений\n')
        else:
          achive.append('[❎] Написать `1000` сообщений\n')

        if msgs >= 3000:
          achive.append('[✅] Написать `3000` сообщений\n')
        else:
          achive.append('[❎] Написать `3000` сообщений\n')

        str_a = ''.join(achive)
        embed.add_field(name = '💰 `Достижения`', value = f'**{str_a}**')

      if member.bot:
        embed.add_field(name = "🔸 Информация", value = '`Этот аккаунт является Discord-Ботом!`', inline = False)
        return await ctx.send(embed = embed)

      if len(member.roles) <= 1:
        embed.add_field(name = f"📊 `Роли({len(roles)})`", value = '**Ролей нет.**', inline = False)
      elif len(member.roles) > 1:
        roles1 = roles[::-1]
        embed.add_field(name = f"📊 `Роли({len(roles)})`", value = "".join(roles1), inline = False)
        embed.add_field(name = "🏮 `Высшая роль`", value = member.top_role.mention, inline = False)

      teh1 = discord.utils.get(ctx.guild.roles, id = 703270075666268160)
      if teh1 in member.roles:
        embed.add_field(name = "🏆 Support", value = f'`Данный пользователь является является агентом технической поддержки` {teh1.mention}', inline = False)

      bust = discord.utils.get(ctx.guild.roles, id = 752179518168367176)
      if bust in member.roles:
        embed.add_field(name = "❤ Follow", value = f'`Данный пользователь поддержал данный Discord-Сервер.`', inline = False)
      
      if member.top_role.id in rolid:          
        embed.add_field(name = "📌 Importent Persone", value = f'`Данный пользователь является администратором проекта.`', inline = False)

      stadm = [577525590769532938, 577530456870748171, 577526148330815498]
      if member.top_role.id in stadm:
        embed.add_field(name = "<:owner:733973554206343168> Senior Administrator", value = f'`Данный пользователь находится в составе старшей администрации проекта.`', inline = False)

      embed.set_thumbnail(url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
      embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
      await ctx.send(embed = embed)

    @commands.command(aliases = ['теннис'])
    @commands.cooldown(1, 60, commands.BucketType.member)
    async def tennis(self, ctx, member: discord.Member = None, stavka : int = None):
      global tens
      stor = 0
      if not ctx.guild.id == 577511138032484360:
          return

      await ctx.message.delete()

      if not member:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(f'{ctx.author.mention}, ```Укажите пользователя с которым хотите начать игру!\n/tennis @Пользователь#1234 [сумма]```', delete_after = 5)

      if not stavka:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(f'{ctx.author.mention}, ```Укажите ставку на которую хотите сыграть!\n/tennis @Пользователь#1234 [сумма]```', delete_after = 5)

      if ctx.author.id in tens:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(f'{ctx.author.mention}, ```Вы находитесь в активной игре!```', delete_after = 5)

      if member.id in tens:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(f'{ctx.author.mention}, ```Этот пользователь находится в активной игре!```', delete_after = 5)

      if member == ctx.author:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(f'{ctx.author.mention}, ```Нельзя играть с самим собой!```', delete_after = 3)

      if stavka <= 0:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(f'{ctx.author.mention}, ```Нельзя выбрать ставку меньше или равной нулю!```', delete_after = 3)

      one = proverka(ctx.author, stavka)
      two = proverka(member, stavka)

      if not one == 1 or not two == 1:
        if not one == 1 and not two == 1:
          ctx.command.reset_cooldown(ctx)
          return await ctx.send(f'{ctx.author.mention}, ```Никто из участников не имеет нужной суммы!```', delete_after = 5)

        if not one == 1:
          ctx.command.reset_cooldown(ctx)
          return await ctx.send(f'{ctx.author.mention}, ```Вы не имеете нужной суммы!```', delete_after = 5)

        if not two == 1:
          ctx.command.reset_cooldown(ctx)
          return await ctx.send(f'{ctx.author.mention}, ```Выбранный пользователь не имеет нужно суммы```', delete_after = 5)

      try:
        await ctx.author.send('+', delete_after = 1)
      except discord.Forbidden:
        ctx.command.reset_cooldown(ctx)
        return await ctx.send(f'{ctx.author.mention}, ```Откройте личные сообщения в настройках конфиденциальности для того что бы начать игру!```', delete_after = 5)

      try:
        mes = await member.send(f'`[ZAPROS]` `Здравствуйте` {member.mention}! `Пользователь {ctx.author.display_name} хочет сыграть с вами в теннис.\nСтавка на игру: {stavka} коинов!\nДля того что бы принять его предложение нажмите на` 🔋 `под этим сообщением.`\n`В противном случае проигнорируйте это сообщение!`')
        await mes.add_reaction('🔋')
        await ctx.send(embed = discord.Embed(description = f'**Пользователю {member.name} было отправлено предложение сыграть.\nНа подтверждение ему даётся 30 секунд.**', colour = 0xFB9E14), delete_after = 10)
        try:
          react, user = await self.bot.wait_for('reaction_add', timeout= 30.0, check= lambda react, user: user == member and react.emoji == '🔋')
        except Exception:
          await mes.delete()
          return await ctx.send(f'{ctx.author.mention}, ```Пользователь проигнорировал Ваше предложение!```', delete_after = 15)
        else:
          await mes.delete()
          tens.append(member.id)
          tens.append(ctx.author.id)
          embed = discord.Embed(title = 'Игра в теннис', description = f'**Что это вообще такое? - Возник у вас вопрос.\nЭто увеселительная игра, в которой всё решает ваша удача и знание вашего оппонента!\nВ личные сообщения, бот присылает Вам сообщение, в котором вы должны будете выбрать, правую или левую сторону, так же можно ударить по середине!\nУсловно, это выбор стороны в которую Ваш соперник отправил мяч. Думать и отвечать необходимо достаточно быстро, так как на выбор Вам даётся ровно 15 секунд!\nЕсли в течении этого времени не будет выбрана сторона, Вы автоматом становитесь проигравшим. Для того что бы победить, Вам необходимо первым заработать 10 очков.\nКаждый гол даёт Вам одно очко, если Вы отбиваете мяч, тогда два.\n\nЖелаем Вам приятной игры, начало через 20 секунд. Первым бросает {member.display_name}, гости начинают!**', colour = 0xFB9E14)
          embed.set_author(name = 'Теннис - Rodina RP | Восточный Округ', icon_url = ctx.guild.icon_url)
          embed.set_footer(text = 'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
          embed.set_thumbnail(url = ctx.guild.icon_url)
          try:
            await member.send(embed = embed, delete_after = 20)
          except:
            tens.remove(member.id)
            tens.remove(ctx.author.id)
            rebt(member, stavka)
            addbt(ctx.author, stavka)
            return await ctx.send(f'{ctx.author.mention}, ```Игра закончена, кто-то закрыл личные сообщения...```', delete_after = 15)
          try:
            await ctx.author.send(embed = embed, delete_after = 20)
          except:
            tens.remove(member.id)
            tens.remove(ctx.author.id)
            addbt(member, stavka)
            rebt(ctx.author, stavka)
            return await ctx.send(f'{ctx.author.mention}, ```Игра закончена, кто-то закрыл личные сообщения...```', delete_after = 15)
          
          await asyncio.sleep(20)
          r_list = ['⬅', '⬆', '➡']
          with open("cogs/tennis.json", "r") as file:
              data = json.load(file)
          if str(ctx.guild.id) not in data.keys():
            data[str(ctx.guild.id)] = {}

    
          data[str(ctx.guild.id)][str(ctx.author.id)] = 0
          data[str(ctx.guild.id)][str(member.id)] = 0
          with open("cogs/tennis.json", "w") as file:
              json.dump(data, file, indent = 4)
          st = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
          for i in st:   
            with open("cogs/tennis.json", "r") as file:
              data = json.load(file)

            try:
              msg = await member.send(embed = discord.Embed(description = f'**{member.mention}, Ваш ход!\nВыбирайте в какую сторону вы ударите!\n\n> `Нажмите` ⬅ `для удара в левую сторону`\n> `Нажав на` ⬆ `Вы отправите мяч в середину.`\n> `Для удара в правую сторону используйте` ➡\n\nНа выбор даётся 15 секунд!**', colour = 0xFB9E14))
              for f in r_list:
                await msg.add_reaction(f)
              try:
                react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == member and react.emoji in r_list)
              except Exception:
                await msg.delete()
                data[str(ctx.guild.id)][str(member.id)] = 0
                data[str(ctx.guild.id)][str(ctx.author.id)] = 0
                with open("cogs/tennis.json", "w") as file:
                  json.dump(data, file, indent = 4)
                tens.remove(member.id)
                tens.remove(ctx.author.id)
                rebt(member, stavka)
                addbt(ctx.author, stavka)
                try:
                  await member.send(f'{member.mention}, ```Вы проиграли эту битву.\nПричина: Отсутствие действий.```', delete_after = 15)
                except:
                  pass
              
                try:
                  return await ctx.author.send(embed = discord.Embed(description = f'**Поздравляем, Вы выиграли партию у игрока {member.display_name}, `{stavka} коинов` зачислены Вам на счёт!\n[P.S]: Ваш соперник был исключён из игры за неактив!**', colour = 0xFB9E14), delete_after = 30)
                except:
                  return
              else:
                await msg.delete()
                if str(react.emoji) == r_list[0]:
                  stor = 'левую'
                  txt = 'Вы выбрали `левую` сторону, ожидайте дальнейшей информации!'
                elif str(react.emoji) == r_list[2]:
                  stor = 'правую'
                  txt = 'Вы выбрали `правую` сторону, ожидайте дальнейшей информации!'
                elif str(react.emoji) == r_list[1]:
                  stor = 'середине'
                  txt = 'Вы решили ударить по `середине`, ожидайте дальнейшей информации!'

                await member.send(embed = discord.Embed(description = f'**{txt}**', colour = 0xFB9E14), delete_after = 5)
                if ctx.author.id == 646573856785694721:
                  await ctx.author.send(f'`Выбор соперника: {stor}`', delete_after = 5)
                try:
                  msg = await ctx.author.send(embed = discord.Embed(description = f'**{ctx.author.mention}, Ваш соперник сделал ход!\nВыбирайте в какую сторону вы поставите ракетку, что бы отбить его подачу!\n\n`Нажмите` ⬅ `для выбора левой стороны`\n> `Нажав на` ⬆ `Вы отправите мяч в середину`\n`Для выбора правой стороны используйте` ➡\n\nНа выбор даётся 15 секунд!**', colour = 0xFB9E14))
                  for f in r_list:
                    await msg.add_reaction(f)
                  try:
                    react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in r_list)
                  except Exception:
                    await msg.delete()
                    data[str(ctx.guild.id)][str(member.id)] = 0
                    data[str(ctx.guild.id)][str(ctx.author.id)] = 0
                    tens.remove(member.id)
                    tens.remove(ctx.author.id)
                    rebt(member, stavka)
                    addbt(ctx.author, stavka)
                    try:
                      await member.send(f'{member.mention}, ```Вы проиграли эту битву.\nПричина: Отсутствие действий.```', delete_after = 15)
                    except:
                      pass

                    try:
                      return await ctx.author.send(embed = discord.Embed(description = f'**Поздравляем, Вы выиграли партию у игрока {member.display_name}, `{stavka} коинов` зачислены Вам на счёт!\n[P.S]: Ваш соперник был исключён из игры за неактив!**', colour = 0xFB9E14), delete_after = 30)
                    except:
                      pass
                  else:
                    await msg.delete()
                    if str(react.emoji) == r_list[0]:
                      a = 'левую'
                    elif str(react.emoji) == r_list[2]:
                      a = 'правую'
                    elif str(react.emoji) == r_list[1]:
                      a = 'середине'

                    if a == stor:
                      data[str(ctx.guild.id)][str(ctx.author.id)] += 2
                      g2 = data[str(ctx.guild.id)][str(member.id)]
                      g1 = data[str(ctx.guild.id)][str(ctx.author.id)]
                      text = f'{ctx.author.display_name} смог отбить мяч!\nТеперь счёт игры: `({ctx.author.display_name})` {g1} - {g2} `({member.display_name})`'
                    else:
                      data[str(ctx.guild.id)][str(member.id)] += 1
                      g2 = data[str(ctx.guild.id)][str(member.id)]
                      g1 = data[str(ctx.guild.id)][str(ctx.author.id)]
                      text = f'{ctx.author.display_name} не смог отбить мяч!\nТеперь счёт игры: `({ctx.author.display_name})` {g1} - {g2} `({member.display_name})`'
                    try:
                      await member.send(embed = discord.Embed(description = f'**{text}**', colour = 0xFB9E14), delete_after = 10)
                    except:
                      pass
                    try:
                      await ctx.author.send(embed = discord.Embed(description = f'**{text}**', colour = 0xFB9E14), delete_after = 10)
                    except:
                      pass
                    
                    g2 = data[str(ctx.guild.id)][str(member.id)]
                    g1 = data[str(ctx.guild.id)][str(ctx.author.id)]
                    if g2 >= 10:                           
                      tens.remove(member.id)
                      tens.remove(ctx.author.id)
                      data[str(ctx.guild.id)][str(member.id)] = 0
                      data[str(ctx.guild.id)][str(ctx.author.id)] = 0
                      addbt(member, stavka)
                      rebt(ctx.author, stavka)
                      with open("cogs/tennis.json", "w") as file:
                        json.dump(data, file, indent = 4)
                      try:
                        await member.send(f'{member.mention}, ```Вы выиграли эту партию у игрока {ctx.author.display_name}, так как набрали 10 очков первым!\n`{stavka} коинов` зачислены Вам на счёт!```', delete_after = 15)
                      except:
                        pass

                      try:
                        return await ctx.author.send(embed = discord.Embed(description = f'**К сожалению, вы проигрываете партию игроку {member.display_name}!\n[P.S]: Ваш соперник набрал 10 очков быстрее Вас!**', colour = 0xFB9E14), delete_after = 30)
                      except:
                        return
                    
                    if g1 >= 10:
                      tens.remove(member.id)
                      tens.remove(ctx.author.id)
                      data[str(ctx.guild.id)][str(member.id)] = 0
                      data[str(ctx.guild.id)][str(ctx.author.id)] = 0
                      rebt(member, stavka)
                      addbt(ctx.author, stavka)
                      with open("cogs/tennis.json", "w") as file:
                        json.dump(data, file, indent = 4)
                      try:
                        await ctx.author.send(f'{ctx.author.mention}, ```Вы выиграли эту партию у игрока {member.display_name}, так как набрали 10 очков первым!\n`{stavka} коинов` зачислены Вам на счёт!```', delete_after = 15)
                      except:
                        pass

                      try:
                        return await member.send(embed = discord.Embed(description = f'**К сожалению, вы проигрываете партию игроку {ctx.author.display_name}!\n[P.S]: Ваш соперник набрал 10 очков быстрее Вас!**', colour = 0xFB9E14), delete_after = 30)
                      except:
                        return
                    try:
                      msg = await ctx.author.send(embed = discord.Embed(description = f'**{ctx.author.mention}, теперь Ваш ход!\nВыбирайте в какую сторону вы ударите!\n\n> `Нажмите` ⬅ `для удара в левую сторону`\n> `Нажав на` ⬆ `Вы отправите мяч в середину`\n> `Для удара в правую сторону используйте` ➡\n\nНа выбор даётся 15 секунд!**', colour = 0xFB9E14))
                      for f in r_list:
                        await msg.add_reaction(f)                 
                      try:
                        react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in r_list)                      
                      except Exception:
                        await msg.delete()
                        data[str(ctx.guild.id)][str(member.id)] = 0
                        data[str(ctx.guild.id)][str(ctx.author.id)] = 0
                        tens.remove(member.id)
                        tens.remove(ctx.author.id)
                        addbt(member, stavka)
                        rebt(ctx.author, stavka)
                        with open("cogs/tennis.json", "w") as file:
                            json.dump(data, file, indent = 4)
                        try:
                          await ctx.author.send(f'{ctx.author.mention}, ```Вы проиграли эту битву.\nПричина: Отсутствие действий.```', delete_after = 15)
                        except:
                          pass
                        try:
                          return await member.send(embed = discord.Embed(description = f'**Поздравляем, Вы выиграли партию у игрока {ctx.author.display_name}, `{stavka} коинов` зачислены Вам на счёт!\n[P.S]: Ваш соперник был исключён из игры за неактив!**', colour = 0xFB9E14), delete_after = 30)
                        except:
                          return
                      
                      else:
                        await msg.delete()
                        if str(react.emoji) == r_list[0]:
                          stor = 'левую'
                          txt = 'Вы выбрали `левую` сторону, ожидайте дальнейшей информации!'
                        elif str(react.emoji) == r_list[2]:
                          stor = 'правую'
                          txt = 'Вы выбрали `правую` сторону, ожидайте дальнейшей информации!'
                        elif str(react.emoji) == r_list[1]:
                          stor = 'середине'
                          txt = 'Вы решили ударить по `середине`, ожидайте дальнейшей информации!'

                        await ctx.author.send(embed = discord.Embed(description = f'**{txt}**', colour = 0xFB9E14), delete_after = 5)
                        if member.id == 646573856785694721: 
                          await member.send(f'`Выбор соперника: {stor}`', delete_after = 5)
                        try:
                          msg = await member.send(embed = discord.Embed(description = f'**{member.mention}, Ваш соперник сделал ход!\nВыбирайте в какую сторону вы поставите ракетку, что бы отбить его подачу!\n\n`Нажмите` ⬅ `для выбора левой стороны`\n> `Нажав на` ⬆ `Вы отправите мяч в середину.`\n`Для выбора правой стороны используйте` ➡\n\nНа выбор даётся 15 секунд!**', colour = 0xFB9E14))
                          for f in r_list:
                            await msg.add_reaction(f)
                          try:
                            react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == member and react.emoji in r_list)
                          except Exception:
                            await msg.delete()
                            data[str(ctx.guild.id)][str(member.id)] = 0
                            data[str(ctx.guild.id)][str(ctx.author.id)] = 0
                            tens.remove(member.id)
                            tens.remove(ctx.author.id)
                            rebt(member, stavka)
                            addbt(ctx.author, stavka)
                            with open("cogs/tennis.json", "w") as file:
                                json.dump(data, file, indent = 4)
                            try:
                              await member.send(f'{member.mention}, ```Вы проиграли эту битву.\nПричина: Отсутствие действий.```', delete_after = 15)
                            except:
                              pass

                            try:
                              return await ctx.author.send(embed = discord.Embed(description = f'**Поздравляем, Вы выиграли партию у игрока {member.display_name}, `{stavka} коинов` зачислены Вам на счёт!\n[P.S]: Ваш соперник был исключён из игры за неактив!**', colour = 0xFB9E14), delete_after = 30)
                            except:
                              return
                          else:
                            await msg.delete()
                            if str(react.emoji) == r_list[0]:
                              a = 'левую'
                            elif str(react.emoji) == r_list[2]:
                              a = 'правую'
                            elif str(react.emoji) == r_list[1]:
                              a = 'середине'

                            if a == stor:
                              data[str(ctx.guild.id)][str(member.id)] += 2
                              g2 = data[str(ctx.guild.id)][str(member.id)]
                              g1 = data[str(ctx.guild.id)][str(ctx.author.id)]
                              text = f'{member.display_name} смог отбить мяч!\nТеперь счёт игры: `({ctx.author.display_name})` {g1} - {g2} `({member.display_name})`'
                            else:
                              data[str(ctx.guild.id)][str(ctx.author.id)] += 1
                              g2 = data[str(ctx.guild.id)][str(member.id)]
                              g1 = data[str(ctx.guild.id)][str(ctx.author.id)]
                              text = f'{member.display_name} не смог отбить мяч!\nТеперь счёт игры: `({ctx.author.display_name})` {g1} - {g2} `({member.display_name})`'
                            try:
                              await member.send(embed = discord.Embed(description = f'**{text}**', colour = 0xFB9E14), delete_after = 10)
                            except:
                              pass
                            try:
                              await ctx.author.send(embed = discord.Embed(description = f'**{text}**', colour = 0xFB9E14), delete_after = 10)
                            except:
                              pass

                            g2 = data[str(ctx.guild.id)][str(member.id)]
                            g1 = data[str(ctx.guild.id)][str(ctx.author.id)]
                            if g2 >= 10:                           
                              tens.remove(member.id)
                              tens.remove(ctx.author.id)
                              addbt(member, stavka)
                              rebt(ctx.author, stavka)
                              data[str(ctx.guild.id)][str(member.id)] = 0
                              data[str(ctx.guild.id)][str(ctx.author.id)] = 0
                              with open("cogs/tennis.json", "w") as file:
                                json.dump(data, file, indent = 4)
                              try:
                                await member.send(f'{member.mention}, ```Вы выиграли эту партию у игрока {ctx.author.display_name}, так как набрали 10 очков первым!\n`{stavka} коинов` зачислены Вам на счёт!```', delete_after = 15)
                              except:
                                pass

                              try:
                                return await ctx.author.send(embed = discord.Embed(description = f'**К сожалению, вы проигрываете партию игроку {member.display_name}!\n[P.S]: Ваш соперник набрал 10 очков быстрее Вас!**', colour = 0xFB9E14), delete_after = 30)
                              except:
                                pass
                            
                            if g1 >= 10:
                              tens.remove(member.id)
                              tens.remove(ctx.author.id)
                              rebt(member, stavka)
                              addbt(ctx.author, stavka)
                              data[str(ctx.guild.id)][str(member.id)] = 0
                              data[str(ctx.guild.id)][str(ctx.author.id)] = 0
                              with open("cogs/tennis.json", "w") as file:
                                json.dump(data, file, indent = 4)

                              try:
                                await ctx.author.send(f'{ctx.author.mention}, ```Вы выиграли эту партию у игрока {member.display_name}, так как набрали 10 очков первым!\n`{stavka} коинов` зачислены Вам на счёт!```', delete_after = 15)
                              except:
                                pass

                              try:
                                return await member.send(embed = discord.Embed(description = f'**К сожалению, вы проигрываете партию игроку {ctx.author.display_name}!\n[P.S]: Ваш соперник набрал 10 очков быстрее Вас!**', colour = 0xFB9E14), delete_after = 30)
                              except:
                                pass

                            with open("cogs/tennis.json", "w") as file:
                                json.dump(data, file, indent = 4)
                        
                        except discord.Forbidden:
                          data[str(ctx.guild.id)][str(member.id)] = 0
                          data[str(ctx.guild.id)][str(ctx.author.id)] = 0
                          tens.remove(member.id)
                          tens.remove(ctx.author.id)
                          with open("cogs/tennis.json", "w") as file:
                              json.dump(data, file, indent = 4)
                          return await ctx.send(f'{ctx.author.mention}, ```Игра закончена, кто-то закрыл личные сообщения...```', delete_after = 15)

                    except discord.Forbidden:
                      data[str(ctx.guild.id)][str(member.id)] = 0
                      data[str(ctx.guild.id)][str(ctx.author.id)] = 0
                      tens.remove(member.id)
                      tens.remove(ctx.author.id)
                      with open("cogs/tennis.json", "w") as file:
                          json.dump(data, file, indent = 4)
                      return await ctx.send(f'{ctx.author.mention}, ```Игра закончена, кто-то закрыл личные сообщения...```', delete_after = 15)
                
                except discord.Forbidden:
                  data[str(ctx.guild.id)][str(member.id)] = 0
                  data[str(ctx.guild.id)][str(ctx.author.id)] = 0
                  tens.remove(member.id)
                  tens.remove(ctx.author.id)
                  with open("cogs/tennis.json", "w") as file:
                      json.dump(data, file, indent = 4)
                  return await ctx.send(f'{ctx.author.mention}, ```Игра закончена, кто-то закрыл личные сообщения...```', delete_after = 15)

            except discord.Forbidden:
              data[str(ctx.guild.id)][str(member.id)] = 0
              data[str(ctx.guild.id)][str(ctx.author.id)] = 0
              tens.remove(member.id)
              tens.remove(ctx.author.id)
              with open("cogs/tennis.json", "w") as file:
                  json.dump(data, file, indent = 4)
              return await ctx.send(f'{ctx.author.mention}, ```Игра закончена, кто-то закрыл личные сообщения...```', delete_after = 15)

      except discord.Forbidden:
        ctx.command.reset_cooldown(ctx)
        with open("cogs/tennis.json", "w") as file:
            json.dump(data, file, indent = 4)
        return await ctx.send(f'{ctx.author.mention}, ```Выбранный пользователь ограничил отправку личных сообщений, я не могу отправить ему запрос на подтверждение!```', delete_after = 5)

    @commands.command(aliases = ['обнулить', 'очистить'])
    @commands.has_permissions(administrator = True)
    async def reset_coins(self, ctx, member: discord.Member = None):
      if not ctx.guild.id == 577511138032484360:
        return

      if ctx.channel.id == 756183285188788306:
        return await ctx.message.delete()

      await ctx.message.delete()
      if not member:
        return await ctx.send(f'{ctx.author.mention}, ```Укажите пользователя!```', delete_after = 5)

      if ctx.author.top_role.position <= member.top_role.position:
        return

      if coins.count_documents({"id": member.id}) != 0:
        coins.update_one({"id": member.id}, {"$set": {"coins": 0}})
      else:
        pass
      channel = self.bot.get_channel(736200220311945256)
      await channel.send(embed = discord.Embed(title = 'Обнуление', description = f'**Модератор {ctx.author.mention} обнулил коины пользователю {member.mention}!**', colour = 0xFB9E14, timestamp = ctx.message.created_at))
      return await ctx.send(f'{ctx.author} => {member}', embed = discord.Embed(title = 'Обнуление', description = f'**Модератор {ctx.author.mention} обнулил коины пользователю {member.mention}!**', colour = 0xFB9E14))

def setup(bot):
    bot.add_cog(econom(bot))

'''

