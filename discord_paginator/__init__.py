import discord
from discord.ext import commands
from typing import List

class goto_modal(discord.ui.Modal, title="Go to"): 
 page = discord.ui.TextInput(label="page", placeholder='page number', required=True, style=discord.TextStyle.short)

 async def on_submit(self, interaction: discord.Interaction): 
  try: 
    view = self.view
    num = int(self.page.value)-1
    if num in range(len(view.embeds)): 
     view.page = num 
     await view.update_view(interaction)
    else: return await interaction.response.send_message(ephemeral=True, embed=discord.Embed(color=0xffff00, description=f"⚠️ {interaction.user.mention}: Invalid Page")) 
  except ValueError: return await interaction.response.send_message(ephemeral=True, embed=discord.Embed(color=0xffff00, description=f"⚠️ {interaction.user.mention}: This is not a number"))

class prev_page(discord.ui.Button): 
  def __init__(self, label, emoji, style): 
   super().__init__(label=label, emoji=emoji, style=style)

  async def callback(self, interaction: discord.Interaction): 
   view = self.view 
   if view.page == 0: view.page = len(view.embeds)-1
   else: view.page -= 1
   await view.update_view(interaction)

class next_page(discord.ui.Button): 
 def __init__(self, label, emoji, style): 
  super().__init__(label=label, emoji=emoji, style=style)

 async def callback(self, interaction: discord.Interaction): 
  view = self.view 
  if view.page == len(view.embeds)-1: view.page = 0
  else: view.page += 1 
  await view.update_view(interaction)

class first_page(discord.ui.Button): 
 def __init__(self, label, emoji, style): 
  super().__init__(label=label, emoji=emoji, style=style)

 async def callback(self, interaction: discord.Interaction):
  self.view.page = 0
  await self.view.update_view(interaction)

class last_page(discord.ui.Button): 
 def __init__(self, label, emoji, style): 
  super().__init__(label=label, emoji=emoji, style=style)

 async def callback(self, interaction: discord.Interaction):
  self.view.page = len(self.view.embeds)-1
  await self.view.update_view(interaction)

class delete_page(discord.ui.Button): 
 def __init__(self, label, emoji, style): 
  super().__init__(label=label, emoji=emoji, style=style)

 async def callback(self, interaction: discord.Interaction): 
  await interaction.message.delete()

class goto_page(discord.ui.Button): 
 def __init__(self, label, emoji, style): 
  super().__init__(label=label, emoji=emoji, style=style) 

 async def callback(self, interaction: discord.Interaction):  
  modal = goto_modal()
  modal.view = self.view
  return await interaction.response.send_modal(modal)

class Paginator(discord.ui.View): 
  def __init__(self, ctx: commands.Context, embeds: List[discord.Embed], invoker: int=None): 
   """A class which manages the pages of a message
        Parameters
        ----------- 
        ctx: :class:`discord.ext.commands.Context`
          The context where the paginator was invoked in
        embeds: :class:`list`
            The embeds that will be paginated
        invoker: Optional[:class:`int`]
          The id of the member that can use the paginator    
    """
   super().__init__(timeout=None)
   self.embeds = embeds
   self.ctx = ctx
   self.invoker = invoker   
   self.actions = ["next", "previous", "prev", "first", "last", "delete", "goto"]
   self.page = 0
   self.color = 0xffff00
   self.emoji = "⚠️"

  async def update_view(self, interaction: discord.Interaction): 
   await interaction.response.edit_message(embed=self.embeds[self.page])

  def add_button(self, action: str, /, *, label: str="", emoji=None, style: str=discord.ButtonStyle.gray): 
   """Add a button to the paginator
       Parameters
       ----------
       action: :class:`str`
         The action you want the button to do. Can be: first, last, next, prev, goto, delete
       label: Optional[:class:`str`]
        Text on the button
       emoji: Optional[:class:`discord.PartialEmoji`]
         An emoji for the button
       style: Optional[:class:`discord.ButtonStyle`]
        The color of the button. Default is to discord.ButtonStyle.gray
   """
   action = action.strip().lower()
   if not action in self.actions: return
   if action == "first": self.add_item(first_page(label, emoji, style))  
   elif action == "last": self.add_item(last_page(label, emoji, style)) 
   elif action == "next": self.add_item(next_page(label, emoji, style))
   elif action in ["prev", "previous"]: self.add_item(prev_page(label, emoji, style))
   elif action == "delete": self.add_item(delete_page(label, emoji, style))
   elif action == "goto": self.add_item(goto_page(label, emoji, style)) 

  async def interaction_check(self, interaction: discord.Interaction) -> bool:
   if not self.invoker: return True 
   if interaction.user.id != self.invoker: 
    await interaction.response.send_message(embed=discord.Embed(color=self.color, description=f"{self.emoji} {interaction.user.mention}: You are **not** the author of this embed"), ephemeral=True)
    return False 
   return True 

  async def default_paginator(self): 
   """Start the paginator with some default buttons"""
   self.add_button("first", label='first')
   self.add_button("back", label='back')
   self.add_button("goto", label='go to')
   self.add_button("next", label='next')
   self.add_button("last", label='last')
   self.add_button("delete", label='Close paginator', style=discord.ButtonStyle.danger)
   await self.start()

  async def start(self): 
   try: self.message = await self.ctx.send(embed=self.embeds[0], view=self)
   except discord.HTTPException: self.stop()