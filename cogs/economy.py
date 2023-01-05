import discord
from discord.ext import commands
import random
import sqlite3
import asyncio


conn = sqlite3.connect("accounts.db")
c = conn.cursor()

coin = ['heads', 'tails']


class Economy(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def balance(self, ctx):
    name = str(ctx.message.author)
    c.execute("SELECT * FROM users WHERE name = :name", {'name':name})
    try:
      money = str(c.fetchall()[0][2])
      await ctx.send("you have " + money + " shit(s)")
    except IndexError:
      await ctx.send("You need to create an account using the following format: !create [username]")


  @commands.command()
  async def whale(self, ctx):
    name = str(ctx.message.author)
    c.execute("SELECT * FROM users WHERE name = :name", {'name':name})
    try:
      money = c.fetchall()[0][2]
      c.execute("""UPDATE users SET money = :money
            WHERE name = :name""", {'name':name, 'money':money + 500000})
      conn.commit()
      await ctx.send(name + " received 500000 shits")
    except IndexError:
      await ctx.send("You need to create an account using the following format: !create [username]")


  @commands.command()
  async def cf(self, ctx, amount = str(1), side = 'heads'):
    name = str(ctx.message.author)
    c.execute("SELECT * FROM users WHERE name = :name", {'name':name})
    try:
      money = c.fetchall()[0][2]  
      if side == 't':
        side = 'tails'
      if amount == 'all':
        amount = money
      else:
        amount = int(amount)
      if money == 0:
        await ctx.send("you broke")
      elif money < amount:
        await ctx.send("you broke")
      else:
        await ctx.send(str(ctx.author) + " spent " + str(amount) + " and chose " + side)
        result = random.choice(coin)
        await asyncio.sleep(3)
        if side == result:
          c.execute("""UPDATE users SET money = :money
            WHERE name = :name""", {'name':name, 'money':money + amount})
          conn.commit()
          await ctx.send("The coin landed on " + result + ", you won " + str(amount) + " shit(s)!" )
        else:
          c.execute("""UPDATE users SET money = :money
            WHERE name = :name""", {'name':name, 'money':money - amount})
          conn.commit()
          await ctx.send("The coin landed on " + result + ", you lost " + str(amount) + " shit(s)!" )
    except IndexError:
      await ctx.send("You need to create an account using the following format: !create [username]")
      

def setup(bot):
  bot.add_cog(Economy(bot))
  print('Economy is loaded')