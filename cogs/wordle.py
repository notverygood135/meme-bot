import discord
from discord.ext import commands
import asyncio
import random
import requests

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = requests.get(word_site)
words = response.content.splitlines()
words_5 = list(filter(lambda x: len(x) == 5, words))

guesses_amount = 0
game_active = False
word_display = []
char_count = {}


def generate_message(answer, guess):
  func_char_count = char_count.copy()
  print(func_char_count)
  guess_result = [":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:", ":white_large_square:"]
  message = ""
  
  for i in range(0, 5):
    if guess[i] == answer[i]:
      guess_result[i] = ":green_square:"
      func_char_count[guess[i]] -= 1
  for i in range(0, 5):
    if (guess[i] != answer[i]) and (guess[i] in answer) and (func_char_count[guess[i]] > 0):
      guess_result[i] = ":yellow_square:"
      func_char_count[guess[i]] -= 1
  
  word_display.append("".join(guess_result))
  for item in word_display:
    message = message + item + "\n"
  return message


class Wordle(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command()
  async def wd(self, ctx):
    global game_active
    global word
    if game_active == False:
      word = str(random.choice(words_5))[2:-1]
      for char in word:
        if char not in char_count:
          char_count[char] = 1
        elif char in char_count:
          char_count[char] += 1
          
      game_active = True
      message = ":white_large_square::white_large_square::white_large_square::white_large_square::white_large_square:"
      await ctx.send(message)
    else:
      await ctx.send("có game đang dở")
    print(word_display)
    print(word)
    print(guesses_amount)

  @commands.command()
  async def w(self, ctx, guess):
    global game_active
    global guesses
    global guesses_amount
    global word
    global word_display
    global char_count
    if game_active == True:
      if len(guess) != 5:
        await ctx.send("đoán từ 5 chữ thôi thằng ngu")
      else:
        if guess.lower() == word:
          await ctx.send("bạn là nhất. đáp án là " + word)
          guesses = []
          guesses_amount = 0
          game_active = False
          word_display = []
          char_count = {}
        else:
          guesses_amount += 1
          await ctx.send(generate_message(word, guess.lower()))
          
      if guesses_amount == 6:
        await ctx.send("mày ngu. đáp án là " + word)
        guesses = []
        guesses_amount = 0
        game_active = False
        word_display = []
        char_count = {}
      print(guesses_amount)
    else:
      await ctx.send("đéo có game để chơi")
  
  @commands.command()
  async def sw(self, ctx):
    global game_active
    global word_display
    global char_count
    game_active = False
    word_display = []
    char_count = {}
    await ctx.send("kém thế. đáp án là " + word)

def setup(bot):
  bot.add_cog(Wordle(bot))
  print('Wordle is loaded')