import discord 
from discord.ext import commands 
from discord_paginator import Paginator

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event 
async def on_ready(): 
  print(f"{bot.user} is ready")  

@bot.command()
async def default(ctx: commands.Context):
 """A paginator command using the default paginator""" 
 embeds = [discord.Embed(color=0x2f3136, description="hi"), "content, not embed", discord.Embed(color=0xff0000, title="goodbye")]
 #building the embeds above
 paginator = Paginator(ctx, embeds)
 await paginator.default_paginator() #send the paginator

@bot.command()
async def custom(ctx: commands.Context): 
 """A paginator command using custom buttons"""
 embeds = [discord.Embed(color=0x2f3136, description=i) for i in ["this is the 1st page", "this is the 2nd page", "this is the 3rd page"]]
 #building the embeds above
 paginator = Paginator(ctx, embeds)
 paginator.add_button('prev', label="prev", style=discord.ButtonStyle.blurple)
 paginator.add_button('next', label="next", style=discord.ButtonStyle.blurple)
 paginator.add_button('goto', label="go to")
 paginator.add_button('delete', label="close", style=discord.ButtonStyle.danger)
 #since the buttons are part of the discord.ui.Button class you can modify the label, style and emoji as you like
 await paginator.start() #sending the custom paginator

bot.run("token")  