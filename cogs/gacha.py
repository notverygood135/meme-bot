import discord
from discord.ext import commands
import random
import sqlite3
import asyncio


conn = sqlite3.connect("accounts.db")
c = conn.cursor()


epitomized_weapon = ["Mistsplitter Reforged", "Thundering Pulse"]

weapons = {
"epitomized_choice" : [
  "weapons/Weapon_Mistsplitter_Reforged_Wish.png", 
  "weapons/Weapon_Thundering_Pulse_Wish.png"
],

"three_star" : [
  "weapons/Weapon_Black_Tassel_Wish.png", 
  "weapons/Weapon_Bloodtainted_Greatsword_Wish.png", 
  "weapons/Weapon_Cool_Steel_Wish.png", 
  "weapons/Weapon_Debate_Club_Wish.png", "weapons/Weapon_Emerald_Orb_Wish.png", 
  "weapons/Weapon_Ferrous_Shadow_Wish.png",
  "weapons/Weapon_Harbinger_of_Dawn_Wish.png",
  "weapons/Weapon_Magic_Guide_Wish.png",
  "weapons/Weapon_Raven_Bow_Wish.png",
  "weapons/Weapon_Sharpshooter%27s_Oath_Wish.png",
  "weapons/Weapon_Skyrider_Sword_Wish.png",
  "weapons/Weapon_Slingshot_Wish.png",
  "weapons/Weapon_Thrilling_Tales_of_Dragon_Slayers_Wish.png",
  "weapons/Weapon_Twin_Nephrite_Wish.png",
  "weapons/Weapon_White_Tassel_Wish.png"
],

"four_star_ra" : [
  "weapons/Weapon_Akoumaru_Wish.png",
  "weapons/Weapon_Favonius_Sword_Wish.png",
  "weapons/Weapon_Favonius_Lance_Wish.png",
  "weapons/Weapon_Eye_of_Perception_Wish.png",
  "weapons/Weapon_Rust_Wish.png"
],

"four_star_nra" : [
  "weapons/Weapon_Dragon%27s_Bane_Wish.png",
  "weapons/Weapon_Favonius_Codex_Wish.png",
  "weapons/Weapon_Favonius_Greatsword_Wish.png",
  "weapons/Weapon_Favonius_Warbow_Wish.png",
  "weapons/Weapon_Lion%2527s_Roar_Wish.png",
  "weapons/Weapon_Rainslasher_Wish.png",
  "weapons/Weapon_Sacrificial_Bow_Wish.png",
  "weapons/Weapon_Sacrificial_Fragments_Wish.png",
  "weapons/Weapon_Sacrificial_Greatsword_Wish.png",
  "weapons/Weapon_Sacrificial_Sword_Wish.png",
  "weapons/Weapon_The_Bell_Wish.png",
  "weapons/Weapon_The_Stringless_Wish.png",
  "weapons/Weapon_The_Widsith_Wish.png"
],

"five_star_nra" : [
  "weapons/Weapon_Amos%27_Bow_Wish.png",
  "weapons/Weapon_Aquila_Favonia_Wish.png",
  "weapons/Weapon_Lost_Prayer_to_the_Sacred_Winds_Wish.png",
  "weapons/Weapon_Primordial_Jade_Winged-Spear_Wish.png",
  "weapons/Weapon_Skyward_Atlas_Wish.png",
  "weapons/Weapon_Skyward_Blade_Wish.png",
  "weapons/Weapon_Skyward_Harp_Wish.png",
  "weapons/Weapon_Skyward_Pride_Wish.png",
  "weapons/Weapon_Skyward_Spine_Wish.png",
  "weapons/Weapon_Wolf%27s_Gravestone_Wish.png"
]
}


def roll(result, pity4, pity5, guarantee4, guarantee5, fp, epitomized_path):
  five_rate = 99301.0
  four_rate = five_rate - 6000
  three_rate = 1
  if pity5 > 62:
    five_rate = -0.004107762368*pity5**4 + 159998.677
  if pity4 > 7:
    four_rate = five_rate - (6000 + (pity4 - 7)*46650)
  five_rate_up = 1/4*(100001 - five_rate) + five_rate
  four_rate_up = 1/4*(five_rate - four_rate) + four_rate
  if five_rate_up <= result or five_rate <= result and result < five_rate_up and (guarantee5 == 1 or fp == 2):
    if fp < 2:
      weapon = random.choice(weapons["epitomized_choice"])
    else:
      weapon = epitomized_path
    if weapon == epitomized_path:
      fp = 0
    else:
      fp += 1
    pity4 += 1
    pity5 = 0
    guarantee5 = 0
    star = ":star::star::star::star::star:"
  elif five_rate <= result and result < five_rate_up and fp < 2:
    weapon = random.choice(weapons["five_star_nra"])
    pity4 += 1
    pity5 = 0
    guarantee5 = 1
    fp += 1
    star = ":star::star::star::star::star:"
  elif four_rate_up <= result and result < five_rate or four_rate <= result and result < four_rate_up and guarantee4 == 1 and guarantee5 != 1:
    weapon = random.choice(weapons["four_star_ra"])
    pity4 = 0
    pity5 += 1
    guarantee4 = 0
    star = ":star::star::star::star:"
  elif four_rate <= result and result < four_rate_up:
    weapon = random.choice(weapons["four_star_nra"])
    pity4 = 0
    pity5 += 1
    guarantee4 = 1
    star = ":star::star::star::star:"
  elif three_rate <= result and result < four_rate:
    weapon = random.choice(weapons["three_star"])
    pity4 += 1
    pity5 += 1
    star = ":star::star::star:"
  return [weapon, pity4, pity5, guarantee4, guarantee5, fp, star]


