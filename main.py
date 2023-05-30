import re

import pygame
import discord
from discord.ext import commands
from Dannie_Goose import *




async def proverka_color(old_cords_x,old_cords_y, message,color):
    global Wrong_message
    if chess_table[old_cords_x][old_cords_y][0] == color[0]:
        Wrong_message = await message.channel.send("Так нельзя!")
        await message.delete()
        return True
    else:
        return False

async def rokirovka(hod_ladyi, hod_king, cord_x, cord_y_l, cord_y_k, message):
    global player, hod
    if hod_ladyi != True and hod_king != True:
        is_collide = False
        for i in range (min(cord_y_l, cord_y_k)+1, max(cord_y_l, cord_y_k)):
            if chess_table[cord_x][i] != "":
                is_collide = True
        print(is_collide)
        if is_collide == False:
            if cord_y_l == 0:
                chess_table[cord_x][2] = hod[0] + "k"
                chess_table[cord_x][4] = ""
                chess_table[cord_x][3] = hod[0] + "л"
                chess_table[cord_x][0] = ""
            if cord_y_l == 7:
                chess_table[cord_x][6] = hod[0] + "k"
                chess_table[cord_x][4] = ""
                chess_table[cord_x][5] = hod[0] + "л"
                chess_table[cord_x][7] = ""
            if player == 1:
                player = 2
                hod = "чёрных"
            else:
                player = 1
                hod = "белых"
            await update_screen(message, is_start=False)
            await message.channel.send(f"Ходит игрок номер {player} за {hod}")
    else:
        await message.channel.send("Вы не можте сделать рокировку")

