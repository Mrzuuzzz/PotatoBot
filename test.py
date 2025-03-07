import discord, requests, aiohttp, io, random, asyncio, json
from discord.ext import commands
from discord import app_commands
# from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

with open("brailynmom.json", "r") as file:
    j = json.load(file)
    
    for i in j["leaderboard"]:
        print(i+" "+str(j["leaderboard"][i]))