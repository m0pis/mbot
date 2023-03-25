import discord
from discord.ext import commands
import time
import random
import requests
from bs4 import BeautifulSoup
#from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")
'''
@client.event
async def on_message(message):
    if message.author == client.user:
       return

    try:
        if str(target_user_id) in message.content:
            response = "КУДА ТЭГАЕШЬ УЕБОК"
            await message.channel.send(response)
    except Exception as e:
        print(f"Error occurred: {e}")
'''

@client.command()
async def runit(ctx):
    await ctx.send("Чтобы запустить эту команду, введите пароль.")

@client.command()
async def delete(ctx):
    await ctx.message.delete()
    async for message in ctx.channel.history():
        if message.author == client.user or message.content.startswith('!'):
            time.sleep(0.3)
            await message.delete()

@client.command()
async def porno(ctx):
    await ctx.send("https://goo.su/WZQ3")

@client.command()
async def ilovenephentus(ctx):
    with open('image.png', 'rb') as f:
            picture = discord.File(f)
            await ctx.reply(file=picture)

@client.command()
async def helps(ctx):
    await ctx.send("!delete, !runit, !porno, !tictactoe @tag @tag, !artemkto, !ilovenephentus, !cringe")

@client.command()
async def artemkto(ctx):
    await ctx.send("Пидрила, конечно же")

@client.command()
async def lightshot(ctx):
    random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))

    image_url = f"https://prnt.sc/{random_string}"

    await ctx.send(image_url)

@client.command()
async def cringe(ctx):
    emojis = ["🟦", "❌", "👍", "😂", "😢"]
    current_emoji_index = 0 # индекс текущей отправленной эмодзи
    square_message = await ctx.send(emojis[current_emoji_index]) # отправляем начальную эмодзи
    for emoji in emojis[1:]:
        await square_message.add_reaction(emoji) # добавляем остальные эмодзи на сообщение с квадратом
    
    @client.event
    async def on_reaction_add(reaction, user):
        nonlocal current_emoji_index # делаем переменную current_emoji_index доступной внутри функции
        if user == client.user: # проверяем, что реакцию добавил наш бот
            return
        if reaction.message.content in emojis: # проверяем, что реакция была добавлена к сообщению с квадратом
            # находим индекс выбранной пользователем эмодзи в списке эмодзи
            index = emojis.index(str(reaction.emoji))
            if index != current_emoji_index: # если выбранная пользователем эмодзи отличается от текущей
                current_emoji_index = index # обновляем текущую эмодзи
                new_square = emojis[current_emoji_index]
                await reaction.message.edit(content=new_square)

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !tictactoe command.")

def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")

#target_user_id = "275492125833953282"

@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author == client.user:
        return

    if message.content.startswith('!'):
        return

    # здесь указываем ID пользователя, за которым будем следить
    if '<@275492125833953282>' in message.content:
        await message.channel.send('КУДА ТЭГАЕШЬ УЕБОК')

    if not message.author.bot and message.author.id == 276257943593418753:
        # Отправляем приветственное сообщение пользователю
        await message.channel.reply(f"Иди нахуй, {message.author.name}!")

@client.event
async def on_ready():
   await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='!helps - Команды'))

#keep_alive()

client.run("")