async def mat(message,k_x, k_y, king_name, enemy_name, enemy_x, enemy_y):
    global blocked_figure, chess_table, chess_table1
    for kx in range(-1, 2):
        for ky in range(-1,2):
            if k_x + kx >= 0 and k_y + ky >= 0:
                if chess_table[k_x + kx][k_y +ky] == "":
                    chess_table[k_x][k_y - 1] = king_name
                    chess_table[k_x][k_y] = ""
                    if shah(message,False) == None:
                        chess_table[k_x + kx][k_y +ky] = ""
                        chess_table[k_x][k_y] = king_name
                        blocked_figure = ""
                        return
                    else:
                        chess_table[k_x + kx][k_y +ky] = ""
                        chess_table[k_x][k_y] = king_name
                        blocked_figure = king_name
    for x in range(8):
        for y in range(8):
            if chesstable[x][y][0] == king_name[0]:
                if chesstable[x][y] == "бп":
                    if enemy_x - x == -1 and abs(enemy_y - y) == 1:
                        return
                if chesstable[x][y] == "чп":
                    if enemy_x - x == 1 and abs(enemy_y - y) == 1:
                        return
                if chesstable[x][y] == "л":
                    if hod_ladyi(enemy_x,x,enemy_y, y, message, chess_table[x][y][0],0) == True:
                        return
                if chesstable[x][y] == "к":
                    if hod_konya(enemy_x,x,enemy_y, y, message, chess_table[x][y][0],0) == True:
                        return
                if chesstable[x][y] == "c":
                    if hod_slona(enemy_x,x,enemy_y, y, message, chess_table[x][y][0],0) == True:
                        return
                if chesstable[x][y] == "q":
                    if hod_korolevi(enemy_x,x,enemy_y, y, message, chess_table[x][y][0],0) == True:
                        return
    if enemy_name[1] == "л" or enemy_x[1] == "q":
        if enemy_y - k_y == 0:
            for needed_x in range(min(k_x, enemy_x) + 1, max(k_x, enemy_x)):
                for x in range(8):
                    for y in range(8):
                        if chesstable[x][y][0] == king_name[0]:
                            if chesstable[x][y] == "л":
                                if hod_ladyi(needed_x, x, enemy_y, y, message, chess_table[x][y][0], 0) == True:
                                        return
                            if chesstable[x][y] == "к":
                                if hod_konya(needed_x, x, enemy_y, y, message, chess_table[x][y][0], 0) == True:
                                        return
                            if chesstable[x][y] == "c":
                                if hod_slona(needed_x, x, enemy_y, y, message, chess_table[x][y][0], 0) == True:
                                        return
                            if chesstable[x][y] == "q":
                                if hod_korolevi(needed_x, x, enemy_y, y, message, chess_table[x][y][0], 0) == True:
                                        return
        if enemy_x - k_x == 0:
            for needed_y in range(min(k_y, enemy_y) + 1, max(k_y, enemy_y)):
                for x in range(8):
                    for y in range(8):
                        if chesstable[x][y][0] == king_name[0]:
                            if chesstable[x][y] == "л":
                                if hod_ladyi(enemy_x, x, needed_y, y, message, chess_table[x][y][0], 0) == True:
                                    return
                            if chesstable[x][y] == "к":
                                if hod_konya(enemy_x, x, needed_y, y, message, chess_table[x][y][0], 0) == True:
                                    return
                            if chesstable[x][y] == "c":
                                if hod_slona(enemy_x, x, needed_y, y, message, chess_table[x][y][0], 0) == True:
                                    return
                            if chesstable[x][y] == "q":
                                if hod_korolevi(enemy_y, x, needed_y, y, message, chess_table[x][y][0], 0) == True:
                                    return

    if enemy_name[1] == "с" or enemy_x[1] == "q":
        min_x = min(k_x, enemy_x)
        max_x = max(k_x, enemy_x)
        min_y = min(k_y, enemy_y)
        max_y = max(k_y, enemy_y)
        for needed_x, needed_y in zip(range(min_x + 1, max_x), range(min_y + 1, max_y)):
            for x in range(8):
                for y in range(8):
                    if chesstable[x][y][0] == king_name[0]:
                        if chesstable[x][y] == "л":
                            if hod_ladyi(needed_x, x, needed_y, y, message, chess_table[x][y][0], 0) == True:
                                    return
                        if chesstable[x][y] == "к":
                                if hod_konya(needed_x, x, needed_y, y, message, chess_table[x][y][0], 0) == True:
                                    return
                        if chesstable[x][y] == "c":
                            if hod_slona(needed_x, x, needed_y, y, message, chess_table[x][y][0], 0) == True:
                                    return
                        if chesstable[x][y] == "q":
                            if hod_korolevi(needed_x, x, needed_y, y, message, chess_table[x][y][0], 0) == True:
                                    return
    if king_name[0] == "ч":
        await message_channel_send("МАТ! Выйграл игрок №1")
        chess_table = chess_table1
    if king_name[0] == "б":
        await message_channel_send("МАТ! Выйграл игрок №2")
    chess_table = chess_table1

