from keepalive import keep_alive
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import os
import random
import sys
import sqlite3

client = commands.Bot(command_prefix='t!')
conn2 = sqlite3.connect("banned.db")
c2 = conn2.cursor()
try:
  c2.execute("SELECT * FROM banned")
except Exception as e:
  print(e)
db_banned = c2.fetchall()
banned = [db_banned[i][0] for i in range(len(db_banned))]
print(banned)
conn2.close()

swear = [
    'địt', 'đjt', 'dit', 'djt', 'đm', 'dm', 'dcm', 'đcm', 'đụ', 'duma', 'dmm',
    'đmm', 'lồn', 'loz', 'lon', 'loonf', 'lz', 'cặc', 'cc', 'buồi', 'đb', 'db',
    'buoi', 'fuck', 'fck', 'cunt', 'dick', 'cock', 'nigga', 'nigger', 'shit'
]

memeball = [
    "It is certain.", "It is decidedly so.", "Without a doubt.",
    "Yes definitely.", "You may rely on it.", "As I see it, yes.",
    "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
    "Don't count on it.", "My reply is no.", "My sources say no.",
    "Outlook not so good.", "Very doubtful.", "có cái lồn", "con cặc", "đéo",
    "mơ đi con gà", "hỏi cái lồn à?", "hỏi đéo gì?", "tự đi mà tìm",
    "google đi thằng óc chó", "địt mẹ hỏi lắm thế", "cút", "im mồm", "im",
    "ngậm mồm", "lalalalalala đéo nghe thấy gì cả", "haha thằng ngu",
    "<:weirdchamp:980500442968645663>", "tạch là cái chắc", "tạch rồi con",
    "tạch chắc rồi cu", "mõm", "sủa tiếp đi con", "tư duy đi",
    "svbk có nên hỏi câu đấy không", "não đâu mà hỏi thế", "đéo quan tâm",
    "mày là kĩ sư bk hay mày là con bò"
]

# banned = [
#     "mù", "tạch", "đáy xh", "mu chu", "day xh", "mu' chữ"
# ]
banned = banned + [f"n{i}" for i in range(6, 500)]


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    print('Load successfully')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    print('Unload successfully')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    print('Reload successfully')


@client.event
async def on_ready():
    print('ready as {0.user}'.format(client))


initial_extensions = [
    'cogs.reacts', 'cogs.compare', 'cogs.hangman', 'cogs.wordle'
]

if __name__ == "__main__":
    for extension in initial_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}', file=sys.stderr)
            print(e)


@client.command()
async def add(ctx, *args):
    word = ' '.join(locals()['args'])
    global banned
    print(word)
    if ctx.message.author.name == 'helium':
      conn2 = sqlite3.connect("banned.db")
      c2 = conn2.cursor()
      c2.execute("INSERT INTO banned VALUES (:words)", {'words':word})
      banned.append(word)
      conn2.commit()
      conn2.close()


async def roll(ctx, max=100):
    rand = random.randint(1, int(max))
    await ctx.send(f"{ctx.author.mention} rolled {rand} point(s)")


@client.command()
async def ball(ctx):
    await ctx.send(random.choice(memeball))


@client.command()
async def avatar(ctx, *, avamember: discord.Member = None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)


@client.command()
async def handou(ctx):
    await ctx.send(
        "打倒共産党 Đả đảo Đảng Cộng sản 犬共産 犬政権 独裁政権 Độc tài 自由 Tự do 独立 Dân chủ 多党制 Chế độ đa đảng 越南共和国 Việt Nam Cộng Hoà 越南更新革命党 越新 Việt Tân Việt Nam Canh tân Cách mạng Đảng VNRP 人文佳品 Nhân văn giai phẩm 千九百六十八 戊申順化虐殺 Thảm sát Huế Mậu Thân 1968 千九百七十六 柬埔寨侵略 Xâm lược Campuchia 1976 同心事件 Vụ án Đồng Tâm 台塑河静 Formosa Vũng Áng 2019冠状病毒病 Đại dịch COVID-19 民権 民主 自由言論 思想 反共 反革命 反動 暴乱 温和表情 Trọng lú Phúc ngoẻo 汚職 貪污 和平演変"
    )


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error


@client.event
async def on_message(message):
    global msg
    # conn1 = sqlite3.connect("accounts.db")
    # c1 = conn1.cursor()
    msg = message.content.lower().split(' ')
    print(message.content)
    roulette = random.randint(0, 2500)
    print(message.author)
    # if 'Admin ☜(⌒▽⌒)☞' != message.author.roles[-1].name:
    #   if roulette == 0:
    #     await message.author.kick()
    #     await message.channel.send(f'{message.author} đã bị kick vì tạch roulette')
    # print(f'{message.author.id}, {message.author}')
    # print(message.author.roles[-1].name)
    # for word in banned:
    #     if word in message.content:
    #         c1.execute("SELECT * FROM users WHERE name = :name",
    #                   {'name': str(message.author)})
    #         mom = c1.fetchall()[0][1]
    #         if mom < 5:
    #             await message.channel.send(f"mõm {5-mom} lần nữa ăn ban")
    #             c1.execute(
    #                 """UPDATE users SET mom = :mom
    #           WHERE name = :name""", {
    #                     'name': str(message.author),
    #                     'mom': mom + 1
    #                 })
    #             break
    #         if mom >= 5:
    #             await message.channel.send(
    #                 f"{message.author} đã mõm 5 lần và sẽ ăn ban")
    #             c1.execute(
    #                 """UPDATE users SET mom = :mom
    #           WHERE name = :name""", {
    #                     'name': str(message.author),
    #                     'mom': 0
    #                 })
    #             await message.author.kick()
    #             break
    # conn1.commit()
    # conn1.close()

  
    if 'Admin ☜(⌒▽⌒)☞' != message.author.roles[-1].name:
        if ('😏' in message.content) or ('😼' in message.content):
            await message.author.kick(reason="nhếch nữa đi cu")
            await message.channel.send("này thì nhếch")
    # if message.author.id == 701269996700958762 and ("lồn" in msg):
    #     await message.author.kick()
    #     await message.channel.send("ngu thì chịu")
    if '727' in msg:
        await message.channel.send("wysi")
    # if ('liêm' in msg) or ('Liêm' in msg) or ("liem" in msg) or ("Liem" in msg) and not message.author.bot:
    #   await message.channel.send("Liem cai dau buoi tao nay cho an ban bay gio")
    for word in msg:
        if word in swear and message.channel.id == 947153310681534504:
            await message.channel.send(
                "thằng này mày ăn gan hùm hay sao mà mày dám chửi bậy trước mặt tao"
            )
    await client.process_commands(message)


keep_alive()

client.run(os.environ['TOKEN'])
