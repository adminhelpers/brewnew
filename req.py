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

global number 
number = 0

class req(commands.Cog):
    """REQ Cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        print('Rodina 04 | Question System by dollar ム baby#3603 - Запущен')

    @commands.command()
    async def вопрос(self, ctx):
        global number
        if not ctx.guild.id == 577511138032484360:
            return

        if not ctx.channel.id == 577718720911376384:
            ch = self.bot.get_channel(577718720911376384)
            return await ctx.send(f'`[ERROR]` `Задавать вопросы можно только в канале` {ch.mention}', delete_after = 5)
        
        vch = self.bot.get_channel(579221894344081408)
        if not ctx.author in vch.members:
            return await ctx.send(f'`[ERROR]` `Задавать вопросы можно только если вы находитесь в голосовом канале` {vch.mention}', delete_after = 5)

        for i in cursor.execute('SELECT `id`, `name`, `number`, `mid`, `css` FROM `req` WHERE `id` = {}'.format(ctx.author.id)):
            if i[3] > 1:
                await ctx.message.add_reaction('🕐')
                return await ctx.channel.send(f'{ctx.author.mention}, `Вы уже отправляли запрос, дождитесь его одобрения.`', delete_after = 5)
            elif i[4] == 1:
                await ctx.message.add_reaction('❌')
                return await ctx.channel.send(f'{ctx.author.mention}, `вы находитесь в чёрном списке и не можете задавать вопросы.`', delete_after = 5)

        channel = self.bot.get_channel(736845886692524052)
        embed = discord.Embed(description = '`Discord >> Пользователь хочет задать вопрос`', colour = 0xFB9E14, timestamp = datetime.datetime.utcnow())
        embed.set_footer(text = f'Support Team by dollar ム baby#3603', icon_url = 'https://images-ext-1.discordapp.net/external/cVW5pAsyoLnQiTP-DZzQ3hLnIq-2Kw3rBZUVZ33Cz30/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/729309765431328799/684fd7878d39ba93511700dbf7a45931.webp?width=677&height=677')
        embed.add_field(name = 'Аккаунт', value = f'`Пользователь`: {ctx.author.mention}', inline = True)
        embed.add_field(name = 'Никнейм', value = f'`Ник:` {ctx.author.display_name}', inline = True)
        embed.add_field(name = 'Запрос из канала', value = f'{ctx.channel.mention}', inline = False)
        embed.add_field(name = 'Действия', value = '`[✔️] - Одобрить пользователя.`\n`[❌] - Отказать пользователю.`')

        message = await channel.send(embed = embed)
        await message.add_reaction('✔️')
        await message.add_reaction('❌')
        number += 1
        cursor.execute('INSERT INTO `req` (id, name, number, mid, css) VALUES ({}, "{}", {}, {}, 0)'.format(ctx.author.id, ctx.author.display_name, number, message.id))
        conn.commit()
        await ctx.author.edit(nick = f'Вопрос №{number}')
        await ctx.send('`[System]:` `Ваш запрос был отправлен в специальный канал. Как только его одобрит главный админитратор, вам сразу включат микрофон и изменять NickName на старый`', delete_after = 15)
        await ctx.message.add_reaction('📨')
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        if guild == None:
            return
        if not payload.guild_id == 577511138032484360:
            return

        user = self.bot.get_user(payload.user_id)
        if user.bot:
            pass
        else:
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            memb = discord.utils.get(message.guild.members, id=payload.user_id)
            emoji = str(payload.emoji)
                
            z = 0
            for i in cursor.execute('SELECT `id`, `name`, `number`, `mid` FROM `req` WHERE `mid` = {}'.format(message.id)):
                if i[0] > 3:
                    z = 1
            
            if z == 0:
                if not channel.id == 736845886692524052:
                    return
                else:
                    await message.delete()
                    return await channel.send(f'`[BUGTRAKER]` {memb.mention} `удалил багнутый запрос`')

            for i in cursor.execute('SELECT `id`, `name`, `number`, `mid` FROM `req`'):

                if i[3] == message.id:
                    if emoji == '✔️':
                        await message.delete()
                        
                        member = self.bot.get_guild(payload.guild_id).get_member(i[0])

                        if member == None:
                            await channel.send(f'`[BUGTRAKER]` {memb.mention} `запрос был багнутым, мне пришлось его удалить. ID Удалённого запроса: {i[0]}`')
                            cursor.execute('DELETE FROM `req` WHERE `id` = {}'.format(i[0]))
                            conn.commit()
                        else:
                            chan = self.bot.get_channel(577718720911376384)
                            await member.edit(mute = False)
                            await member.edit(nick = i[1])
                            await chan.send(f'{member.mention}, `главный администратор` {memb.mention} `одобрил ваш запрос!` `Заглушка снята и вы можете говорить`.')
                            await channel.send(f'`[ACCEPT]` {memb.mention} `одобрил запрос от {member.display_name}, c ID: {i[0]}`')
                            cursor.execute('DELETE FROM `req` WHERE `id` = {}'.format(i[0]))
                            conn.commit()
                    elif emoji == '❌':
                        await message.delete()
                        member = self.bot.get_guild(payload.guild_id).get_member(i[0])
                        if member == None:
                            await channel.send(f'`[BUGTRAKER]` {memb.mention} `запрос был багнутым, мне пришлось его удалить. ID Удалённого запроса: {i[0]}`')
                            cursor.execute('DELETE FROM `req` WHERE `id` = {}'.format(i[0]))
                            conn.commit()
                        else:
                            chan = self.bot.get_channel(577718720911376384)
                            await member.edit(nick = i[1])
                            await chan.send(f'{member.mention}, `модератор` {memb.mention} `отклонил ваш запрос. Ваш ник изменён.`')
                            await channel.send(f'`[DENY]` {memb.mention} `отклонил запрос от {member.display_name}, c ID: {i[0]}`')
                            cursor.execute('DELETE FROM `req` WHERE `id` = {}'.format(i[0]))
                            conn.commit()
                    else:
                        await message.delete()
                        return await user.send(f'❌ **{user.name}**, данная заявка уже обработана!')
                else:
                    pass

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def unreq(self, ctx, member: discord.Member = None):
        f = 0
        for i in cursor.execute('SELECT `id`, `name`, `number`, `mid` FROM `req` WHERE `id` = {}'.format(member.id)):
            if i[0] > 1:
                f = 1
        
        if f == 0:
            cursor.execute('INSERT INTO `req` (id, name, number, mid, css) VALUES ({}, "{}", 0, 0, 1)'.format(member.id, member.display_name))
            conn.commit()
            return await ctx.send(f'`[System]:` `Пользователь` {member.mention} `занесён в чёрный список вопросов`.')

        if f == 1:
            for i in cursor.execute(f'SELECT `id`, `name`, `number`, `mid` FROM `req` WHERE `id` = {member.id}'):
                chan = self.bot.get_channel(736845886692524052)
                mes = await chan.fetch_message(i[3])
                await mes.delete()
                await member.edit(nick = i[1])
            cursor.execute('DELETE FROM `req` WHERE `id` = {}'.format(member.id))
            cursor.execute('INSERT INTO `req` (id, name, number, mid, css) VALUES ({}, "{}", 0, 0, 1)'.format(member.id, member.display_name))
            conn.commit()
            return await ctx.send(f'`[System]:` `Пользователь` {member.mention} `занесён в чёрный список вопросов`.')

def setup(bot):
    bot.add_cog(req(bot))