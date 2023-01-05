import discord
from discord.ext import commands
import asyncio
import random
import requests

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

response = requests.get(word_site)
words = response.content.splitlines()

word_display = []
guesses = []
guesses_amount = 0
game_active = False
lynch = [
  "```\n  __\n    |\n    |\n    |\n____|```",
  "```\n  __\n O  |\n    |\n    |\n____|```",
  "```\n  __\n O  |\n |  |\n    |\n____|```",
  "```\n  __\n O  |\n/|  |\n    |\n____|```",
  "```\n  __\n O  |\n/|\ |\n    |\n____|```",
  "```\n  __\n O  |\n/|\ |\n/   |\n____|```",
  "```\n  __\n O  |\n/|\ |\n/ \ |\n____|```"
]

def generate_message(guesses, guesses_amount, word_display):
  guessed = ""
  display = ""
  for char in guesses:
    guessed = guessed + char.upper() + " "
  for item in word_display:
    display = display + item
  return lynch[guesses_amount] + "word: " + display + "\nguessed letters: " + guessed

class Hangman(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def hm(self, ctx):
    global game_active
    global word
    if game_active == False:
      word = str(random.choice(words))[2:-1]
      game_active = True
      message = ""
      for char in word:
        word_display.append("\\_ ")
      for item in word_display:
        message = message + item
      await ctx.send(message)
    else:
      await ctx.send("có game đang dở")
    print(word_display)
    print(word)
    print(guesses_amount)

  @commands.command()
  async def h(self, ctx, guess):
    global game_active
    global guesses
    global guesses_amount
    global word
    global word_display
    if game_active == True:
      if len(guess.lower()) > 1:
        if guess.lower() == word:
          await ctx.send("you win. answer is " + word)
          guesses = []
          guesses_amount = 0
          game_active = False
          word_display = []
        else:
          guesses_amount += 1
          await ctx.send(generate_message(guesses, guesses_amount, word_display))
      else:
        if guess.lower() in word:
          for i in range(0, len(word)):
            if guess.lower() == word[i]:
              word_display[i] = guess.lower() + " "
          await ctx.send(generate_message(guesses, guesses_amount, word_display))
        else:
          guesses_amount += 1
          guesses.append(guess.lower())
          await ctx.send(generate_message(guesses, guesses_amount, word_display))
      if guesses_amount == 6:
        await ctx.send("you lose. đáp án là " + word)
        guesses = []
        guesses_amount = 0
        game_active = False
        word_display = []
      print(guesses_amount)
    else:
      await ctx.send("đéo có game để chơi")
  
  @commands.command()
  async def sh(self, ctx):
    global game_active
    global word_display
    game_active = False
    word_display = []
    await ctx.send("game stopped. answer was " + word)

def setup(bot):
  bot.add_cog(Hangman(bot))
  print('Hangman is loaded')