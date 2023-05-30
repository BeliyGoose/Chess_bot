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
hod_bk = False
hod_wk = False
hod_bll = False
hod_wll = False
hod_brl = False
hod_wrl = False
was_shah_before = False
blocked_figure = ""

chess_table = [
    ["чл",  "", "чс", "чk", "чq", "чс", "чк", "чл"],
    ["чп", "бп", "чп", "чп", "чп", "чп", "", "чп"],
    ["",    "",   "",   "",   "",   "",   "",   ""],
    ["бс",  "",   "",   "",   "",   "",   "",   ""],
    ["",    "",   "",   "",   "",   "",   "",   ""],
    ["",    "",   "",   "",   "",   "",   "",   ""],
    ["бп", "бп", "бп", "бп", "бп", "бп", "чп", "бп"],
    ["бл", "бк", "бс", "бq", "бk", "бс", "", "бл"]
]

chess_table1 = [
    ["чл", "чк", "чс", "чq", "чk", "чс", "чк", "чл"],
    ["чп", "чп", "чп", "чп", "чп", "чп", "чп", "чп"],
    ["",    "",   "",   "",   "",   "",   "",   ""],
    ["",    "",   "",   "",   "",   "",   "",   ""],
    ["",    "",   "",   "",   "",   "",   "",   ""],
    ["",    "",   "",   "",   "",   "",   "",   ""],
    ["бп", "бп", "бп", "бп", "бп", "бп", "бп", "бп"],
    ["бл", "бк", "бс", "бq", "бk", "бс", "бк", "бл"]
]

class Figure(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.rect = self.image.get_rect(center=(x + 75, y + 75))
        self.rect.x = x + 75
        self.rect.y = y + 75
