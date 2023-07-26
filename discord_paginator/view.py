from discord import Interaction, Embed 

class CustomInteraction(Interaction): 
   def __init__(self, **kwargs): 
    super().__init__(**kwargs)

   async def warn(self, message: str) -> None: 
    return await self.response.send_message(embed=Embed(color=0xffff00, description=f"⚠️ {self.user.mention}: {message}"), ephemeral=True)     