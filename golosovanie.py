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
bmafia = db["mafia"]

global parse
parse = [ ] 

global mesids
mesids = 0

global golos 
golos = [ ]

global gls
gls = 0

global kto
kto = [ ]

class golosovanie(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Cog golosovanie by dollar ム baby#3603 успешно запущен!')

    @commands.command()
    async def голосование(self, ctx):
        if not ctx.guild.id == 477547500232769536:
            return

        global golos
        global mesids
        global parse
        global kto

        if not ctx.author.id == bmafia.find_one({"leader": 1})["ved"]:
            return await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, Вы не ведущий**', colour = 0xFB9E14), delete_after = 3)

        parse2 = [ ]
        react = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣']
        if len(parse) == 0:
            return await ctx.send(embed = discord.Embed(description = '**На голосование не выставлено ни одного пользователя.**', colour = 0xFB9E14), delete_after = 3)

        d = 0
        for i in parse:
            d += 1
            parse2.append(f'`{d}.` <@!{i}>\n')

        a = ''.join(parse2)
        mes = await ctx.send(embed = discord.Embed(description = f'**Пользователи выставленные на голосование:\n{a}\n{ctx.author.mention}, для окончания голосования напишите "Стоп" в этот чат.**', colour = 0xFB9E14))
        for i in parse2:
            await mes.add_reaction(react[0])
            react.remove(react[0])
        mesids = mes.id

        def check(check):
            return check.content.lower() == 'стоп' and check.author.id == ctx.author.id 

        msg = await self.bot.wait_for('message', check=check)
        await msg.delete()
        await mes.delete()
        parse2 = [ ]
        golos = [ ]
        parsed = [ ]
        mesids = 0
        d = 0
        for b in parse:
            d += 1
            parse2.append(f'`{d}.` <@!{bmafia.find_one({"id": b})["id"]}> | **{bmafia.find_one({"id": b})["golos"]}** голосов\n')
            parsed.append(i[0])
        a = ''.join(parse2)
        a2 = ''.join(kto)
        await ctx.send(embed = discord.Embed(description = f'**Голосование закончено, конечный результат:**\n{a}\n**Информация о голосовании:**\n{a2}', colour = 0xFB9E14))
        parse = [ ]
        kto = [ ]
        d = 0

    @commands.command(aliases = ['golos'])
    async def выставить(self, ctx, member: discord.Member = None):
        if not ctx.guild.id == 477547500232769536:
            return

        global parse

        await ctx.message.delete()

        if not ctx.author.id == bmafia.find_one({"leader": 1})["ved"]:
            return await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, Вы не ведущий**', colour = 0xFB9E14), delete_after = 3)

        if member == None:
            return await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, укажите пользователя!**', colour = 0xFB9E14), delete_after = 3)

        if member.id in parse:
            return await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, пользователь уже выставлен на голосование!**', colour = 0xFB9E14), delete_after = 3)

        if len(parse) >= 7:
            return await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, нельзя выставить на голосование больше 7 пользователей.**', colour = 0xFB9E14), delete_after = 3)

        if bmafia.count_documents({"id": member.id}) == 1:
            for i in bmafia.find({"id": member.id}):
                if not i["active"] == 0:
                    if member.id == i["ved"]:
                        return
                    bmafia.update_one({"id": member.id}, {"$set": {"golos": 0}})
                    parse.append(member.id)
                    return await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, пользователь {member.mention} успешно выставлен.**', colour = 0xFB9E14))
        else:
            return await ctx.send('`[ERROR]` `Пользователь не является участником мафии`', delete_after = 5) 

    @commands.command(aliases = ['список'])
    async def golist(self, ctx):
        global parse

        if not ctx.guild.id == 477547500232769536:
            return

        if not ctx.author.id == bmafia.find_one({"leader": 1})["ved"]:
            return await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, Вы не ведущий**', colour = 0xFB9E14), delete_after = 3)

        if len(parse) == 0:
            return await ctx.send(embed = discord.Embed(description = '**На голосование не выставлено ни одного пользователя.**', colour = 0xFB9E14), delete_after = 3)
        
        parse3 = [ ]

        d = 0
        for i in parse:
            d += 1
            parse3.append(f'`{d}.` <@!{i}>\n')

        a = ''.join(parse3)
        return await ctx.send(embed = discord.Embed(description = f'**Пользователи выставленные на голосование:\n{a}**', colour = 0xFB9E14))

    @commands.command(aliases = ['ungolos'])
    async def снять_с_голосования(self, ctx, member: discord.Member = None):
        if not ctx.guild.id == 477547500232769536:
            return

        global parse

        await ctx.message.delete()

        if not ctx.author.id == bmafia.find_one({"leader": 1})["ved"]:
            return await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, Вы не ведущий**', colour = 0xFB9E14), delete_after = 3)

        if member == None:
            return await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, укажите пользователя!**', colour = 0xFB9E14), delete_after = 3)

        if not member.id in parse:
            return await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, пользователь не выставлен на голосование!**', colour = 0xFB9E14), delete_after = 3)

        if bmafia.count_documents({"id": member.id}) == 1:
            for i in bmafia.find({"id": member.id}):
                if not i["name"] == 0:
                    if member.id == i["ved"]:
                        return
                    parse.remove(member.id)
                    return await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, пользователь {member.mention} успешно снят с голосования.**', colour = 0xFB9E14))
        else:
            return await ctx.send('`[ERROR]` `Пользователь не является участником мафии`', delete_after = 5) 

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        if guild == None:
            return
        if not guild.id == 477547500232769536:
            return

        global golos
        global mesids
        global parse
        global gls
        global kto

        user = self.bot.get_user(payload.user_id)
        if user.bot:
            pass
        else:
            emoji = str(payload.emoji)
            channel = self.bot.get_channel(payload.channel_id)
            if not channel.id == 806215020333236244:
                return
            message = await channel.fetch_message(payload.message_id)
            if not message.id == mesids:
                return
            memb = discord.utils.get(message.guild.members, id=payload.user_id)
            if not bmafia.count_documents({"id": memb.id}) == 1 or not bmafia.find_one({"id": memb.id})["active"] == 1:
                return

            if memb.id in golos:
                return await channel.send(embed = discord.Embed(description = f'**{memb.mention}, Вы уже приняли участие в голосовании!**', colour = 0xFB9E14), delete_after = 3)

            if gls == 1:
                return await channel.send(embed = discord.Embed(description = f'**Ожидайте, сейчас на записи другой участник!**', colour = 0xFB9E14), delete_after = 3)

            gls = 1
            if emoji == '1⃣':
                if parse[0] == memb.id:
                    pass
                bmafia.update_one({"id": parse[0]}, {"$set": {"golos": bmafia.find_one({"id": parse[0]})["golos"] + 1}})
                kto.append(f'`Игрок` {memb.mention} `=> голос в игрока` <@!{parse[0]}>\n')
            if emoji == '2⃣':
                if parse[1] == memb.id:
                    pass
                bmafia.update_one({"id": parse[1]}, {"$set": {"golos": bmafia.find_one({"id": parse[1]})["golos"] + 1}})
                kto.append(f'`Игрок` {memb.mention} `=> голос в игрока` <@!{parse[1]}>\n')
            if emoji == '3⃣':
                if parse[2] == memb.id:
                    pass
                bmafia.update_one({"id": parse[2]}, {"$set": {"golos": bmafia.find_one({"id": parse[2]})["golos"] + 1}})
                kto.append(f'`Игрок` {memb.mention} `=> голос в игрока` <@!{parse[2]}>\n')
            if emoji == '4⃣':
                if parse[3] == memb.id:
                    pass
                bmafia.update_one({"id": parse[3]}, {"$set": {"golos": bmafia.find_one({"id": parse[3]})["golos"] + 1}})
                kto.append(f'`Игрок` {memb.mention} `=> голос в игрока` <@!{parse[3]}>\n')
            if emoji == '5⃣':
                if parse[4] == memb.id:
                    pass
                bmafia.update_one({"id": parse[4]}, {"$set": {"golos": bmafia.find_one({"id": parse[4]})["golos"] + 1}})
                kto.append(f'`Игрок` {memb.mention} `=> голос в игрока` <@!{parse[4]}>\n')
            if emoji == '6⃣':
                if parse[5] == memb.id:
                    pass
                bmafia.update_one({"id": parse[5]}, {"$set": {"golos": bmafia.find_one({"id": parse[5]})["golos"] + 1}})
                kto.append(f'`Игрок` {memb.mention} `=> голос в игрока` <@!{parse[5]}>\n')
            if emoji == '7⃣':
                if parse[6] == memb.id:
                    pass
                bmafia.update_one({"id": parse[6]}, {"$set": {"golos": bmafia.find_one({"id": parse[6]})["golos"] + 1}})
                kto.append(f'`Игрок` {memb.mention} `=> голос в игрока` <@!{parse[6]}>\n')

            golos.append(memb.id)
            gls = 0
            
def setup(bot):
    bot.add_cog(golosovanie(bot))