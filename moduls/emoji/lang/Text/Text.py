# ------------------------------------
import discord
from discord.ext import commands
from discord import utils
# ------------------------------------

def command_response (id, author, mention:None, language):
    if mention == None:
        if language == "RU":
            error_emoji = '***⛔️: Тебе нужно выбрать человека!***'
        elif language == "ENG":
            error_emoji = '***⛔️: You need to choose a person!***'
        return error_emoji  
    if language == "RU":
        commands =  {  
                "slap": f'*💭:* ***{mention}!*** *Вас ударил(а)* ***{author}!***' ,
                "hug": f'*💭:* ***{mention}!*** *Вас обнял(а)* ***{author}!***' ,
                "tickle": f'*💭:* ***{mention}!*** *Вас пощекотал(а)* ***{author}!***',
                "feed": f'*💭:* ***{mention}!*** *Вас покормил(а)* ***{author}!***',
                "poke": f'*💭:* ***{mention}!*** *Вас тыкнул(а)* ***{author}!***',
                "bite": f'*💭:* ***{mention}!*** *Вас укусил(а)* ***{author}!***',
                "pat": f'*💭:* ***{mention}!*** *Вас погладил(а)* ***{author}!***',
                "kiss": f'*💭:* ***{mention}!*** *Вас поцеловал(а)* ***{author}!***',
                "bonk": f'*💭:* ***{mention}!*** *You get The BONK by* ***{author}!***',
                "sorry": f'*💭:* ***{mention}!*** ***{author}*** *просит у вас прощения!*',
                "sorryt": f'*💭:* ***{mention}!*** ***{author}*** *требует чтобы ты извинился.* ***ИЗВИНИСЬ!***',
        }
        return_text = commands[id]

    elif language == "ENG":
        commands =  {  
            "slap": f'*💭:* ***{mention}!*** ***{author}*** *hit you!*' ,
            "hug": f'*💭:* ***{mention}!*** ***{author}*** *hugged you!*' ,
            "tickle": f'*💭:* ***{mention}!*** ***{author}*** *tickled you!*' ,
            "feed": f'*💭:* ***{mention}!*** ***{author}*** *fed you!*' ,
            "poke": f'*💭:* ***{mention}!*** ***{author}*** *poked you!*' ,
            "bite": f'*💭:* ***{mention}!*** ***{author}*** *bit you!*' ,
            "pat": f'*💭:* ***{mention}!*** ***{author}*** *patted you!*' ,
            "kiss": f'*💭:* ***{mention}!*** ***{author}*** *kissed you!*' ,
            "bonk": f'*💭:* ***{mention}!*** *You get The BONK by* ***{author}!***',
            "sorry": f'*💭:* ***{mention}!*** ***{author}*** *asks your forgiveness!*',
            "sorryt": f'*💭:* ***{mention}!*** ***{author}*** *demands you to apologize.* ***SAY SORRY!***',
            "lick": f'*💭:* ***{mention}!*** ***{author}*** *licked you!*' ,
        }
        return_text = commands[id]

    return  return_text