async def shah(message, otpravit):
    b_king_x = 0
    b_king_y = 0
    w_king_x = 0
    w_king_y = 0
    for x in range(8):
        for y in range(8):
            if chess_table[x][y] == "чk":
                b_king_x = x
                b_king_y = y
            if chess_table[x][y] == "бk":
                w_king_x = x
                w_king_y = y
    for x in range(8):
        for y in range(8):
            if chess_table[x][y] == "бп" and abs(b_king_x - x) == 1 and abs(b_king_y - y) == 1:
                if otpravit == True:
                    await message.channel.send("шах чёрному королю от белой пешки")
                return "б"

            if chess_table[x][y] == "чп" and abs(w_king_x - x) == 1 and abs(w_king_y - y) == 1:
                if otpravit == True:
                    await message.channel.send("шах белому королю от чёрной пешки")
                return "ч"


            if chess_table[x][y] == "бл" and abs(b_king_x - x) == 0 and abs(b_king_y - y) > 0:
                min_y = min(y, b_king_y)
                max_y = max(y, b_king_y)
                is_collide = False
                for y1 in range(min_y +1, max_y):
                    if chess_table[x][y1] != "":
                        is_collide = True
                if not is_collide:
                    if otpravit == True:
                        await message.channel.send("шах чёрному королю от белой ладьи")
                    return "б"

            if chess_table[x][y] == "бл" and abs(b_king_x - x) > 0 and abs(b_king_y - y) == 0:
                min_x = min(x, b_king_x)
                max_x = max(x, b_king_x)
                is_collide = False
                for x1 in range(min_x + 1, max_x):
                    if chess_table[x1][y] != "":
                        is_collide = True
                if not is_collide:
                    if otpravit == True:
                        await message.channel.send("шах чёрному королю от белой ладьи")
                    return "б"

            if chess_table[x][y] == "чл" and abs(w_king_x - x) == 0 and abs(w_king_y - y) > 0:
                min_y = min(y, w_king_y)
                max_y = max(y, w_king_y)
                is_collide = False
                for y1 in range(min_y + 1, max_y):
                    if chess_table[x][y1] != "":
                        is_collide = True
                if not is_collide:
                    if otpravit == True:
                        await message.channel.send("шах белому королю от чёрной ладьи")
                    return "ч"

            if chess_table[x][y] == "чл" and abs(w_king_x - x) > 0 and abs(w_king_y - y) == 0:
                min_x = min(x, b_king_x)
                max_x = max(x, b_king_x)
                is_collide = False
                for x1 in range(min_x + 1, max_x):
                    if chess_table[x1][y] != "":
                        is_collide = True
                if not is_collide:
                    if otpravit == True:
                        await message.channel.send("шах белому королю от чёрной ладьи")
                    return "ч"

            if chess_table[x][y] == "бк" and abs(b_king_x - x) == 2 and abs(b_king_y - y) == 1:
                if otpravit == True:
                    await message.channel.send("шах чёрному королю от белого коня")
                return "б"

            if chess_table[x][y] == "бк" and abs(b_king_x - x) == 1 and abs(b_king_y - y) == 2:
                if otpravit == True:
                    await message.channel.send("шах чёрному королю от белого коня")
                return "б"
            if chess_table[x][y] == "чк" and abs(w_king_x - x) == 2 and abs(w_king_y - y) == 1:
                if otpravit == True:
                    await message.channel.send("шах чёрному королю от белого коня")
                return "ч"

            if chess_table[x][y] == "чк" and abs(w_king_x - x) == 1 and abs(w_king_y - y) == 2:
                if otpravit == True:
                    await message.channel.send("шах чёрному королю от белого коня")
                return "ч"

            if chess_table[x][y] == "чс" and abs(w_king_x - x) == abs(w_king_y - y):
                min_x = min(x, w_king_x)
                max_x = max(x, w_king_x)
                min_y = min(y, w_king_y)
                max_y = max(y, w_king_y)
                is_collide = False
                if (b_king_x - x > 0 and b_king_y - y < 0) or (b_king_x - x < 0 and b_king_y - y > 0):
                    for x1, y1 in zip(range(min_x + 1, max_x), range(max_y - 1, min_y, - 1)):
                        if chess_table[x1][y1] != "":
                            is_collide = True
                else:
                    for x1, y1 in zip(range(min_x + 1, max_x), range(min_y + 1, max_y)):
                        if chess_table[x1][y1] != "":
                            is_collide = True
                if not is_collide:
                    if otpravit == True:
                        await message.channel.send("шах белому королю от чёрного слона")
                    return "ч"

            if chess_table[x][y] == "бс" and abs(b_king_x - x) == abs(b_king_y - y):
                min_x = min(x, b_king_x)
                max_x = max(x, b_king_x)
                min_y = min(y, b_king_y)
                max_y = max(y, b_king_y)
                is_collide = False
                if (b_king_x - x > 0 and b_king_y - y <0) or (b_king_x - x < 0 and b_king_y - y > 0):
                    for x1, y1 in zip(range(min_x + 1, max_x), range(max_y - 1, min_y, - 1)):
                        if chess_table[x1][y1] != "":
                            is_collide = True
                else:
                    for x1, y1 in zip(range(min_x + 1, max_x), range(min_y + 1, max_y)):
                        if chess_table[x1][y1] != "":
                            is_collide = True
                if not is_collide:
                    if otpravit == True:
                        await message.channel.send("шах чёрному королю от белого слона")
                    return "б"

            if chess_table[x][y] == "бq" and abs(b_king_x - x) == abs(b_king_y - y):
                min_x = min(x, b_king_x)
                max_x = max(x, b_king_x)
                min_y = min(y, b_king_y)
                max_y = max(y, b_king_y)

                is_collide = False
                if (b_king_x - x > 0 and b_king_y - y <0) or (b_king_x - x < 0 and b_king_y - y > 0):
                    for x1, y1 in zip(range(min_x + 1, max_x), range(max_y - 1, min_y, - 1)):
                        if chess_table[x1][y1] != "":
                            is_collide = True
                else:
                    for x1, y1 in zip(range(min_x + 1, max_x), range(min_y + 1, max_y)):
                        if chess_table[x1][y1] != "":
                            is_collide = True

                if not is_collide:
                    if otpravit == True:
                        await message.channel.send("шах чёрному королю от белой королевы")
                    return "б"

            if chess_table[x][y] == "бq" and abs(b_king_x - x) == 0 and abs(b_king_y - y) > 0:
                min_y = min(y, b_king_y)
                max_y = max(y, b_king_y)
                is_collide = False
                for y1 in range(min_y + 1, max_y):
                    if chess_table[x][y1] != "":
                        is_collide = True
                if not is_collide:
                    if otpravit == True:
                        await message.channel.send("шах чёрному королю от белой королевы")
                    return "б"

            if chess_table[x][y] == "бq" and abs(b_king_x - x) > 0 and abs(b_king_y - y) == 0:
                min_x = min(x, b_king_x)
                max_x = max(x, b_king_x)
                is_collide = False
                for x1 in range(min_x + 1, max_x):
                    if chess_table[x1][y] != "":
                        is_collide = True
                if not is_collide:
                    if otpravit == True:
                        await message.channel.send("шах чёрному королю от белой королевы")
                    return "б"

            if chess_table[x][y] == "чq" and abs(w_king_x - x) == 0 and abs(w_king_y - y) > 0:
                min_y = min(y, w_king_y)
                max_y = max(y, w_king_y)
                is_collide = False
                for y1 in range(min_y + 1, max_y):
                    if chess_table[x][y1] != "":
                        is_collide = True
                if not is_collide:
                    if otpravit == True:
                        await message.channel.send("шах белому королю от чёрной королевы")
                    return "ч"

            if chess_table[x][y] == "чq" and abs(w_king_x - x) > 0 and abs(w_king_y - y) == 0:
                min_x = min(x, w_king_x)
                max_x = max(x, w_king_x)
                is_collide = False
                for x1 in range(min_x + 1, max_x):
                    if chess_table[x1][y] != "":
                        is_collide = True
                if not is_collide:
                    if otpravit == True:
                        await message.channel.send("шах белому королю от чёрной королевы")
                    return "ч"

            if chess_table[x][y] == "чq" and abs(w_king_x - x) == abs(w_king_y - y):
                min_x = min(x, w_king_x)
                max_x = max(x, w_king_x)
                min_y = min(y, w_king_y)
                max_y = max(y, w_king_y)
                is_collide = False
                if (b_king_x - x > 0 and b_king_y - y < 0) or (b_king_x - x < 0 and b_king_y - y > 0):
                    for x1, y1 in zip(range(min_x + 1, max_x), range(max_y - 1, min_y, - 1)):
                        if chess_table[x1][y1] != "":
                            is_collide = True
                        print(chess_table[x1][y1])
                else:
                    for x1, y1 in zip(range(min_x + 1, max_x), range(min_y + 1, max_y)):
                        if chess_table[x1][y1] != "":
                            is_collide = True
                        print(chess_table[x1][y1])
                if not is_collide:
                    if otpravit == True:
                        await message.channel.send("шах белому королю от чёрной королевы")
                    return "ч"

