import discord
from discord.ext import commands
import sqlite3


conn = sqlite3.connect("accounts.db")
c = conn.cursor()


class Account(commands.Cog):
  def __init__(self, bot):
    self.bot = bot


  @commands.command()
  async def create(self, ctx, username = None):
    name = str(ctx.message.author)
    try:
      if username == None:
        await ctx.send("Create an account using the following format: !create [username]")
      else:
        c.execute("INSERT INTO users VALUES(:name, :username, :money, :exp, :level, :max_hp, :hp, :atk, :def, :wep, :arm, :area)", {'name': name, 'username': username, 'money': 0, 'exp': 0, 'level': 1, 'max_hp': 100, 'hp': 100, 'atk': 10, 'def': 10, 'wep': 'Wooden Sword', 'arm': 'Wooden Armor', 'area': 1})
        conn.commit()
        await ctx.send("Successfully logged in as " +  username)
    except sqlite3.IntegrityError:
      await ctx.send("You cannot create more than 1 account")


def setup(bot):
  bot.add_cog(Account(bot))
  print('Account is loaded')