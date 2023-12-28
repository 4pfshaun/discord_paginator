import discord

class Goto(discord.ui.Modal, title="Go to"): 
  page = discord.ui.TextInput(
    label="Page", 
    placeholder='Page Number', 
    required=True, 
    style=discord.TextStyle.short
  )
 
  async def on_submit(self, interaction: discord.Interaction): 
    view = self.view
    num = int(self.page.value)-1
    if num in range(len(view.embeds)): 
      view.page = num 
      await view.update_view(interaction)
    else: 
      return await interaction.response.send_message("Invalid Page", ephemeral=True) 
    
  async def on_error(self, interaction: discord.Interaction, error: Exception):
    await interaction.response.send_message(
      embed=discord.Embed(
        color=0xffff00, 
        description=f"⚠️ {interaction.user.mention}: A problem occured while changing the page"
      ), 
      ephemeral=True
    )

class Previous(discord.ui.Button): 
  async def callback(self, interaction: discord.Interaction): 
    view = self.view 
    
    if view.page == 0: 
      view.page = len(view.embeds)-1
    else: 
      view.page -= 1
    
    await view.update_view(interaction)

class Next(discord.ui.Button): 
  async def callback(self, interaction: discord.Interaction): 
    view = self.view 
    
    if view.page == len(view.embeds)-1: 
      view.page = 0
    else: 
      view.page += 1 
    
    await view.update_view(interaction)
 
class First(discord.ui.Button): 
  async def callback(self, interaction: discord.Interaction):
    self.view.page = 0
    await self.view.update_view(interaction)
 
class Last(discord.ui.Button): 
  
  async def callback(self, interaction: discord.Interaction):
    self.view.page = len(self.view.embeds)-1
    await self.view.update_view(interaction)

class Delete(discord.ui.Button): 

  async def callback(self, interaction: discord.Interaction): 
    await interaction.message.delete()

class GotoPage(discord.ui.Button): 

  async def callback(self, interaction: discord.Interaction):  
    modal = Goto()
    modal.view = self.view
    return await interaction.response.send_modal(modal)