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

global s
s = 0

class privats(commands.Cog):
    """privats Cog."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        print('Rodina 04 | Privates Rooms by dollar ム baby#3603 - Запущен')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before = None, after = None):
        global s

        if not member.guild.id == 477547500232769536:
            return

        if after.channel == None:
            return

        if (not before.channel == None) and (not after.channel == None):
            if before.channel.id == after.channel.id:
                return

        if not after.channel == None:
            if after.channel.id == 806485613222166538:
                if s == 1:
                    s = 0
                    return await member.move_to(None)
                s = 1
                mainCategory = discord.utils.get(member.guild.categories, id=806485611958501476)
                for i in mainCategory.voice_channels:
                    if len(i.members) == 0:
                        await i.delete()
                channel2 = await member.guild.create_voice_channel(name=f"{member.display_name}",category=mainCategory)
                await channel2.set_permissions(member, view_channel = True, connect = True, manage_channels = True, manage_permissions = False, speak = True, move_members = False, use_voice_activation = True, priority_speaker = True, mute_members = False, deafen_members = False)
                vch = self.bot.get_channel(806485613222166538)
                if not vch.members:
                    s = 0
                    return await channel2.delete()
                else:
                    if member in vch.members:
                        try:
                            await member.move_to(channel2)
                        except:
                            pass
                        if not channel2.members:
                            s = 0
                            return await channel2.delete()
                    else:
                        s = 0
                        return await channel2.delete()
                
                for i in mainCategory.channels:
                    if isinstance(i, discord.VoiceChannel):
                        if not i.id == 806485613222166538:
                            if len(i.members) == 0:
                                try:
                                    await i.delete()
                                except:
                                    pass
                s = 0
                def check(a,b,c):
                    return len(channel2.members) == 0
                await self.bot.wait_for('voice_state_update', check=check)
                return await channel2.delete()

def setup(bot):
    bot.add_cog(privats(bot))