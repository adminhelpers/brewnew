import discord
from discord.ext import commands
import json
import asyncio
import sqlite3
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://dbrbase:oT4y7678BFK00Bsp@rodinadb.rhew3.mongodb.net/rodinaname?retryWrites=true&w=majority")
db = cluster["rodina"]
report = db["report"]
users = db["users"]

def addbt(member, arg):
  if users.count_documents({"id": member}) == 0:
    users.insert_one({"id": member, "vsv": 0, "messages": 0})
    bal = 1 + users.find_one({"id": member})[arg]
    users.update_one({"id": member}, {"$set": {arg: bal}})
  else:
    bal = 1 + users.find_one({"id": member})[arg]
    users.update_one({"id": member}, {"$set": {arg: bal}})

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prev = []
 
    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            for guild in self.bot.guilds:
                if guild.id == 577511138032484360:   
                  voices = [channel for channel in guild.voice_channels if not channel.category_id == 577838942133682177]
                  members = [channel.members for channel in voices]
                  ids = []
                  for lst in members:
                      for member in lst:
                          if not member.bot:
                            ids.append(member.id)
  
                  if len(ids) <= 0:
                      continue
  
                  for member in ids:
                    addbt(member, "vsv")
 
            await asyncio.sleep(1)
  
    
 
def setup(bot):
    bot.add_cog(Voice(bot))