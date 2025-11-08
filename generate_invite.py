"""
Generate Discord Bot Invite URL
This script creates the invite link for your bot using your Application ID
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Get Application ID from environment
APP_ID = os.getenv('DISCORD_APPLICATION_ID')

if not APP_ID:
    print("❌ ERROR: DISCORD_APPLICATION_ID not found in .env file")
    print("Please add your Application ID to the .env file")
    exit(1)

# Permissions needed for the bot
# 277025787968 = Send Messages, Embed Links, Read Message History, Use Application Commands, Manage Channels
PERMISSIONS = "277025787968"

# Generate invite URL with BOTH bot and applications.commands scopes
invite_url = f"https://discord.com/api/oauth2/authorize?client_id={APP_ID}&permissions={PERMISSIONS}&scope=bot%20applications.commands"

print("=" * 70)
print("🏈 MADDEN FRANCHISE BOT - INVITE URL")
print("=" * 70)
print()
print("⚠️  IMPORTANT: If bot is already in your server, you need to:")
print("   1. Kick the bot from your server first")
print("   2. Then use this new invite URL")
print()
print("=" * 70)
print()
print("Copy this URL and paste it in your browser to invite the bot:")
print()
print(invite_url)
print()
print("=" * 70)
print()
print("Steps:")
print("1. Right-click the bot in your server → Kick")
print("2. Open the URL above in your browser")
print("3. Select your Discord server from the dropdown")
print("4. Make sure 'bot' and 'applications.commands' are BOTH checked")
print("5. Click 'Authorize'")
print("6. Complete the CAPTCHA if prompted")
print()
print("After re-inviting, restart bot.py and commands should work!")
print("=" * 70)
