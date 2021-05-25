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
warns = db["warns"]
muted = db["mute"]
banlist = db["ban"]

dbd = cluster["RodinaBD"]
reports = dbd["reports"]

def add(member: discord.Member, arg):
  if moder.count_documents({"guild": 477547500232769536, "id": member.id}) == 0:
    moder.insert_one({"guild": 477547500232769536, "id": member.id, "close": 0, "rasm": 0, "mute": 0, "kick": 0, "warn": 0, "ban": 0, "unwarn": 0, "unmute": 0, "vmute": 0, "vunmute": 0, "rols": 0, "repa": 0, "derols": 0, "dezaprols": 0, "vig": 0, "leader": 0, "x2": 0})
    moder.update_one({"guild": 477547500232769536, "id": member.id}, {"$set": {arg: 1}})
  else:
    moder.update_one({"guild": 477547500232769536, "id": member.id}, {"$set": {arg: moder.find_one({"guild": 477547500232769536, "id": member.id})[arg] + 1}})

class getform(commands.Cog):
    """DEBUG Cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        print('Rodina 04 | Moder-Form by dollar ム baby#3603 - Запущен')

    @commands.command(aliases = ['af', 'форма', 'addforma'])
    async def __addforma(self, ctx, *, amount = None):

        if not ctx.guild.id == 477547500232769536:
            return

        if not discord.utils.get(ctx.guild.roles, id = 652869023599558656) in ctx.author.roles and not discord.utils.get(ctx.guild.roles, id = 817813676178407425) in ctx.author.roles:
            return await ctx.send(f'`[ERR]` {ctx.author.mention}, `вам не доступна данная команда!`', delete_after = 5)

        await ctx.message.delete()
        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]
        if amount == None or not amount.split(' ')[0] in [f'{prefix}ban', f'{prefix}bantime', f'{prefix}kick', f'{prefix}warn', f'{prefix}unwarn', f'{prefix}mute', f'{prefix}unmute']:
            return await ctx.send(embed = discord.Embed(description = f':exclamation: **Пожалуйста ознакомьтесь с методом использования данной команды**\n\n> :sparkles: `| Как это работает?`\nВы отправляете форму на пользователя, после чего она будет добавлена в очередь, из которой её будут получать исполнители.\nПосле того, как Ваша форма будет принята, Вы получите уведомление об этом и данное действие будет записано в вашу модерскую статистику\n\n> :grey_question: `| Как правильно пользоваться командой?`\n**Команда:** `{prefix}addforma(af|форма) {prefix}command [**args]`\n\n> `{prefix}af {prefix}ban @Провокатор#1234 4.15 || dollar`\n-- Я добавлю в очередь форму на `бан` пользователя с указанием причины: `"4.15 || dollar"`\n\n> `{prefix}af {prefix}bantime @Провокатор#1234 3d 4.15 || dollar`\n-- Я добавлю в очередь форму на `временный бан` пользователя, сроком на `3 дня` с указанием причины: `"4.15 || dollar"`\n\n**Доступные команды**: `{prefix}ban, {prefix}bantime, {prefix}kick, {prefix}warn, {prefix}unwarn, {prefix}mute, {prefix}unmute`', color = 0xFB9E14), delete_after = 30)

        message = await ctx.send(embed = discord.Embed(title = 'Подтверждение отправки формы', description = f'**Ваша форма:**\n> {amount}\n\n`Для подтверждения нажмите` ✅\n`Для отмены нажмите` ❌', color = 0xFB9E14), delete_after = 10)
        await message.add_reaction('✅')
        await message.add_reaction('❌')
        try:
          react, user = await self.bot.wait_for('reaction_add', timeout= 15.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
        except Exception:
          return await message.delete()
        else:
          await message.delete()
          if str(react.emoji) == '❌':
                return await ctx.send(embed = discord.Embed(description = f'Вы успешно отменили действие!', color = 0xFB9E14), delete_after = 10)
          elif str(react.emoji) == '✅':
                form.insert_one({"guild": 477547500232769536, "by": ctx.author.id, "forma": amount})
                await ctx.send(embed = discord.Embed(title = 'Форма успешно отправлена', description = f'**Ваша форма:**\n> {amount}\n\n✅ Успешно записана в очередь и занимает `{len([i for i in form.find({"guild": 477547500232769536})])} позицию`', color = 0xFB9E14), delete_after = 10)
                return await self.bot.get_channel(594257934553448454).send(embed = discord.Embed(title = 'Новая форма', description = f'**Модератор {ctx.author.mention}`({ctx.author})` отправил новую форму**\n> {amount}\nОна занимает `{len([i for i in form.find({"guild": 477547500232769536})])} позицию` в очереди.\n\nДля того что бы принять её, пропишите команду: {prefix}getforma', color = 0xFB9E14))


    @commands.command(aliases = ['gf', 'getforma'])
    async def __getforma(self, ctx):
        prefix = reports.find_one({"guild_id": ctx.guild.id, "proverka": 1})["prefix"]

        if not ctx.guild.id == 477547500232769536:
            return

        await ctx.message.delete()

        if not discord.utils.get(ctx.guild.roles, id = 817813676178407425) in ctx.author.roles:
            return await ctx.send(f'`[ERR]` {ctx.author.mention}, `вам не доступна данная команда!`', delete_after = 5)

        if len([i for i in form.find({"guild": 477547500232769536})]) == 0:
            return await ctx.send(embed = discord.Embed(description = f'❌ На данный момент очередь пуста.', color = 0xFB9E14), delete_after = 10)

        zk = [i["_id"] for i in form.find({"guild": 477547500232769536})]
        nat = form.find_one({"_id": zk[0]})

        modr = discord.utils.get(ctx.guild.members, id = nat["by"])
        message = await ctx.send(embed = discord.Embed(description = f'Форма от модератора: {modr.mention}`({modr})`:\n> `{nat["forma"]}`\n\n`Для подтверждения нажмите` ✅\n`Для отказа нажмите` ❌\n\nВ очереди осталось: {len([i for i in form.find({"guild": 477547500232769536})])} форм', color = 0xFB9E14))
        await message.add_reaction('✅')
        await message.add_reaction('❌')
        try:
          react, user = await self.bot.wait_for('reaction_add', timeout= 30.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
        except Exception:
          return await message.delete()
        else:
          await message.delete()
          if str(react.emoji) == '❌':
                message = await ctx.send(embed = discord.Embed(description = f'❌ Вы отказались принимать форму от модератора <@!{nat["by"]}>\n\n`Если Вы хотите объяснить причину отклонения модератору, нажмите` ✅', color = 0xFB9E14))
                await message.add_reaction('✅')
                try:
                    react, user = await self.bot.wait_for('reaction_add', timeout= 30.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅'])
                except Exception:
                    try:
                        await modr.send(embed = discord.Embed(description = f'❌ Ваша форма: `{nat["forma"]}` была отклонена модератором {ctx.author.display_name}`({ctx.author})`.', color = 0xFB9E14))
                    except:
                        pass
                    form.delete_one({"_id": nat["_id"]})
                    return await message.delete()
                else:
                    await message.delete()
                    if str(react.emoji) == '✅':
                        message = await ctx.send(embed = discord.Embed(description = f'❌ Напишите в чат причину, по которой вы отклонили форму от модератора {modr.mention}`({modr})`.', color = 0xFB9E14))
                        def check(m):
                            return m.channel == ctx.channel and m.author == ctx.author
                        try:
                            msg = await self.bot.wait_for('message', check = check, timeout= 300.0)
                        except TimeoutError:
                            try:
                                await modr.send(embed = discord.Embed(description = f'❌ Ваша форма: `{nat["forma"]}` была отклонена модератором {ctx.author.display_name}`({ctx.author})`.', color = 0xFB9E14))
                            except:
                                pass
                            form.delete_one({"_id": nat["_id"]})
                            return await message.delete()
                        else:
                            await message.delete()
                            await msg.delete()
                            try:
                                await modr.send(embed = discord.Embed(description = f'❌ Ваша форма: `{nat["forma"]}` была отклонена модератором {ctx.author.display_name}`({ctx.author})`.\n**Причина указанная модератором:**\n> `{msg.content}`', color = 0xFB9E14))
                            except:
                                pass
                            form.delete_one({"_id": nat["_id"]})
                            return await ctx.send(embed = discord.Embed(description = f'Сообщение было отправлено модератору!', color = 0xFB9E14), delete_after = 5)

          elif str(react.emoji) == '✅':
            message = await ctx.send(embed = discord.Embed(description = f'✅ Вы согласились принять форму от модератора {modr.mention}`({modr})`.\n`Форма:` **{nat["forma"]}**\n\n**Если Вы хотите принять форму в ручную, используйте** ❌\n**Если Вы хотите выполнить действие автоматически используйте** ✅', color = 0xFB9E14))
            await message.add_reaction('✅')
            await message.add_reaction('❌')
            try:
                react, user = await self.bot.wait_for('reaction_add', timeout= 30.0, check= lambda react, user: user == ctx.author and react.emoji in ['✅', '❌'])
            except Exception:
                try:
                    await ctx.author.send(f'`{nat["forma"]}`', delete_after = 120)
                    await ctx.send(embed = discord.Embed(description = f'✅ Вы согласились принять форму от модератора. Скопируйте полное сообщение, которое отправлено Вам в личные сообщения.\nНе медлите, оно будет удалено через 2 минуты!', color = 0xFB9E14), delete_after = 10)
                except:
                    pass
                form.delete_one({"_id": nat["_id"]})
                await message.delete()
            else:
                try:
                    await message.delete()
                except:
                    pass
                if str(react.emoji) == '❌':
                    try:
                        form.delete_one({"_id": nat["_id"]})
                        await ctx.author.send(f'`{nat["forma"]}`', delete_after = 120)
                        await ctx.send(embed = discord.Embed(description = f'✅ Вы согласились принять форму от модератора. Скопируйте полное сообщение, которое отправлено Вам в личные сообщения.\nНе медлите, оно будет удалено через 2 минуты!', color = 0xFB9E14), delete_after = 10)
                    except:
                        pass
                    form.delete_one({"_id": nat["_id"]})
                elif str(react.emoji) == '✅':
                    cmd = nat["forma"].split(' ')[0].replace(prefix, '')
                    if cmd == 'unwarn':
                        try:
                            numbed = int(nat["forma"].split(' ')[1])
                        except:
                            form.delete_one({"_id": nat["_id"]})
                            return await ctx.send(embed = discord.Embed(description = f'✅ Вы выбрали автоматическое выполнение формы\n`Форма:` **{nat["forma"]}**\n\n**Форма была отклонена**\n> `Причина:` Модератор не правильно указал аргумент `[№ случая]`', color = 0xFB9E14), delete_after = 15)
                        if numbed > 10000 or numbed < 0:
                            form.delete_one({"_id": nat["_id"]})
                            return await ctx.send(embed = discord.Embed(description = f'✅ Вы выбрали автоматическое выполнение формы\n`Форма:` **{nat["forma"]}**\n\n**Форма была отклонена**\n> `Причина:` Модератор не правильно указал аргумент `[№ случая]`', color = 0xFB9E14), delete_after = 15)
                    else:
                        memberid = int(nat["forma"].split(' ')[1].replace('<@!', '').replace('>', ''))
                        if not memberid in [i.id for i in ctx.guild.members]:
                            form.delete_one({"_id": nat["_id"]})
                            return await ctx.send(embed = discord.Embed(description = f'✅ Вы выбрали автоматическое выполнение формы\n`Форма:` **{nat["forma"]}**\n\n**Форма была отклонена**\n> `Причина:` Пользователя нет на сервере.', color = 0xFB9E14), delete_after = 15)
                        member = discord.utils.get(ctx.guild.members, id = memberid)
                        if not cmd == 'unmute':
                            if cmd in ['mute', 'bantime']:
                                arg = nat["forma"].split(' ')[2]
                                if cmd == 'bantime':
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
                                elif cmd == 'mute':
                                    mute_role = discord.utils.get(ctx.guild.roles, id = 800085900435652678)
                                    sleep = 0
                                    
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
                                    
                                reason = nat["forma"].split(' ')[3]
                            else:
                                reason = nat["forma"].split(' ')[2]

                    if cmd == 'ban':
                        embed = discord.Embed(colour = member.color, timestamp = ctx.message.created_at) 
                        embed.set_author(name = f'Пользователь был забанен по форме!')
                        embed.add_field(name = 'Пользователь', value = f'**{member.display_name}** ({member.id})', inline = False) 
                        embed.add_field(name = 'Модератор отправивший форму:', value = f'**{modr.mention}**`({modr})`', inline = False)    
                        embed.add_field(name = 'Модератор принявший форму:', value = f'**{ctx.author.mention}**`({ctx.author})`', inline = False) 
                        embed.add_field(name = 'Причина', value = f'{reason}', inline = False)  
                        embed.set_thumbnail(url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
                        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                        channel = self.bot.get_channel(834039427541631016)
                        await channel.send(embed = embed) 
                        await ctx.guild.ban(member, reason = f'BANNED by {modr} | REASON: {reason} | FORM ACCEPTED: {ctx.author.display_name}')

                    elif cmd == 'kick':
                        embed = discord.Embed(colour = member.color, timestamp = ctx.message.created_at) 
                        embed.set_author(name = f'Пользователь был кикнут по форме!')
                        embed.add_field(name = 'Пользователь', value = f'**{member.display_name}** ({member.id})', inline = False) 
                        embed.add_field(name = 'Модератор отправивший форму:', value = f'**{modr.mention}**`({modr})`', inline = False)    
                        embed.add_field(name = 'Модератор принявший форму:', value = f'**{ctx.author.mention}**`({ctx.author})`', inline = False) 
                        embed.add_field(name = 'Причина', value = f'{reason}', inline = False)  
                        embed.set_thumbnail(url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
                        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                        channel = self.bot.get_channel(834039427541631016)
                        await channel.send(embed = embed) 
                        await ctx.guild.kick(member, reason = f'KICK by {modr} | REASON: {reason} | FORM ACCEPTED: {ctx.author.display_name}')

                    elif cmd == 'mute':

                        if mute_role in member.roles:
                            form.delete_one({"_id": nat["_id"]})
                            return await ctx.send(embed = discord.Embed(description = f'✅ Вы выбрали автоматическое выполнение формы\n`Форма:` **{nat["forma"]}**\n\n**Форма была отклонена**\n> `Причина:` Пользователь уже находится в мьюте.', color = 0xFB9E14), delete_after = 15) 
                        embed = discord.Embed(colour = member.color, timestamp = ctx.message.created_at) 
                        embed.set_author(name = f'Пользователь был замьючен по форме!')
                        embed.add_field(name = 'Пользователь', value = f'**{member.display_name}** ({member.mention})', inline = False) 
                        embed.add_field(name = 'Модератор отправивший форму:', value = f'**{modr.mention}**`({modr})`', inline = False)    
                        embed.add_field(name = 'Модератор принявший форму:', value = f'**{ctx.author.mention}**`({ctx.author})`', inline = False) 
                        embed.add_field(name = 'Время', value = f'**{tp}**')    
                        embed.add_field(name = 'Причина', value = f'{reason}', inline = False)  
                        embed.set_thumbnail(url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
                        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                        logs = self.bot.get_channel(834039427541631016)
                        await logs.send(embed = embed)
                        await member.add_roles(mute_role)
                        muted.insert_one({"guild": ctx.guild.id, "id": member.id, "time": sleep})

                    elif cmd == 'bantime':
                        try:
                            await ctx.guild.ban(member, reason = f'BANNED by {modr} | REASON: {reason} | TIME: {tp} | FORM ACCEPTED: {ctx.author.display_name}')
                            banlist.insert_one({"guild": ctx.guild.id, "type": "bands", "id": member.id, "time": fpl, "name": f'{member.name}#{member.discriminator}'})
                            embed = discord.Embed(colour = member.color, timestamp = ctx.message.created_at) 
                            embed.set_author(name = f'Пользователь был временно забанен по форме!')
                            embed.add_field(name = 'Модератор отправивший форму:', value = f'**{modr.mention}**`({modr})`', inline = False)    
                            embed.add_field(name = 'Модератор принявший форму:', value = f'**{ctx.author.mention}**`({ctx.author})`', inline = False)   
                            embed.add_field(name = 'Время', value = f'{tp}', inline = False)  
                            embed.add_field(name = 'Причина', value = f'{reason}', inline = False)  
                            embed.set_thumbnail(url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
                            embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                            channel = self.bot.get_channel(834039427541631016)
                            await channel.send(embed = embed) 
                            embed = discord.Embed(colour = member.color, timestamp = ctx.message.created_at) 
                            embed.set_author(name = f'Вы были временно забанены на сервере {ctx.guild.name}!')
                            embed.add_field(name = 'Модератор отправивший форму:', value = f'**{modr.mention}**`({modr})`', inline = False)    
                            embed.add_field(name = 'Модератор принявший форму:', value = f'**{ctx.author.mention}**`({ctx.author})`', inline = False)   
                            embed.add_field(name = 'Время', value = f'{tp}', inline = False)  
                            embed.add_field(name = 'Причина', value = f'{reason}', inline = False)  
                            embed.set_thumbnail(url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
                            embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                            try:
                                await member.send(embed = embed)
                            except:
                                pass
                        except:
                            return await ctx.send(embed = discord.Embed(description = f'✅ Вы выбрали автоматическое выполнение формы\n`Форма:` **{nat["forma"]}**\n\n**Форма была отклонена**\n> `Причина:` Не удалось забанить пользователя', color = 0xFB9E14), delete_after = 15)
                    
                    elif cmd == 'unmute':
                        mute_role = discord.utils.get(ctx.guild.roles, id = 800085900435652678)
                        if not mute_role in member.roles:
                            form.delete_one({"_id": nat["_id"]})
                            return await ctx.send(embed = discord.Embed(description = f'✅ Вы выбрали автоматическое выполнение формы\n`Форма:` **{nat["forma"]}**\n\n**Форма была отклонена**\n> `Причина:` Пользователь не находится в мьюте', color = 0xFB9E14), delete_after = 15)
                        if muted.count_documents({"id": member.id}) == 1:
                            muted.delete_one({"id": member.id})
                        await member.remove_roles(mute_role)
                        logs = self.bot.get_channel(834039427541631016)
                        await logs.send(embed = discord.Embed(description = f'**Модератор {ctx.author.mention}`({ctx.author})`, снял мут с пользователя {member.mention}`({member})` по форме от {modr.mention}`({modr})`**', colour = 0xFB9E14, timestamp = ctx.message.created_at))
                    
                    elif cmd == 'warn':
                        s = 0
                        for i in warns.find({"id": member.id}):
                            s += 1           

                        if int(s) == 2:
                            await ctx.guild.kick(member, reason = f'3/6 warns | Force by {modr} | Reason: {reason} | Form Accepted: {ctx.author.display_name}')
                            chan = self.bot.get_channel(834039427541631016)
                            reason = f'[{ctx.message.created_at.strftime("%m, %d - %H:%M:%S")}]: {reason}'
                            warns.insert_one({"proverka": 0, "numbed": warns.find_one({"proverka": 1})["numbed"], "id": member.id, "kto": f'{modr.name}#{modr.discriminator}', "reas": reason})
                            warns.update_one({"proverka": 1}, {"$set": {"numbed": warns.find_one({"proverka": 1})["numbed"] + 1}})
                            embed = discord.Embed(colour = member.color, timestamp = ctx.message.created_at) 
                            embed.set_author(name = f'Пользователь был кикнут по форме!')
                            embed.add_field(name = 'Пользователь', value = f'**{member.display_name}** ({member.id})', inline = False) 
                            embed.add_field(name = 'Модератор отправивший форму:', value = f'**{modr.mention}**`({modr})`', inline = False)    
                            embed.add_field(name = 'Модератор принявший форму:', value = f'**{ctx.author.mention}**`({ctx.author})`', inline = False) 
                            embed.add_field(name = 'Причина', value = f'3/6 Предупреждений | `(Команда {prefix}warn)` | Last: {reason}', inline = False)  
                            embed.set_thumbnail(url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
                            embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                            channel = self.bot.get_channel(834039427541631016)
                            await channel.send(embed = embed) 
                        elif int(s) == 5:
                            reason = f'[{ctx.message.created_at.strftime("%m.%d - %H:%M:%S")}]: {reason}'
                            await ctx.send(embed = discord.Embed(description = f'**{ctx.author.mention}, вы выдали пользователю {member.mention} предупреждение.\nКол-во предупреждений: 6/6 | Пользователь забанен.**', colour = 0xFB9E14))
                            await ctx.guild.ban(member, reason = f'6/6 warns | Force by {modr} | Reason: {reason} | Form Accepted: {ctx.author.display_name}')
                            for i in warns.find({"id": member.id}):
                                warns.delete_one({"_id": i["id"]})
                            embed = discord.Embed(colour = member.color, timestamp = ctx.message.created_at) 
                            embed.set_author(name = f'Пользователь был забанен по форме!')
                            embed.add_field(name = 'Пользователь', value = f'**{member.display_name}** ({member.id})', inline = False) 
                            embed.add_field(name = 'Модератор отправивший форму:', value = f'**{modr.mention}**`({modr})`', inline = False)    
                            embed.add_field(name = 'Модератор принявший форму:', value = f'**{ctx.author.mention}**`({ctx.author})`', inline = False) 
                            embed.add_field(name = 'Причина', value = f'6/6 Предупреждений | `(Команда {prefix}warn)` | Last: {reason}', inline = False)  
                            embed.set_thumbnail(url = 'https://images-ext-1.discordapp.net/external/yarwcyEZug1mZITDcgLOQKSbDh7O6361bRAu7S95qNU/https/avatars.mds.yandex.net/get-pdb/2826470/29569d4a-36f3-4b9c-94f5-027c7cfb03f6/s1200')
                            embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
                            channel = self.bot.get_channel(834039427541631016)
                            await channel.send(embed = embed) 
                        else:
                            reason = f'[{ctx.message.created_at.strftime("%m.%d - %H:%M:%S")}]: {reason}'
                            warns.insert_one({"proverka": 0, "numbed": warns.find_one({"proverka": 1})["numbed"], "id": member.id, "kto": f'{modr.name}#{modr.discriminator}', "reas": reason})
                            warns.update_one({"proverka": 1}, {"$set": {"numbed": warns.find_one({"proverka": 1})["numbed"] + 1}})
                            chan = self.bot.get_channel(834039427541631016)
                            embed = discord.Embed(title = 'Пользователю выдано предупреждение по форме!', colour = 0xFB9E14, timestamp = ctx.message.created_at)
                            embed.add_field(name = 'Пользователь', value = f'**{member.display_name}** ({member.id})', inline = False) 
                            embed.add_field(name = 'Модератор отправивший форму:', value = f'**{modr.mention}**`({modr})`', inline = False)    
                            embed.add_field(name = 'Модератор принявший форму:', value = f'**{ctx.author.mention}**`({ctx.author})`', inline = False) 
                            embed.add_field(name = 'Количество предупреждений', value = f'**{s}/3**', inline = False)
                            embed.add_field(name = 'Причина', value = f'{reason}', inline = False) 
                            embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = self.bot.user.avatar_url)
                            embed.set_thumbnail(url = ctx.guild.icon_url)
                            await chan.send(embed = embed)

                    elif cmd == 'unwarn':
                        if warns.count_documents({"numbed": numbed}) == 1:    
                            if not warns.find_one({"numbed": numbed})["id"] in [i.id for i in ctx.guild.members]:
                                form.delete_one({"_id": nat["_id"]})
                                return await ctx.send(embed = discord.Embed(description = f'✅ Вы выбрали автоматическое выполнение формы\n`Форма:` **{nat["forma"]}**\n\n**Форма была отклонена**\n> `Причина:` Пользователя нет на сервере.', color = 0xFB9E14), delete_after = 15)
                            memb = discord.utils.get(ctx.guild.members, id = warns.find_one({"numbed": numbed})["id"])
                            if memb.id == modr.id:
                                form.delete_one({"_id": nat["_id"]})
                                return await ctx.send(embed = discord.Embed(description = f'✅ Вы выбрали автоматическое выполнение формы\n`Форма:` **{nat["forma"]}**\n\n**Форма была отклонена**\n> `Причина:` Модератор хотел снять предупреждение самому себе, вот проказник!', color = 0xFB9E14), delete_after = 15)

                            chan = self.bot.get_channel(834039427541631016)
                            await chan.send(embed = discord.Embed(description = f'**{ctx.author.mention}`({ctx.author})`, снял пользователю {memb.mention}`({memb})` 1 предупреждение по форме от {modr.mention}`({modr})`**', colour = 0xFB9E14))
                            warns.delete_one({"numbed": numbed})
                        else:
                            form.delete_one({"_id": nat["_id"]})
                            return await ctx.send(embed = discord.Embed(description = f'✅ Вы выбрали автоматическое выполнение формы\n`Форма:` **{nat["forma"]}**\n\n**Форма была отклонена**\n> `Причина:` Указанного Варн-случая не существует.', color = 0xFB9E14), delete_after = 15)

                    await ctx.send(embed = discord.Embed(description = f'✅ Вы выбрали автоматическое выполнение формы\n`Форма:` **{nat["forma"]}**\n\n**Форма выполнена, благодарим за использование!**', color = 0xFB9E14), delete_after = 60)
            try:
                await modr.send(embed = discord.Embed(description = f'✅ `Ваша форма:` {nat["forma"]} была принята модератором {ctx.author.display_name}`({ctx.author})`.', color = 0xFB9E14))
            except:
                pass
            asd = {"ban": "ban", "bantime": "ban", "kick": "kick", "warn": "warn", "unwarn": "unwarn", "mute": "mute", "unmute": "unmute"}
            add(modr, asd[nat["forma"].split(' ')[0].replace(prefix, '')])
            form.delete_one({"_id": nat["_id"]})


def setup(bot):
    bot.add_cog(getform(bot))