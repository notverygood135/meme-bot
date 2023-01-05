import discord
from discord.ext import commands
import asyncio


class Compare(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def compare(self, ctx, atk1, cr1, cd1, bn1, em1, atk2, cr2, cd2, bn2, em2):
    dmg1 = float(atk1) * (1 + float(bn1)/100) * (1 + (float(cr1) * float(cd1))/10000)
    dmg2 = float(atk2) * (1 + float(bn2)/100) * (1 + (float(cr2) * float(cd2))/10000)
    
    dmg1 = dmg1 * (1 + (278 * float(em1)/(float(em1)+1400))/100)
    dmg2 = dmg2 * (1 + (278 * float(em2)/(float(em2)+1400))/100)

    if dmg1 > dmg2:
      diff = round((1 - dmg2/dmg1) * 100, 3)
      dmg1 = round(dmg1, 2)
      dmg2 = round(dmg2, 2)
      await ctx.send(f"First Input: {dmg1} :point_left: (+{diff}%)\nSecond Input: {dmg2}")
    elif dmg2 > dmg1:
      diff = round((1 - dmg1/dmg2) * 100, 3)
      dmg1 = round(dmg1, 2)
      dmg2 = round(dmg2, 2)
      await ctx.send(f"First Input: {dmg1}\nSecond Input: {dmg2} :point_left: (+{diff}%)")
    else:
      await ctx.send(f"First Input: {dmg1}\nSecond Input: {dmg2} :point_left: (+{diff}%)")
    

def setup(bot):
  bot.add_cog(Compare(bot))
  print('Compare is loaded')