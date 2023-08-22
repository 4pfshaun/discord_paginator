from discord import Interaction, Embed, ButtonStyle, HTTPException
from discord.ui import View

from discord.ext import commands
from typing import List, Union

from .buttons import first_page, last_page, next_page, prev_page, goto_page, delete_page

class Paginator(View): 
  def __init__(self, ctx: commands.Context, embeds: List[Union[str, Embed]], bad_invoker_message: str="You are **not** the author of this embed"): 
   """A class which manages the pages of a message
        Parameters
        ----------- 
        ctx: :class:`discord.ext.commands.Context`
          The context where the paginator was invoked in
        embeds: :class:`list`
          The embeds that will be paginated  
    """
   super().__init__(timeout=None)
   self.embeds = embeds
   self.ctx = ctx   
   self.actions = ["next", "previous", "prev", "first", "last", "delete", "goto"]
   self.page = 0
   self.color = 0xffff00
   self.emoji = "⚠️"
   self.bad_invoker_message = bad_invoker_message

  async def update_view(self, interaction: Interaction): 
   if isinstance(self.embeds[self.page], str):
    await interaction.response.edit_message(content=self.embeds[self.page], embed=None)
   elif isinstance(self.embeds[self.page], Embed): 
    await interaction.response.edit_message(content=None, embed=self.embeds[self.page]) 

  def add_button(self, action: str, /, *, label: str="", emoji=None, style: str=ButtonStyle.gray): 
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
   if not action in self.actions: 
    return
   if action == "first": 
    self.add_item(first_page(label, emoji, style))  
   elif action == "last": 
    self.add_item(last_page(label, emoji, style)) 
   elif action == "next": 
    self.add_item(next_page(label, emoji, style))
   elif action in ["prev", "previous"]: 
    self.add_item(prev_page(label, emoji, style))
   elif action == "delete": 
    self.add_item(delete_page(label, emoji, style))
   elif action == "goto": 
    self.add_item(goto_page(label, emoji, style)) 

  async def interaction_check(self, interaction: Interaction) -> bool:
   if interaction.user.id != self.ctx.author.id: 
    await interaction.response.send_message(embed=Embed(color=0xffff00, description=f"⚠️ {self.user.mention}: {self.bad_invoker_message}"), ephemeral=True)
    return False 
   return True 

  async def default_paginator(self): 
   """Start the paginator with some default buttons"""
   self.add_button("first", label='first')
   self.add_button("back", label='back')
   self.add_button("goto", label='go to')
   self.add_button("next", label='next')
   self.add_button("last", label='last')
   self.add_button("delete", label='Close paginator', style=ButtonStyle.danger)
   await self.start()

  async def start(self): 
   if len(self.embeds) == 1:
    view = None 
   else: 
    view = self 

   try: 
    if isinstance(self.embeds[0], str):
     self.message = await self.ctx.send(content=self.embeds[0], embed=None, view=view)
    elif isinstance(self.embeds[0], Embed): 
     self.message = await self.ctx.send(content=None, embed=self.embeds[0], view=view) 
   except HTTPException: 
    self.stop()