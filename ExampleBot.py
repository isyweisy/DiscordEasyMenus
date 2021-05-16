#!/usr/bin/env python3
#============================#
# Discord Easy Menus Example #
#        By isyweisy         #
#============================#

"""A program to demonstrate the Discord Easy Menus library."""

# Import required dependencies.
import discord, DiscordEasyMenus

# Make sure to configure the settings file!
import Settings

# Make your custom bot as normal, but this time inherit from DiscordEasyMenus.Bot
# Any overrides to on_raw_reaction_add, on_raw_reaction_remove or close will need to include a call to super however.
class MyBot(DiscordEasyMenus.Bot):
    async def on_ready(self):
        print(f"Logged in as {self.user.name}#{self.user.discriminator}")

# Create a new bot, with your desired command prefix.
bot = MyBot(command_prefix="!")

# What will happen when the question mark button is pressed?
# Payload will be an instance of discord.RawReactionActionEvent
async def question_down(payload, menu):
    print("Question button down!")

# What will happen when the question mark button is released?
# Payload will be an instance of discord.RawReactionActionEvent
async def question_up(payload, menu):
    print("Question button up!")

# What will happen when the cool button is pressed?
# Payload will be an instance of discord.RawReactionActionEvent
async def cool_down(payload, menu):
    print("Cool button down!")

# What will happen when the question cool button is released?
# Payload will be an instance of discord.RawReactionActionEvent
async def cool_up(payload, menu):
    print("Cool button up!")

# What will happen when the close button is pressed?
# Payload will be an instance of discord.RawReactionActionEvent
async def close_down(payload, menu):
    # Generate our new message.
    message = "When this menu was closed:\n"
    for i in menu.buttons:
        # MenuButton.pressers represents the users who have currently reacted for that button.
        for j in i.pressers:
            if j != None:
                message += f"{j.name} was pressing {i.emoji.name}\n"
            else:
                # If the user was None, we are in a DM.
                message += f"You were pressing {i.emoji.name}\n"
    # Send the updated message.
    # Notice we did not specify a title. Unspecified arguments will remain the same.
    await menu.edit(body=message, color=discord.Color.green())
    # Close the menu when we are done, to prevent further changes and interactiona, and to free memory.
    await menu.close()

# What will happen if the bot gets shutdown whilst this menu is still open?
async def on_close(menu):
    await menu.edit(body="This menu was open when the bot was shutdown!", color=discord.Color.blue())

# This is the command to create our menu.
@bot.command()
async def mymenu(ctx):
    # Create the buttons for our menu.
    buttons = [
        # We specify our emoji, as well as the functions to call when the button is pressed or released.
        # You don't need to provide a on_down or on_up function if you don't want to.
        # Remember to pass these functions through WITHOUT THE BRACKETS.
        DiscordEasyMenus.MenuButton(discord.PartialEmoji(name="\U00002753"), on_down=question_down, on_up=question_up),
        DiscordEasyMenus.MenuButton(discord.PartialEmoji(name="\U0001F60E"), on_down=cool_down, on_up=cool_up)
    ]
    # Create our menu, specifying title, body, color, buttons and on_close function.
    # Make sure to pass through the context (ctx), but the other parameters are optional.
    menu = await bot.create_menu(ctx, "Hello World!", "This is a menu!", discord.Color.dark_red(), buttons, on_close)

    # Let's add another button whilst the menu is already up.
    # This one doesn't have and on_up
    button = DiscordEasyMenus.MenuButton(discord.PartialEmoji(name="\U0000274C"), on_down=close_down)
    await menu.add_button(button)

# It's always good practice to have a way to close the connection gracefully!
# In a production bot, this would likely only respond to a few users.
@bot.command()
async def shutdown(ctx):
    await ctx.send("Closing bot.")
    await ctx.bot.close()

# Finally, we run our bot!
# Remember to configure your bot's access token in the settings file!
bot.run(Settings.TOKEN)