async def hod_korolya(new_cords_x,old_cords_x,new_cords_y, old_cords_y, message, color, number_of_player):
    global Wrong_message, hod_bk, hod_wk
    if chess_table[old_cords_x][old_cords_y] == blocked_figure:
        await message.channel.send("Вы не можете пойти королём")
        await message.delete()
        return
    if await proverka_color(old_cords_x,old_cords_y, message,color):
        return
    if abs(old_cords_y - new_cords_y) <= 1 and abs(old_cords_x - new_cords_x) <= 1:
        await hodi(new_cords_x, new_cords_y, old_cords_x, old_cords_y, message,color, number_of_player)
        if color[0] == "ч":
            hod_bk = True
        else:
            hod_wk = True
    else:
        Wrong_message = await message.channel.send("Так нельзя!")
        await message.delete()

async def hod_korolevi(new_cords_x,old_cords_x,new_cords_y, old_cords_y, message, color, number_of_player):
    global Wrong_message
    if await proverka_color(old_cords_x,old_cords_y, message,color):
        return
    if abs(new_cords_x - old_cords_x) == abs(new_cords_y - old_cords_y):
        min_x = min(old_cords_x, new_cords_x)
        max_x = max(old_cords_x, new_cords_x)
        min_y = min(old_cords_y, new_cords_y)
        max_y = max(old_cords_y, new_cords_y)
        IsColide = True
        for x, y in zip(range(min_x + 1, max_x), range(min_y + 1, max_y)):
            if chess_table[x][y] != "":
                IsColide = False
        if chess_table[new_cords_x][new_cords_y] != "":
            if IsColide == True and color[0] == chess_table[new_cords_x][new_cords_y][0]:
                if number_of_player == 0:
                    return True
                await hodi(new_cords_x, new_cords_y, old_cords_x, old_cords_y, message, color, number_of_player)
            else:
                Wrong_message = await message.channel.send("Так нельзя, на пути стоит преграда!")
                await message.delete()
        else:
            await hodi(new_cords_x, new_cords_y, old_cords_x, old_cords_y, message, color, number_of_player)
    elif old_cords_y == new_cords_y and old_cords_x - new_cords_x != 0:
        is_collide = False
        for i in range(min(old_cords_x, new_cords_x)+1, max(old_cords_x, new_cords_x)):
            if chess_table[i][new_cords_y] != "":
                is_collide = True
        if is_collide == False:
            await hodi(new_cords_x, new_cords_y, old_cords_x, old_cords_y, message, color, number_of_player)
        else:
            Wrong_message = await message.channel.send("Так нельзя!")
            await message.delete()
    elif old_cords_y != new_cords_y and old_cords_x == new_cords_x:
        is_collide = False
        for i in range(min(old_cords_y, new_cords_y)+1, max(old_cords_y, new_cords_y)):
            if chess_table[new_cords_x][i] != "":
                is_collide = True
        if is_collide == False:
            await hodi(new_cords_x, new_cords_y, old_cords_x, old_cords_y, message, color, number_of_player)
        else:
            Wrong_message = await message.channel.send("Так нельзя!")
            await message.delete()
    else:
        Wrong_message = await message.channel.send("Так нельзя!")
        await message.delete()

