import random
import discord
import pygame
from discord.ext import commands

intents = discord.Intents().all()
client = discord.Client(intents=intents)
settings = {
    'token': 'MTA2MzQ2OTM3MDU3NzI2NDc1Mg.GzdLav.luMJXLCWfW4qGi8E7Nat59RH_0IRxxFamwf4ag',
    'bot': 'Goosebot5',
    'id': 1063469370577264752,
    'prefix': '!'
}

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)

size = (750, 750)
pygame.init()
screen = pygame.display.set_mode(size)
background = pygame.image.load("grass.jpeg")
background = pygame.transform.scale(background, (750, 750))
lose = pygame.image.load("goose_proigral.jpg")
lose = pygame.transform.scale(lose, (750, 750))
pobeda = pygame.image.load("goosewin.jpg")
pobeda = pygame.transform.scale(pobeda, (750, 750))
potatos = 0
number_of_beet = 0
game_end = False
speed = 50
old_message = None


class Person(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("goose_PNG10.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect(center=(x, y))
        self.rect.x = x
        self.rect.y = y


person = Person(15, 15)


@bot.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == 'start':
        await update_screen(message, is_start=True)
    if message.content == 'left':
        person.rect.x -= speed
        await update_screen(message)
    if message.content == 'right':
        person.rect.x += speed
        await update_screen(message)
    if message.content == 'up':
        person.rect.y -= speed
        await update_screen(message)
    if message.content == 'down':
        person.rect.y += speed
        await update_screen(message)


class Farmer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("farmer.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect(center=(x, y))
        self.rect.x = x
        self.rect.y = y


farmer = Farmer(random.randint(50, 700), random.randint(50, 700))
farmer2 = Farmer(random.randint(50, 700), random.randint(50, 700))


class Potato(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("potato.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect(center=(x, y))
        self.rect.x = x
        self.rect.y = y


potato1 = Potato(250, 50)


class beet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("beet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect(center=(x, y))
        self.rect.x = x
        self.rect.y = y


beet1 = beet(250, 100)


async def update_screen(message, is_start=False):
    global old_message
    global game_end
    global potatos
    global number_of_beet
    if game_end == True:
        return
    screen.blit(background, (0, 0))
    screen.blit(person.image, (person.rect.x, person.rect.y))
    screen.blit(farmer.image, farmer.rect)
    screen.blit(farmer2.image, farmer2.rect)
    if person.rect.colliderect(farmer.rect):
        screen.blit(lose, (0, 0))
        game_end = True
    if person.rect.colliderect(farmer2.rect):
        screen.blit(lose, (0, 0))
        game_end = True
    if person.rect.colliderect(potato1.rect):
        potato1.rect.x = random.randint(100, 650)
        potato1.rect.y = random.randint(100, 650)
        potatos += 1
    if person.rect.colliderect(beet1.rect):
        beet1.rect.x = random.randint(100, 650)
        beet1.rect.y = random.randint(100, 650)
        number_of_beet += 1
    if number_of_beet == 1 and potatos == 2:
        screen.blit(pobeda, (0, 0))
        game_end = True
    if number_of_beet > 1 or potatos > 2:
        number_of_beet = 0
        potatos = 0
    if not game_end:
        screen.blit(potato1.image, potato1.rect)
        screen.blit(beet1.image, beet1.rect)
        pygame.font.init()
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render(f'Potatos: {potatos} Beet: {number_of_beet}', False, (255, 255, 255))
        screen.blit(text_surface, (10, 10))
    pygame.display.flip()
    pygame.image.save(screen, "screen.jpeg")
    if (is_start == True):
        old_message = await message.channel.send(file=discord.File("screen.jpeg"))
    else:

        await old_message.delete()

        old_message = await message.channel.send(file=discord.File("screen.jpeg"))
        await message.delete()

bot.run(settings['token'])