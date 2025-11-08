# 🚀 Quick Setup Guide

## Step 1: Create Your `.env` File

1. Copy `.env.example` to create a new file called `.env`
2. Replace the placeholder values with your actual Discord credentials

**Your `.env` file should look like this:**

```env
# Discord Bot Configuration
DISCORD_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
DISCORD_APPLICATION_ID=YOUR_APPLICATION_ID_HERE
DISCORD_CLIENT_SECRET=YOUR_CLIENT_SECRET_HERE
DISCORD_PUBLIC_KEY=YOUR_PUBLIC_KEY_HERE
```

⚠️ **IMPORTANT**: Never commit your `.env` file to Git! It's already in `.gitignore`.

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `discord.py` - Discord bot framework
- `python-dotenv` - Environment variable management

## Step 3: Invite Bot to Your Server

Use this URL format (replace `YOUR_CLIENT_ID` with `1435854356720123904`):

```
https://discord.com/api/oauth2/authorize?client_id=1435854356720123904&permissions=274878221376&scope=bot%20applications.commands
```

**Or build it manually:**
1. Go to [Discord Developer Portal](https://discord.com/developers/applications/1435854356720123904/oauth2/url-generator)
2. Select scopes: `bot` + `applications.commands`
3. Select permissions:
   - Send Messages
   - Embed Links
   - Read Message History
   - Use Slash Commands
4. Copy the generated URL and open it

## Step 4: Set Up Admin Role

1. In your Discord server, create a role called **"League Admin"**
2. Assign this role to league commissioners
3. Only users with this role can use admin commands like `/report_game`

## Step 5: Run the Bot

```bash
python bot.py
```

You should see:
```
[Bot Name] has connected to Discord!
Bot is in 1 guild(s)
Synced 12 command(s)
```

## Step 6: Test Commands

In your Discord server, try:
- `/help` - View all commands
- `/register_team team_name:Chiefs abbreviation:KC` - Register a team
- `/teams` - View registered teams

---

## 🔑 Understanding Your API Keys

| Credential | Purpose | Used In This Bot |
|------------|---------|------------------|
| **Bot Token** | Authenticates your bot to Discord | ✅ **REQUIRED** - Used in `bot.py` |
| **Application ID** | Identifies your app (same as Client ID) | ℹ️ Optional - For reference/OAuth |
| **Client Secret** | OAuth2 authentication for web apps | ❌ Not used (no web login) |
| **Public Key** | Verifies HTTP interactions | ❌ Not used (using gateway) |

### What This Bot Actually Needs

**Only the Bot Token is required!** The bot uses Discord's Gateway API (websocket connection), not HTTP interactions.

The other credentials are useful for:
- **Application ID**: Building invite URLs, future OAuth features
- **Client Secret**: If you later add web-based user authentication
- **Public Key**: If you switch to HTTP-based slash commands (not recommended for this use case)

---

## 🎮 Quick Start Commands

### For Players
```
/register_team team_name:Cowboys abbreviation:DAL
/my_team
/standings
```

### For Admins
```
/report_game winner:@Player1 loser:@Player2 winner_score:28 loser_score:21
/advance_week
/league_info
```

---

## 🔧 Troubleshooting

### Bot doesn't respond
- Check that bot is online (green status)
- Verify bot has permissions in the channel
- Wait 5 minutes after first startup for commands to sync

### "Missing Access" error
- Bot needs "Send Messages" and "Use Slash Commands" permissions
- Check Server Settings → Integrations → Your Bot

### Commands not showing up
- Type `/` in chat to see if commands appear
- Try `/help` to force a sync
- Restart the bot

---

**Ready to go! 🏈**