async def hod_slona(new_cords_x,old_cords_x,new_cords_y, old_cords_y, message, color, number_of_player):
    global Wrong_message
    if await proverka_color(old_cords_x, old_cords_y, message, color):
        return
    if abs(new_cords_x - old_cords_x) == abs(new_cords_y - old_cords_y):
        x_range = range(old_cords_x + 1, new_cords_x)
        if old_cords_x > new_cords_x:
            x_range = range(old_cords_x - 1, new_cords_x, -1)
        y_range = range(old_cords_y + 1, new_cords_y)
        if old_cords_y > new_cords_y:
            y_range = range(old_cords_y - 1, new_cords_y, -1)
        IsColide = True
        for x, y in zip(x_range, y_range):
            if chess_table[x][y] != "":
                IsColide = False
                print(x,y, chess_table[x][y])
        if chess_table[new_cords_x][new_cords_y] != "":
            print(IsColide)
            if IsColide == True and color[0] == chess_table[new_cords_x][new_cords_y][0]:
                if number_of_player == 0:
                    return True
                await hodi(new_cords_x, new_cords_y, old_cords_x, old_cords_y, message, color, number_of_player)
            else:
                Wrong_message = await message.channel.send("Так нельзя, на пути стоит преграда!")
                await message.delete()
        else:
            await hodi(new_cords_x, new_cords_y, old_cords_x, old_cords_y, message, color, number_of_player)
    else:
        Wrong_message = await message.channel.send("Так нельзя!")
        await message.delete()

