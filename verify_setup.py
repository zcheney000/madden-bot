"""
Setup Verification Script
Checks if everything is configured correctly before running the bot
"""
import os
import sys
from pathlib import Path

def check_file(filepath, required=True):
    """Check if a file exists"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else ("❌" if required else "⚠️")
    req_text = " (REQUIRED)" if required else " (optional)"
    print(f"{status} {filepath}{req_text if required else ''}")
    return exists

def check_env_var(var_name, required=True):
    """Check if an environment variable is set"""
    from dotenv import load_dotenv
    load_dotenv()
    
    value = os.getenv(var_name)
    exists = value is not None and value != "" and "your_" not in value.lower()
    status = "✅" if exists else ("❌" if required else "⚠️")
    req_text = " (REQUIRED)" if required else " (optional)"
    
    if exists:
        # Show first/last few characters for verification
        if len(value) > 20:
            display = f"{value[:8]}...{value[-8:]}"
        else:
            display = value[:4] + "..." + value[-4:]
        print(f"{status} {var_name}: {display}")
    else:
        print(f"{status} {var_name}: NOT SET{req_text}")
    
    return exists

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import discord
        print(f"✅ discord.py: {discord.__version__}")
        return True
    except ImportError:
        print("❌ discord.py: NOT INSTALLED")
        return False

print("=" * 70)
print("🏈 MADDEN FRANCHISE BOT - SETUP VERIFICATION")
print("=" * 70)
print()

# Check files
print("📁 Checking Files:")
print("-" * 70)
has_bot = check_file("bot.py", required=True)
has_requirements = check_file("requirements.txt", required=True)
has_env = check_file(".env", required=True)
has_env_example = check_file(".env.example", required=False)
print()

# Check dependencies
print("📦 Checking Dependencies:")
print("-" * 70)
has_deps = check_dependencies()
print()

# Check environment variables
print("🔑 Checking Environment Variables:")
print("-" * 70)
has_token = check_env_var("DISCORD_BOT_TOKEN", required=True)
has_app_id = check_env_var("DISCORD_APPLICATION_ID", required=False)
has_secret = check_env_var("DISCORD_CLIENT_SECRET", required=False)
has_key = check_env_var("DISCORD_PUBLIC_KEY", required=False)
print()

# Summary
print("=" * 70)
print("📊 SUMMARY")
print("=" * 70)

all_required = has_bot and has_requirements and has_env and has_deps and has_token

if all_required:
    print("✅ All required components are configured!")
    print()
    print("🚀 You're ready to run the bot:")
    print("   python bot.py")
    print()
    print("📋 Next steps:")
    print("   1. Run: python generate_invite.py")
    print("   2. Use the invite URL to add bot to your server")
    print("   3. Create 'League Admin' role in Discord")
    print("   4. Start the bot with: python bot.py")
else:
    print("❌ Some required components are missing!")
    print()
    print("🔧 To fix:")
    
    if not has_deps:
        print("   → Install dependencies: pip install -r requirements.txt")
    
    if not has_env:
        print("   → Create .env file: copy .env.example to .env")
    
    if not has_token:
        print("   → Add DISCORD_BOT_TOKEN to your .env file")
    
    print()
    print("📖 See SETUP_GUIDE.md for detailed instructions")

print("=" * 70)
