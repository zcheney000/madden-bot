# 🔑 Discord API Keys - Complete Guide

## Your Credentials

You have 4 different credentials from Discord:

```
Bot Token:        YOUR_BOT_TOKEN_HERE
Application ID:   YOUR_APPLICATION_ID_HERE
Client Secret:    YOUR_CLIENT_SECRET_HERE
Public Key:       YOUR_PUBLIC_KEY_HERE
```

## What Each One Does

### 1️⃣ Bot Token (REQUIRED ✅)

**What it is:** Your bot's password to log into Discord

**Used for:** Authenticating your bot with Discord's API

**In this project:** 
- Used in `bot.py` to connect to Discord
- Read from `.env` file as `DISCORD_BOT_TOKEN`
- **This is the ONLY credential you need for the bot to work!**

**Example usage:**
```python
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
bot.run(TOKEN)
```

**Security:** 🔒 **NEVER share this!** Anyone with your bot token can control your bot.

---

### 2️⃣ Application ID / Client ID (Optional ⚠️)

**What it is:** A unique identifier for your Discord application

**Used for:**
- Building OAuth2 URLs
- Creating bot invite links
- Identifying your app in API requests

**In this project:**
- Used by `generate_invite.py` to create your bot invite URL
- Not used by the main bot code
- Stored for reference and future features

**Example usage:**
```python
invite_url = f"https://discord.com/api/oauth2/authorize?client_id={APP_ID}&permissions=..."
```

**Security:** 🟡 Public - it's okay if others see this (it's in your invite URL anyway)

---

### 3️⃣ Client Secret (Not Used ❌)

**What it is:** A secret key for OAuth2 authentication

**Used for:**
- Building web apps where users "Login with Discord"
- Server-side OAuth2 flows
- Exchanging authorization codes for access tokens

**In this project:**
- **Not currently used** - the bot doesn't have a web interface
- Stored in `.env` for potential future features
- Would be needed if you build a web dashboard

**Example future usage:**
```python
# If you built a web dashboard with Discord login
response = requests.post('https://discord.com/api/oauth2/token', data={
    'client_id': APP_ID,
    'client_secret': CLIENT_SECRET,
    'grant_type': 'authorization_code',
    'code': auth_code
})
```

**Security:** 🔒 **Keep secret!** This is like a password for OAuth2.

---

### 4️⃣ Public Key (Not Used ❌)

**What it is:** A cryptographic key for verifying HTTP interactions

**Used for:**
- Verifying that HTTP requests actually came from Discord
- Required if you host slash commands via HTTP instead of Gateway
- Validating interaction webhooks

**In this project:**
- **Not currently used** - the bot uses Gateway API (websocket), not HTTP
- Stored in `.env` for reference
- Would be needed if you switch to HTTP-based interactions

**Example future usage:**
```python
# If using HTTP interactions instead of Gateway
from nacl.signing import VerifyKey
verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
verify_key.verify(signature, body)
```

**Security:** 🟢 Public - it's meant to be shared (it's for verification, not authentication)

---

## Summary Table

| Credential | Required? | Used In Bot? | Purpose | Security Level |
|------------|-----------|--------------|---------|----------------|
| **Bot Token** | ✅ YES | ✅ YES | Authenticate bot to Discord | 🔒 SECRET |
| **Application ID** | ⚠️ Optional | ⚠️ Partially | Generate invite URLs | 🟡 Public |
| **Client Secret** | ❌ No | ❌ No | OAuth2 web login | 🔒 SECRET |
| **Public Key** | ❌ No | ❌ No | Verify HTTP interactions | 🟢 Public |

---

## How This Bot Works

This bot uses **Discord's Gateway API** (websocket connection), which means:

1. Bot connects to Discord using the **Bot Token**
2. Discord sends events (messages, commands) through the websocket
3. Bot responds through the same connection
4. No HTTP endpoints needed
5. No OAuth2 login needed

This is the **simplest and most common** way to build a Discord bot!

---

## When Would You Need The Other Keys?

### Application ID
- ✅ **Now**: Generating bot invite URLs
- 🔮 **Future**: OAuth2 features, analytics

### Client Secret
- 🔮 **Future**: If you build a web dashboard where users login with Discord
- 🔮 **Future**: If you want to access user data via OAuth2

### Public Key
- 🔮 **Future**: If you switch from Gateway to HTTP-based interactions
- 🔮 **Future**: If you build a webhook endpoint for Discord

---

## Best Practices

### ✅ DO:
- Store all credentials in `.env` file
- Add `.env` to `.gitignore` (already done)
- Keep Bot Token and Client Secret private
- Use environment variables in your code

### ❌ DON'T:
- Commit `.env` to Git
- Share your Bot Token or Client Secret
- Hardcode credentials in your code
- Post credentials in Discord or public forums

---

## What If My Token Gets Leaked?

If your Bot Token is exposed:

1. Go to [Discord Developer Portal](https://discord.com/developers/applications/1435854356720123904)
2. Go to "Bot" section
3. Click "Reset Token"
4. Copy the new token
5. Update your `.env` file
6. Restart the bot

The old token will stop working immediately.

---

## Quick Reference

**To run the bot:**
```bash
# Only need Bot Token in .env
python bot.py
```

**To generate invite URL:**
```bash
# Needs Application ID in .env
python generate_invite.py
```

**To verify setup:**
```bash
# Checks all credentials and files
python verify_setup.py
```

---

## Questions?

- **"Why store keys I don't use?"** - For future features and easy reference
- **"Is Application ID secret?"** - No, it's public (visible in invite URLs)
- **"Can I delete Client Secret/Public Key?"** - Yes, but keep them for future use
- **"What if I lose my Bot Token?"** - Reset it in the Developer Portal

---

**Remember: Only the Bot Token is required to run this bot! 🏈**
