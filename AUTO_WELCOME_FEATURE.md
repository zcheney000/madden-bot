# 👋 Auto-Welcome Message Feature

## What's New?

The bot now **automatically sends a welcome message** when someone joins your Discord server!

---

## 🎯 Features

### **1. Automatic Welcome on Join**
- When a new member joins the server
- Bot automatically posts to `#welcome-message` channel
- Mentions the new member
- Shows league credentials and steps

### **2. Updated Welcome Message**
Includes:
- ⚠️ **30-minute timer warning**
- 🎮 **League credentials** (Name: AlphaMales, Password: NoFire1)
- 📜 Steps to join and register
- 🔍 Available teams command
- ❓ Help information

---

## 📋 Welcome Message Format

```
🏈 Welcome to AʟᴘʜᴀMᴀʟᴇs Gʀᴏᴜᴘ!

Hey @NewMember, Welcome to AʟᴘʜᴀMᴀʟᴇs Gʀᴏᴜᴘ!

⚠️ YOU HAVE 30 MINUTES to complete the steps below 
or the team will be filled with another user!

🎮 STEP 1: JOIN LEAGUE VIA SEARCH
LEAGUE NAME: AlphaMales
PASSWORD: NoFire1

📜 STEP 2: Read the Rules
Head over to #league-rules...

🔍 STEP 3: Check Available Teams
Use /available_teams...

📝 STEP 4: Register Your Team
Once you've picked a team, register with:
/register_team team_name:Kansas City Chiefs abbreviation:KC

💬 STEP 5: Join the Community
Check out #general-chat...

❓ Need Help?
Ask questions in #commish-assistance...

⏰ Remember: 30 minutes to complete registration!
```

---

## 🚀 How It Works

### **Automatic (When Member Joins):**
1. New member joins Discord server
2. Bot detects the join event
3. Bot finds `#welcome-message` channel
4. Bot posts personalized welcome message
5. Member sees their @mention and instructions

### **Manual (Admin Command):**
```
/post_welcome
```
Posts a general welcome message (without specific @mention)

---

## ⚙️ Setup Requirements

### **1. Channel Name**
- Must have a channel named: `welcome-message`
- Created automatically by `/setup_league`
- Or create manually

### **2. Bot Permissions**
- Send Messages in #welcome-message
- Embed Links
- Mention @everyone, @here, and All Roles

### **3. Member Intent**
- Already enabled in bot setup
- Required to detect new members joining

---

## 🎮 Testing

### **Test the Auto-Welcome:**
1. **Restart the bot:**
   ```bash
   python bot.py
   ```

2. **Have someone join the server** (or leave and rejoin)

3. **Check #welcome-message** - should see the welcome message

### **Test Manual Welcome:**
```
/post_welcome
```

---

## 🎨 Customization

### **Change League Credentials:**

Edit line 124 in `bot.py`:
```python
value="**LEAGUE NAME:** `AlphaMales`\n**PASSWORD:** `NoFire1`",
```

Change to:
```python
value="**LEAGUE NAME:** `YourLeagueName`\n**PASSWORD:** `YourPassword`",
```

### **Change Timer Duration:**

Edit line 118:
```python
description=f"Hey {member.mention}, Welcome to AʟᴘʜᴀMᴀʟᴇs Gʀᴏᴜᴘ!\n\n⚠️ **YOU HAVE 30 MINUTES**..."
```

Change `30 MINUTES` to your preferred time.

### **Change League Name:**

Edit lines 117 and 118:
```python
title="🏈 Welcome to AʟᴘʜᴀMᴀʟᴇs Gʀᴏᴜᴘ!",
description=f"Hey {member.mention}, Welcome to AʟᴘʜᴀMᴀʟᴇs Gʀᴏᴜᴘ!..."
```

### **Add/Remove Steps:**

Add more fields:
```python
embed.add_field(
    name="🆕 STEP 6: Your Custom Step",
    value="Your instructions here...",
    inline=False
)
```

---

## 💡 Pro Tips

### **For Admins:**

1. **Pin the welcome message** for easy reference
2. **Test with an alt account** before going live
3. **Update credentials** if you change league password
4. **Monitor #welcome-message** for new joins

### **For Members:**

1. **Read the entire message** before starting
2. **Note the 30-minute timer**
3. **Join the Madden league first** (Step 1)
4. **Then register in Discord** (Step 4)

---

## 🔧 Troubleshooting

### **Welcome Message Not Sending:**

**Check:**
- Bot is running
- `#welcome-message` channel exists
- Bot has "Send Messages" permission
- Member intent is enabled (already done)

**Test:**
```python
# In bot.py, check line 14-16:
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # ← This must be True
```

### **Message Sends But No @Mention:**

- This is normal for `/post_welcome` command
- Auto-welcome (on join) includes @mention
- Manual command doesn't mention anyone

### **Channel Links Not Working:**

- Make sure channels exist: `#league-rules`, `#general-chat`, `#commish-assistance`
- Discord auto-detects channel names in `<#channel-name>` format

---

## 📊 Events Summary

| Event | Trigger | Action |
|-------|---------|--------|
| `on_member_join` | New member joins server | Send welcome with @mention |
| `/post_welcome` | Admin runs command | Send general welcome message |

---

## 🔄 Restart Required

After making changes, restart the bot:

```bash
# Stop (Ctrl+C)
python bot.py
```

---

## ✅ Quick Test Checklist

- [ ] Bot restarted
- [ ] `#welcome-message` channel exists
- [ ] Test join (or use `/post_welcome`)
- [ ] Message appears with correct info
- [ ] League credentials are correct
- [ ] All channel links work
- [ ] Timer warning is visible

---

**Your bot now welcomes new members automatically with league info! 🏈**
