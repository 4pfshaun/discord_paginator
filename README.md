# discord_paginator
### A package that can paginate your discord embeds 

To install you need [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). After installing run the following command:

```
pip install git+https://github.com/prettylittlelies/discord_paginator
```

### Examples:

# The default paginator

```py
from discord_paginator import Paginator

@bot.command()
async def default(ctx: commands.Context):
 """A paginator command using the default paginator""" 
 embeds = [discord.Embed(color=0x2f3136, description=i) for i in ["this is the 1st page", "this is the 2nd page", "this is the 3rd page"]]
 #building the embeds above
 paginator = Paginator(ctx, embeds, invoker=ctx.author.id)
 await paginator.default_paginator() #send the paginator
```

Custom paginator
```py
from discord_paginator import Paginator

@bot.command()
async def custom(ctx: commands.Context): 
 """A paginator command using custom buttons"""
 embeds = [discord.Embed(color=0x2f3136, description=i) for i in ["this is the 1st page", "this is the 2nd page", "this is the 3rd page"]]
 #building the embeds above
 paginator = Paginator(ctx, embeds, invoker=ctx.author.id)
 paginator.add_button('prev', label="prev", style=discord.ButtonStyle.blurple)
 paginator.add_button('next', label="next", style=discord.ButtonStyle.blurple)
 paginator.add_button('goto', label="go to")
 paginator.add_button('delete', label="close", style=discord.ButtonStyle.danger)
 #since the buttons are part of the discord.ui.Button class you can modify the label, style and emoji as you like
 await paginator.start() #sending the custom paginator
```

```diff
All actions
! "first": Goes to the first embed
+ "prev": Goes to the previous embed
- "delete": Deletes the message
+ "next": Goes to the next embed
! "last": Goes to the last embed
"goto": goes to a custom embed page
```

**You can check examples to see how the paginator actually works**
