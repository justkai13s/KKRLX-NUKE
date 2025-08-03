import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('')

# Bot setup with all intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_guild_join(guild):
    """Create template channels when bot joins a new server"""
    try:
        # Create categories
        announcements_category = await guild.create_category("KKRLX ")
        general_category = await guild.create_category("KKRLX ")
        voice_category = await guild.create_category("KKRLX ")
        staff_category = await guild.create_category("KKRLX")

        # Create text channels in ANUNTURI
        await announcements_category.create_text_channel("KKRLX")
        await announcements_category.create_text_channel("KKRLX")
        await announcements_category.create_text_channel("KKRLX")
        
        # Create text channels in GENERAL
        await general_category.create_text_channel("KKRLX")
        await general_category.create_text_channel("KKRLX")
        await general_category.create_text_channel("KKRLX")
        await general_category.create_text_channel("KKRLX")
        await general_category.create_text_channel("KKRLX")

        # Create voice channels
        await voice_category.create_voice_channel("KKRLX")
        await voice_category.create_voice_channel("KKRLX")
        await voice_category.create_voice_channel("KKRLX")

        # Create staff channels
        await staff_category.create_text_channel("KKRLX")
        await staff_category.create_text_channel("KKRLX")
        await staff_category.create_voice_channel("KKRLX")

        # Send setup complete message
        system_channel = guild.system_channel or next((ch for ch in guild.text_channels), None)
        if system_channel:
            await system_channel.send("🛡️ Server setup complet!")

    except discord.Forbidden:
        print(f"Nu am permisiuni să creez canale pe serverul {guild.name}")
    except Exception as e:
        print(f"Eroare la setarea serverului {guild.name}: {str(e)}")

@bot.event
async def on_guild_channel_delete(channel):
    """Monitor for mass channel deletions"""
    guild = channel.guild
    async for entry in guild.audit_logs(action=discord.AuditLogAction.channel_delete, limit=5):
        if (discord.utils.utcnow() - entry.created_at).seconds < 10:
            # If multiple channels are deleted in less than 10 seconds
            if entry.user != bot.user and not entry.user.guild_permissions.administrator:
                try:
                    # Remove their roles
                    await entry.user.edit(roles=[])
                    # Ban the user
                    await guild.ban(entry.user, reason="Mass channel deletion detected")
                except discord.Forbidden:
                    print(f"Could not take action against {entry.user}")

@bot.event
async def on_guild_channel_create(channel):
    """Monitor for mass channel creation"""
    guild = channel.guild
    async for entry in guild.audit_logs(action=discord.AuditLogAction.channel_create, limit=5):
        if (discord.utils.utcnow() - entry.created_at).seconds < 10:
            # If multiple channels are created in less than 10 seconds
            if entry.user != bot.user and not entry.user.guild_permissions.administrator:
                try:
                    # Remove their roles
                    await entry.user.edit(roles=[])
                    # Ban the user
                    await guild.ban(entry.user, reason="Mass channel creation detected")
                    # Delete the created channels
                    if isinstance(channel, discord.TextChannel) or isinstance(channel, discord.VoiceChannel):
                        await channel.delete()
                except discord.Forbidden:
                    print(f"Could not take action against {entry.user}")

@bot.event
async def on_member_ban(guild, user):
    """Notify when a raid attacker is banned"""
    try:
        # Find a system channel or the first text channel to send the notification
        channel = guild.system_channel or next((ch for ch in guild.text_channels), None)
        if channel:
            await channel.send(f"🛡️ Securitate: Utilizatorul {user.name} a fost banat pentru încercare de raid.")
    except:
        pass

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)
