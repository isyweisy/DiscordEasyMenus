#====================#
# Discord Easy Menus #
#    By isyweisy     #
#====================#

"""A library to easily make reaction based menus for Discord bots."""

# Import dependencies.
import discord
from discord.ext import commands

class Bot(commands.Bot):
    """A Discord bot class including hooks for easy custom menus!"""

    # We will need a list of menus to update later.
    menus = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menus = {}

    async def create_menu(self, ctx, title=None, body=None, color=None, buttons=[]):
        """An easy method of generating reaction based Discord bot menus."""
        menu = Menu()
        await menu.create(ctx, self, title, body, color, buttons)
        # Store this in our dictionary, indexed by the message ID, so that we can easily identify it later.
        self.menus[menu.message.id] = menu
        return menu

    async def on_raw_reaction_add(self, payload):
        # This function will be called by Discord when a reaction is added.
        # If our bot wasn't the one who reacted and the reaction was on one of our menus, we will pass the event through to the menu.
        if payload.user_id != self.user.id and payload.message_id in self.menus:
            await self.menus[payload.message_id].on_reaction_add(payload)

    async def on_raw_reaction_remove(self, payload):
        # This function will be called by Discord when a reaction is added.
        # If our bot wasn't the one who reacted and the reaction was on one of our menus, we will pass the event through to the menu.
        if payload.user_id != self.user.id and payload.message_id in self.menus:
            await self.menus[payload.message_id].on_reaction_remove(payload)

class Menu():
    """A reaction based menu for Discord bots."""

    # We will need to keep hold of some of the context information for later.
    channel = discord.abc.Messageable
    bot = Bot
    message = discord.Message
    buttons = []

    async def create(self, ctx, bot, title=None, body=None, color=None, buttons=[]):
        """An easy method of generating reaction based Discord bot menus."""
        self.bot = bot
        # Load up the message content and send.
        embed = discord.Embed(title=title, description=body, color=color)
        self.message = await ctx.send(embed=embed)
        # Add the buttons so that the user can interact with the program.
        self.buttons = []
        for i in buttons:
            await self.add_button(i)

    async def edit(self, title=None, body=None, color=None):
        """A method used to edit the contents of an existing custom menu."""
        # We load up the old data so that we can reuse some of it if the developer has not specified new values.
        # There should only be one embed attached to this message.
        embed = self.message.embeds[0]
        # Only update the data if we have new values.
        if title != None:
            embed.title = title
        if body != None:
            embed.description = body
        if color != None:
            embed.color = color
        # Send off the new data.
        await self.message.edit(embed=embed)

    async def close(self):
        """Make the bot forget about your menu so that you receive no further updates or changes, and can free memory."""
        self.bot.menus.pop(self.message.id)

    async def add_button(self, button):
        """Adds a reaction based button to an existing menu."""
        self.buttons.append(button)
        await self.message.add_reaction(button.emoji)

    async def on_reaction_add(self, payload):
        # If we got here, the reaction was on this menu.
        # Check to see if it was related to any of the buttons, and if so, pass it on to that button.
        for i in self.buttons:
            if payload.emoji.name == i.emoji.name:
                await i.press(payload, self)

    async def on_reaction_remove(self, payload):
        # If we got here, the reaction was on this menu.
        # Check to see if it was related to any of the buttons, and if so, pass it on to that button.
        for i in self.buttons:
            if payload.emoji.name == i.emoji.name:
                await i.release(payload, self)


class MenuButton():
    """A reaction based button for a Discord bot menu."""

    # Every reaction needs an emote. We use the type discord.PartialEmoji to represent these emoji.
    emoji = discord.PartialEmoji
    # This list represents which users are currently pressing the button.
    pressers = []

    def __init__(self, emoji, on_down=None, on_up=None):
        self.emoji = emoji
        self.pressers = []
        self.on_down = on_down
        self.on_up = on_up

    async def press(self, payload, menu):
        # Keep track of who is pressing the button, and if we have a provided function to call, call it.
        self.pressers.append(payload.member)
        if self.on_down != None:
            await self.on_down(payload, menu)

    async def release(self, payload, menu):
        # Keep track of who is pressing the button, and if we have a provided function to call, call it.
        self.pressers.remove(payload.member)
        if self.on_up != None:
            await self.on_up(payload, menu)