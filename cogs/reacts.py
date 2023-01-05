import discord
from discord.ext import commands


class Reacts(commands.Cog):
  def __init__(self, bot):
    self.bot = bot


  @commands.command()
  async def pog(self, ctx, username = None):
    await ctx.send("<:Pog:869964179652636722>")
    
  
  @commands.command()
  async def sadge(self, ctx, username = None):
    await ctx.send("<:Sadge:869964180076253285>")

  
  @commands.command()
  async def kekw(self, ctx, username = None):
    await ctx.send("<:KEKW:869964179073802361>")

  @commands.command()
  async def weird(self, ctx, username = None):
    await ctx.send("<:weirdchamp:980500442968645663>")

def setup(bot):
  bot.add_cog(Reacts(bot))
  print('Reacts is loaded')