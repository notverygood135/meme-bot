import discord
from discord.ext import commands
import asyncio
import random
import sqlite3

conn = sqlite3.connect("accounts.db")
c = conn.cursor()

class Game(commands.Cog):
  def __init__(self, bot):
      self.bot = bot
  
  @commands.command()
  async def vcnv(self, ctx):
    pass
    
    

def setup(bot):
  bot.add_cog(Game(bot))
  print('Game is loaded')