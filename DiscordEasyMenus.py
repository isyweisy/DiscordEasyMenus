#====================#
# Discord Easy Menus #
#    By isyweisy     #
#====================#

"""A library to easily make reaction based menus for Discord bots."""

import discord
from discord.ext import commands

class Bot(commands.Bot):

    menus = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menus = {}

    async def create_menu(self, ctx, title=None, body=None, color=None, buttons=[]):
        menu = Menu()
        await menu.create(ctx, self, title, body, color, buttons)
        self.menus[menu.message.id] = menu
        return menu

    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.user.id and payload.message_id in self.menus:
            await self.menus[payload.message_id].on_reaction_add(payload)

    async def on_raw_reaction_remove(self, payload):
        if payload.user_id != self.user.id and payload.message_id in self.menus:
            await self.menus[payload.message_id].on_reaction_remove(payload)

class Menu():

    channel = discord.abc.Messageable
    bot = Bot
    message = discord.Message
    buttons = []

    async def create(self, ctx, bot, title=None, body=None, color=None, buttons=[]):
        self.bot = bot
        embed = discord.Embed(title=title, description=body, color=color)
        self.message = await ctx.send(embed=embed)
        self.buttons = []
        for i in buttons:
            await self.add_button(i)

    async def edit(self, title=None, body=None, color=None):
        embed = self.message.embeds[0]
        if title != None:
            embed.title = title
        if body != None:
            embed.description = body
        if color != None:
            embed.color = color
        await self.message.edit(embed=embed)

    async def close(self):
        self.bot.menus.pop(self.message.id)

    async def add_button(self, button):
        self.buttons.append(button)
        await self.message.add_reaction(button.emoji)

    async def on_reaction_add(self, payload):
        for i in self.buttons:
            if payload.emoji.name == i.emoji.name:
                await i.press(payload, self)

    async def on_reaction_remove(self, payload):
        for i in self.buttons:
            if payload.emoji.name == i.emoji.name:
                await i.release(payload, self)


class MenuButton():

    emoji = discord.PartialEmoji
    pressers = []

    def __init__(self, emoji, on_down=None, on_up=None):
        self.emoji = emoji
        self.pressers = []
        self.on_down = on_down
        self.on_up = on_up

    async def press(self, payload, menu):
        self.pressers.append(payload.member)
        if self.on_down != None:
            await self.on_down(payload, menu)

    async def release(self, payload, menu):
        self.pressers.remove(payload.member)
        if self.on_up != None:
            await self.on_up(payload, menu)