async def hod_konya(new_cords_x,old_cords_x,new_cords_y, old_cords_y, message, color, number_of_player):
    global Wrong_message
    if await proverka_color(old_cords_x,old_cords_y, message,color):
        return
    if abs(old_cords_y - new_cords_y) == 1 and abs(old_cords_x - new_cords_x) == 2:
        await hodi(new_cords_x, new_cords_y, old_cords_x, old_cords_y, message, color, number_of_player)
    elif abs(old_cords_y - new_cords_y) == 2 and abs(old_cords_x - new_cords_x) == 1:
        if number_of_player == 0:
            return True
        await hodi(new_cords_x, new_cords_y, old_cords_x, old_cords_y, message, color, number_of_player)
    else:
        Wrong_message = await message.channel.send("Так нельзя!")
        await message.delete()

async def hod_ladyi(new_cords_x,old_cords_x,new_cords_y, old_cords_y, message, color, number_of_player):
    global Wrong_message, hod_bll, hod_brl, hod_wll, hod_wrl
    if await proverka_color(old_cords_x,old_cords_y, message,color):
        return
    if old_cords_y == new_cords_y and old_cords_x - new_cords_x != 0:
        is_collide = False
        for i in range(min(old_cords_x, new_cords_x)+1, max(old_cords_x, new_cords_x)):
            if chess_table[i][new_cords_y] != "":
                is_collide = True
        if is_collide == False:
            if number_of_player == 0:
                return True
            await hodi(new_cords_x, new_cords_y, old_cords_x, old_cords_y, message, color, number_of_player)
            if (old_cords_x == 7 and old_cords_y == 0) and color[0] == "б":
                hod_wll = True
            if (old_cords_x == 7 and old_cords_y == 7) and color[0] == "б":
                hod_wrl = True
            if (old_cords_x == 0 and old_cords_y == 0) and color[0] == "ч":
                hod_bll = True
            if (old_cords_x == 0 and old_cords_y == 7) and color[0] == "ч":
                hod_brl = True


        else:
            Wrong_message = await message.channel.send("Так нельзя!")
            await message.delete()
    elif old_cords_y != new_cords_y and old_cords_x == new_cords_x:
        is_collide = False
        for i in range(min(old_cords_y, new_cords_y)+1, max(old_cords_y, new_cords_y)):
            if chess_table[new_cords_x][i] != "":
                is_collide = True
        if is_collide == False:
            await hodi(new_cords_x, new_cords_y, old_cords_x, old_cords_y, message, color, number_of_player)
        else:
            Wrong_message = await message.channel.send("Так нельзя!")
            await message.delete()
    else:
        Wrong_message = await message.channel.send("Так нельзя!")
        await message.delete()