class Gacha(commands.Cog):
  def __init__(self, bot):
    self.bot = bot


  @commands.command()
  async def set(self, ctx, pity4, pity5, guarantee4, guarantee5, fp):
    name = str(ctx.message.author)
    c.execute("""UPDATE pity SET pity4 = :pity4, pity5 = :pity5, guarantee4 = :guarantee4, guarantee5 = :guarantee5, fp = :fp
            WHERE name = :name""", {'name':name, 'pity4':pity4, 'pity5':pity5, 'guarantee4':guarantee4, 'guarantee5':guarantee5, 'fp':fp})
    c.execute("SELECT * FROM pity WHERE name = :name", {'name':name})
    user = c.fetchall()[0]
    pity4 = str(user[1])
    pity5 = str(user[2])
    guarantee4 = str(user[3])
    guarantee5 = str(user[4])
    fp = str(user[5])
    epitomized_path = user[7]
    await ctx.send(f"pity 4: {pity4}\npity 5: {pity5}\nguarantee 4: {guarantee4}\nguarantee 5: {guarantee5}\nfp: {fp}\nepitomized path: {epitomized_path}")


  @commands.command()
  async def pity(self, ctx):
    name = str(ctx.message.author)
    c.execute("SELECT * FROM pity WHERE name = :name", {'name':name})
    try:
      user = c.fetchall()[0]
      pity4 = str(user[1])
      pity5 = str(user[2])
      guarantee4 = str(user[3])
      guarantee5 = str(user[4])
      fp = str(user[5])
      epitomized_path = user[7]
      await ctx.send(f"pity 4: {pity4}\npity 5: {pity5}\nguarantee 4: {guarantee4}\nguarantee 5: {guarantee5}\nfp: {fp}\nepitomized path: {epitomized_path}")
    except IndexError:
      await ctx.send("You need to create an account using the following format: !create [username]")


  @commands.command()
  async def pull(self, ctx, amount = 1):
    name = str(ctx.message.author)
    c.execute("SELECT * FROM pity WHERE name = :name", {'name':name})
    try:
      user = c.fetchall()[0]
      pity4 = user[1]
      pity5 = user[2]
      guarantee4 = user[3]
      guarantee5 = user[4]
      fp = user[5]
      epitomized_path = user[6]
      if amount == 1:
        result = random.randint(1, 100000)
        weapon_result = roll(result, pity4, pity5, guarantee4, guarantee5, fp, epitomized_path)
        await ctx.channel.send(f"u got {weapon_result[6]}", file=discord.File(weapon_result[0]))
      elif amount == 10:
        for i in range(0, 10):
          result = random.randint(1, 100000)
          weapon_result = roll(result, pity4, pity5, guarantee4, guarantee5, fp, epitomized_path)
          pity4 = weapon_result[1]
          pity5 = weapon_result[2]
          guarantee4 = weapon_result[3]
          guarantee5 = weapon_result[4]
          fp = weapon_result[5]
          await ctx.channel.send(f"u got {weapon_result[6]}", file=discord.File(weapon_result[0]))
          await asyncio.sleep(0.5)
      c.execute("""UPDATE pity SET pity4 = :pity4, pity5 = :pity5, guarantee4 = :guarantee4, guarantee5 = :guarantee5, fp = :fp
            WHERE name = :name""", {'name':name, 'pity4':weapon_result[1], 'pity5':weapon_result[2], 'guarantee4':weapon_result[3], 'guarantee5':weapon_result[4], 'fp':weapon_result[5]})
      conn.commit()
    except IndexError:
      await ctx.send("You need to create an account using the following format: !create [username]")
  

  @commands.command()
  async def ep(self, ctx, path = 0):
    try:
      name = str(ctx.message.author)
      c.execute("SELECT * FROM pity WHERE name = :name", {'name':name})
      path1 = "weapons/epipath1.png"
      path2 = "weapons/epipath2.png"
      if path == 0:
        await ctx.send("pick ur shit\n", file=discord.File("weapons/epipat.png"))
      elif path == 1:
        await ctx.send(f"u picked\n", file=discord.File(path1))
        c.execute("""UPDATE pity SET fp = :fp, epitomized_path = :epitomized_path, epitomized_weapon = :epitomized_weapon
            WHERE name = :name""", {'name':name, 'fp':0, 'epitomized_path':weapons["epitomized_choice"][0], 'epitomized_weapon':epitomized_weapon[0]})
        conn.commit()
      elif path == 2:
        await ctx.send(f"u picked\n", file=discord.File(path2))
        c.execute("""UPDATE pity SET fp = :fp, epitomized_path = :epitomized_path, epitomized_weapon = :epitomized_weapon
            WHERE name = :name""", {'name':name, 'fp':0, 'epitomized_path':weapons["epitomized_choice"][1], 'epitomized_weapon':epitomized_weapon[1]})
        conn.commit()
      else:
        await ctx.send("fuck you")
        
    except Exception as e:
      print(e)


def setup(bot):
  bot.add_cog(Gacha(bot))
  print('Gacha is loaded')