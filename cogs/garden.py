import discord
from discord.ext import commands
import asyncio
import numpy
import random

plot = [
  [":white_large_square:", ":white_large_square:", ":white_large_square:"],
  [":white_large_square:", ":white_large_square:", ":white_large_square:"],
  [":white_large_square:", ":white_large_square:", ":white_large_square:"]
]

def match():
  msg = ""
  for i in range(0, 3):
      for j in range(0, 3):
        msg = msg + plot[i][j]
      msg = msg + "\n"
  return msg

class Garden(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def t3(self, ctx, opp):
    global auth
    auth = ctx.message.author
    global oppo
    oppo = opp
    global turn
    await ctx.send(match())


  @commands.command()
  async def m(self, ctx, x, y):  
    x = int(x)
    y = int(y)
    turn = 1
    if turn == 1:
      plot[x-1][y-1] = ":x:"
      await ctx.send(match())
      turn = 2
    elif turn == 2:
      plot[x-1][y-1] = ":o:"
      await ctx.send(match())
      turn = 1
    else:
      pass

  @commands.command()
  async def game(self, ctx):
    msg = ""
    for i in range(0, 3):
      for j in range(0, 3):
        msg = msg + plot[i][j]
      msg = msg + "\n"
    await ctx.send(msg)
  
def setup(bot):
  bot.add_cog(Garden(bot))
  print('Garden is loaded')