async def hod_peshki(new_cords_x,old_cords_x,new_cords_y, old_cords_y, message, color, number_of_player):
    global Wrong_message
    if chess_table[new_cords_x][new_cords_y] == "":
        if new_cords_x == 0 and chess_table[old_cords_x][old_cords_y][0] == "б":
            chess_table[old_cords_x][old_cords_y] = "бq"
        if new_cords_x == 7 and chess_table[old_cords_x][old_cords_y][0] == "ч":
            chess_table[old_cords_x][old_cords_y] = "чq"
        await hodi(new_cords_x, new_cords_y, old_cords_x, old_cords_y, message, color, number_of_player )
    else:
        Wrong_message = await message.channel.send("Так нельзя!")
        await message.delete()

@client.event
async def on_message(message):
    global first_p, second_p, Wrong_message, player, hod_wll, hod_wrl, hod_wk, hod, hod_bk, hod_bll, hod_brl, chess_table, chess_table1, chess_table1
    if message.author == client.user:
        return
    if message.content == 'start':
        await message.channel.send("Первый игрок, напишите в чат цифру 1")
        return
    if message.content == 'stop':
        chess_table = chess_table1
        await message.channel.send("Напишие start что бы начать заново")
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


    if message.content == "рокировка левой ладьёй" and player == 1:
        await rokirovka(hod_wll, hod_wk, 7, 0, 4, message)
        hod_wk = True
    elif message.content == "рокировка левой ладьёй" and player == 2:
        await rokirovka(hod_bll, hod_bk, 0, 0, 4, message)
        hod_bk = True

    elif message.content == "рокировка правой ладьёй" and player == 1:
        await rokirovka(hod_wrl, hod_wk, 7, 7, 4, message)
        hod_wk = True
    elif message.content == "рокировка правой ладьёй" and player == 2:
        await rokirovka(hod_brl, hod_bk, 0, 7, 4, message)
        hod_bk = True

    else:
        match = re.search(r'\d{1}[,]\d{1}[ ]\d{1}[,]\d{1}', message.content)
        if match == None:
            Wrong_message = await message.channel.send("Введите правильно!")
            await message.delete()
            return
        cords = match[0].split(" ")
        old_cords_x = int(cords[0][0]) - 1
        old_cords_y = int(cords[0][2]) - 1
        new_cords_x = int(cords[1][0]) - 1
        new_cords_y = int(cords[1][2]) - 1

        if chess_table[new_cords_x][new_cords_y] == "бk" or chess_table[new_cords_x][new_cords_y] == "чk":
            await message.channel.send("Так нельзя!")
            return

        if (first_p == message.author) and ("б" in chess_table[old_cords_x][old_cords_y]) and (player == 1):
            if chess_table[old_cords_x][old_cords_y] == "бп":
                if old_cords_y == new_cords_y and ((old_cords_x - new_cords_x == 1) or (old_cords_x - new_cords_x == 2 and old_cords_x == 6)):
                    await hod_peshki(new_cords_x, old_cords_x, new_cords_y, old_cords_y, message, "чёрных", 2)
                elif (old_cords_x - new_cords_x == 1) and (abs(old_cords_y - new_cords_y) == 1) and (chess_table[new_cords_x][new_cords_y][0] == "ч"):
                    await hodi(new_cords_x, new_cords_y, old_cords_x, old_cords_y, message, "чёрных", 2)
                else:
                    Wrong_message = await message.channel.send("Так нельзя!")
                    await message.delete()

            if chess_table[old_cords_x][old_cords_y] == "бл":
                await hod_ladyi(new_cords_x, old_cords_x, new_cords_y, old_cords_y, message, "чёрных", 2)

            if chess_table[old_cords_x][old_cords_y] == "бк":
                await hod_konya(new_cords_x, old_cords_x, new_cords_y, old_cords_y, message, "чёрных", 2)

            if chess_table[old_cords_x][old_cords_y] == "бс":
                await hod_slona(new_cords_x, old_cords_x, new_cords_y, old_cords_y, message, "чёрных", 2)

            if chess_table[old_cords_x][old_cords_y] == "бq":
                await hod_korolevi(new_cords_x,old_cords_x,new_cords_y, old_cords_y, message, "чёрных", 2)

            if chess_table[old_cords_x][old_cords_y] == "бk":
                await hod_korolya(new_cords_x, old_cords_x, new_cords_y, old_cords_y, message, "чёрных", 2)

        elif (second_p == message.author) and ("ч" in chess_table[old_cords_x][old_cords_y]) and (player == 2):
            if chess_table[old_cords_x][old_cords_y] == "чп":
                if old_cords_y == new_cords_y and ((old_cords_x - new_cords_x == -1) or (old_cords_x - new_cords_x == -2 and old_cords_x == 1)):
                    await hod_peshki(new_cords_x,old_cords_x,new_cords_y, old_cords_y, message, "белых", 1)
                elif old_cords_x - new_cords_x == -1 and abs(old_cords_y - new_cords_y) == 1 and "б" in chess_table[new_cords_x][new_cords_y]:
                    await hodi(new_cords_x, new_cords_y, old_cords_x, old_cords_y, message, "белых", 1)
                else:
                    Wrong_message = await message.channel.send("Так нельзя!")
                    await message.delete()

            if chess_table[old_cords_x][old_cords_y] == "чл":
                await hod_ladyi(new_cords_x, old_cords_x, new_cords_y, old_cords_y, message, "белых", 1)

            if chess_table[old_cords_x][old_cords_y] == "чк":
                await hod_konya(new_cords_x, old_cords_x, new_cords_y, old_cords_y, message, "белых", 1)

            if chess_table[old_cords_x][old_cords_y] == "чс":
                await hod_slona(new_cords_x, old_cords_x, new_cords_y, old_cords_y, message, "белых", 1)

            if chess_table[old_cords_x][old_cords_y] == "чq":
                await hod_korolevi(new_cords_x,old_cords_x, new_cords_y, old_cords_y, message, "белых", 1)

            if chess_table[old_cords_x][old_cords_y] == "чk":
                await hod_korolya(new_cords_x, old_cords_x, new_cords_y, old_cords_y, message, "белых", 1)

        else:
            Wrong_message = await message.channel.send("Так нельзя!")
            await message.delete()
    await shah(message,True)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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

async def hodi(new_cords_x, new_cords_y, old_cords_x, old_cords_y, message, new_hod, new_player):
    global hod, player
    old_figura = chess_table[new_cords_x][new_cords_y]
    chess_table[new_cords_x][new_cords_y] = chess_table[old_cords_x][old_cords_y]
    chess_table[old_cords_x][old_cords_y] = ""
    if await shah(message,False) == "б" and player == 2:
        chess_table[old_cords_x][old_cords_y] = chess_table[new_cords_x][new_cords_y]
        chess_table[new_cords_x][new_cords_y] = old_figura
        await update_screen(message, is_start=False)
        await message.channel.send("Вашему королю по-прежнему угрожают")
    elif await shah(message,False) == "ч" and player == 1:
        chess_table[old_cords_x][old_cords_y] = chess_table[new_cords_x][new_cords_y]
        chess_table[new_cords_x][new_cords_y] = old_figura
        await update_screen(message, is_start=False)
        await message.channel.send("Вашему королю по-прежнему угрожают")
    else:
        hod = new_hod
        player = new_player
        await update_screen(message, is_start=False)
        await message.channel.send(f"Ходит игрок номер {player} за {hod}")



client.run(settings['token'])
