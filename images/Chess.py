import pygame
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

settings = {
    'token': 'MTA2OTMxNTIzMjk2ODc1MzI3Mg.GL0STd.Epl85UYxnkN20a-jXpXuU6Ri7CoWipH4V5JBLQ',
    'bot': 'Goosebot6',
    'id': 1069315232968753272,
    'prefix': '!'
}

size = (720, 720)
pygame.init()
screen = pygame.display.set_mode(size)
background = pygame.image.load("images/chess.jpg")
background = pygame.transform.scale(background, (720, 720))
Wrong_message = None
old_message = None
first_p = None
second_p = None
hod = "белых"
player = 1




@client.event
async def on_message(message):
    global first_p, second_p, Wrong_message, player, hod
    if message.author == client.user:
        return
    if message.content == 'start':
        await message.channel.send("Первый игрок, напишите в чат цифру 1")
        return
    if message.content == "1":
        first_p = message.author
        await message.channel.send("Второй игрок, напишите в чат цифру 2")
        return
    if message.content == "2":
        if message.author != first_p:
            second_p = message.author
            await update_screen(message, is_start=True)
            await message.channel.send(f"Ходит игрок номер {player} за {hod}")
            return
        else:
            await message.channel.send("Вы не можете играть сами с собой!")
            return
    else:

        old_cords = message.content[find_nth(message.content, " ", 2) + 1:find_nth(message.content, " ", 3)].split(",")
        new_cords = message.content[find_nth(message.content, " ", 3):len(message.content)].split(",")
        old_cords_x = int(old_cords[0]) - 1
        old_cords_y = int(old_cords[1]) - 1
        new_cords_x = int(new_cords[0]) - 1
        new_cords_y = int(new_cords[1]) - 1
        print(player)
        if (first_p == message.author) and ("б" in chess_table[old_cords_x][old_cords_y]) and (player == 1):
            if chess_table[old_cords_x][old_cords_y] == "бп":
                if old_cords_x == new_cords_x and old_cords_y - new_cords_y == 1:
                    await hodi(new_cords_x, new_cords_y,old_cords_x,old_cords_y, message,"чёрных", 2)







        elif (second_p == message.author) and ("ч" in chess_table[old_cords_x][old_cords_y]) and (player == 2) :
            chess_table[new_cords_x][new_cords_y] = chess_table[old_cords_x][old_cords_y]
            chess_table[old_cords_x][old_cords_y] = ""
            print(old_cords)
            await update_screen(message, is_start=False)
            hod = "белых"
            player = 1
            await message.channel.send(f"Ходит игрок номер {player} за {hod}")
        else:

            Wrong_message = await message.channel.send("Так нельзя!")

            await message.delete()


def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start + len(needle))
        n -= 1
    return start


class Figure(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.rect = self.image.get_rect(center=(x + 75, y + 75))
        self.rect.x = x + 75
        self.rect.y = y + 75


chess_table = [
    ["чл", "чк", "чс", "чk", "чq", "чс", "чк", "чл"],
    ["чп", "чп", "чп", "чп", "чп", "чп", "чп", "чп"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["бп", "бп", "бп", "бп", "бп", "бп", "бп", "бп"],
    ["бл", "бк", "бс", "бk", "бq", "бс", "бк", "бл"]
]


async def update_screen(message, is_start=True):
    global old_message, Wrong_message
    screen.blit(background, (0, 0))
    for i in range(len(chess_table)):
        for j in range(len(chess_table[i])):
            if chess_table[i][j] != "":
                figure = Figure(j * 80, i * 80, "images/" + chess_table[i][j] + ".png")
                screen.blit(figure.image, figure.rect)
    pygame.display.flip()
    pygame.image.save(screen, "screen.jpeg")
    if (is_start == True):
        old_message = await message.channel.send(file=discord.File("screen.jpeg"))
    else:

        await old_message.delete()

        old_message = await message.channel.send(file=discord.File("screen.jpeg"))
        await message.delete()
        if Wrong_message != None:
            await Wrong_message.delete()
            Wrong_message = None

async def hodi(new_cords_x, new_cords_y,old_cords_x,old_cords_y, message,new_hod,new_player):
    global hod, player
    chess_table[new_cords_x][new_cords_y] = chess_table[old_cords_x][old_cords_y]
    chess_table[old_cords_x][old_cords_y] = ""

    await update_screen(message, is_start=False)

    hod = new_hod
    player = new_player
    await message.channel.send(f"Ходит игрок номер {player} за {hod}")


client.run(settings['token'])
