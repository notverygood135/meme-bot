import discord
from discord.ext import commands
import pytesseract
import os

os.environ["TESSDATA_PREFIX"] = "~/thuan-cu-to/tessdata"

class Text(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def meme(self, ctx):
    text = pytesseract.image_to_string('image.png')
    print(text)


def setup(bot):
  bot.add_cog(Text(bot))
  print('Text is loaded')