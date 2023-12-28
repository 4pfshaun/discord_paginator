import discord 
from discord.ext import commands

from typing import List, Optional, Any
from .buttons import First, Last, Next, Delete, GotoPage, Previous

class Paginator(discord.ui.View): 
  def __init__(
    self, 
    ctx: commands.Context, 
    embeds: List[Any], 
    invoker: Optional[int]=None): 
   """A class which manages the pages of a message
        Parameters
        ----------- 
        ctx: `discord.ext.commands.Context`
          The context where the paginator was invoked in
        embeds: List[`Any`]
          The values that are going to be paginated (we recommend strings, discord.Embed, discord.File or a dict of contents)  
        invoker: Optional[`int`]
          The member id that can use the paginator (default is the ctx.author id)
    """
   super().__init__(timeout=None)
   self.embeds = embeds
   self.ctx = ctx   
   self.invoker = invoker or self.ctx.author.id
   self.page = 0

  async def update_view(self, interaction: discord.Interaction): 
    if isinstance(self.embeds[self.page], str):
      await interaction.response.edit_message(
        content=self.embeds[self.page], 
        embed=None,
        attachments=[]
      )
    elif isinstance(self.embeds[self.page], discord.Embed): 
      await interaction.response.edit_message(
        content=None, 
        embed=self.embeds[self.page],
        attachments=[],
      ) 
    elif isinstance(self.embeds[self.page], discord.File):
      await interaction.response.edit_message(
        content=None, 
        embed=None, 
        attachments=[self.embeds[self.page]] 
      )
    elif isinstance(self.embeds[self.page], dict): 
      try: 
        await interaction.response.edit_message(**self.embeds[self.page])
      except TypeError:
        await interaction.response.send_message(
          "A problem occured while changing the page", 
          ephemeral=True
        )

  def add_button(
    self, 
    action: str,
    /, 
    *, 
    label: str = "", 
    emoji: str = None, 
    style = discord.ButtonStyle.gray
  ): 
    """Add a button to the paginator
        Parameters
        ----------
        action: `str`
          The action you want the button to do. Can be: first, last, next, prev, goto, delete
        label: Optional[`str`]
          Text on the button
        emoji: Optional[`discord.PartialEmoji`]
          An emoji for the button
        style: Optional[`discord.ButtonStyle`]
          The color of the button. Default is to discord.ButtonStyle.gray
    """

    action = action.strip().lower()
    kwargs = {
      "label": label, 
      "emoji": emoji, 
      "style": style
    }

    match action: 
      case "first":
        self.add_item(First(**kwargs))
      case "last":
        self.add_item(Last(**kwargs))  
      case "next":
        self.add_item(Next(**kwargs))
      case "prev": 
        self.add_item(Previous(**kwargs)) 
      case "previous":
        self.add_item(Previous(**kwargs))
      case "goto":
        self.add_item(GotoPage(**kwargs))
      case "delete":
        self.add_item(Delete(**kwargs))
      case _: 
        return
       
  async def interaction_check(self, interaction: discord.Interaction) -> bool:
    check = bool(interaction.user.id == self.invoker)

    if not check:
      await interaction.response.defer()
    
    return check

  async def default_paginator(self): 
    """
    Start the paginator with some default buttons
    """

    self.add_button("first", label='first')
    self.add_button("back", label='back')
    self.add_button("goto", label='go to')
    self.add_button("next", label='next')
    self.add_button("last", label='last')
    self.add_button("delete", label='Close paginator', style=discord.ButtonStyle.danger)
    await self.start()

  async def start(self): 
    if len(self.embeds) == 1:
     view = None 
    else: 
     view = self 
 
    try: 
      if isinstance(self.embeds[0], str):
        self.message = await self.ctx.send(
          content=self.embeds[0], 
          view=view
        )
      elif isinstance(self.embeds[0], discord.Embed): 
        self.message = await self.ctx.send(
          embed=self.embeds[0], 
          view=view
        ) 
      elif isinstance(self.embeds[0], discord.File): 
        self.message = await self.ctx.send(
          file=self.embeds[0],
          view=view
        )
      elif isinstance(self.embeds[0], dict): 
        self.embeds[0]['view'] = view 
        self.message = await self.ctx.send(**self.embeds[0])

    except discord.HTTPException: 
     self.stop()