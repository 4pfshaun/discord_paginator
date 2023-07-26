from discord import Interaction, TextStyle
from discord.ui import Button, Modal, TextInput 

class goto_modal(Modal, title="Go to"): 
 page = TextInput(label="page", placeholder='page number', required=True, style=TextStyle.short)

 async def on_submit(self, interaction: Interaction): 
  try: 
    view = self.view
    num = int(self.page.value)-1
    if num in range(len(view.embeds)): 
     view.page = num 
     await view.update_view(interaction)
    else: 
     return await interaction.warn("Invalid Page") 
  except ValueError: 
   return await interaction.warn("This is not a number")

class prev_page(Button): 
  def __init__(self, label, emoji, style): 
   super().__init__(label=label, emoji=emoji, style=style)

  async def callback(self, interaction: Interaction): 
   view = self.view 
   
   if view.page == 0: 
    view.page = len(view.embeds)-1
   else: 
    view.page -= 1
   
   await view.update_view(interaction)

class next_page(Button): 
 def __init__(self, label, emoji, style): 
  super().__init__(label=label, emoji=emoji, style=style)

 async def callback(self, interaction: Interaction): 
  view = self.view 
  
  if view.page == len(view.embeds)-1: 
   view.page = 0
  else: 
   view.page += 1 
  
  await view.update_view(interaction)

class first_page(Button): 
 def __init__(self, label, emoji, style): 
  super().__init__(label=label, emoji=emoji, style=style)

 async def callback(self, interaction: Interaction):
  self.view.page = 0
  await self.view.update_view(interaction)

class last_page(Button): 
 def __init__(self, label, emoji, style): 
  super().__init__(label=label, emoji=emoji, style=style)

 async def callback(self, interaction: Interaction):
  self.view.page = len(self.view.embeds)-1
  await self.view.update_view(interaction)

class delete_page(Button): 
 def __init__(self, label, emoji, style): 
  super().__init__(label=label, emoji=emoji, style=style)

 async def callback(self, interaction: Interaction): 
  await interaction.message.delete()

class goto_page(Button): 
 def __init__(self, label, emoji, style): 
  super().__init__(label=label, emoji=emoji, style=style) 

 async def callback(self, interaction: Interaction):  
  modal = goto_modal()
  modal.view = self.view
  return await interaction.response.send_modal(modal)