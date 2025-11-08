# 🏗️ Channel Setup Guide

## New Features Added!

Your bot can now automatically create and manage Discord channels for your league!

---

## 🚀 Quick Start

### **Step 1: Re-invite Bot with New Permissions**

The bot needs "Manage Channels" permission. Run this:

```bash
python generate_invite.py
```

Then:
1. **Kick the bot** from your server (right-click → Kick)
2. **Use the new invite URL** from the terminal
3. **Authorize** the bot with the new permissions

### **Step 2: Restart the Bot**

```bash
python bot.py
```

Wait for it to sync (should now show 15 commands instead of 12)

---

## 📋 New Commands

### **`/setup_league`** (Admin Only)

Creates the complete league structure based on your example:

**Creates:**
- 📊 **LEAGUE INFO** category
  - commish-assistance
  - madden-polls
  - announcements
  - weekly-recap
  - general-chat
  - power-rankings
  - breaking-news
  - league-scores

- 💰 **Upgrade Opportunities** category
  - gotw-potw
  - annual-active-award
  - streaming-channel

- 🚨 **Join League** category
  - welcome-message
  - league-rules

- 🔊 **Voice Channels** category
  - Lobby (voice)
  - GOTW Gaming (voice)

- 👥 **League Members** category
  - team-owners

**Usage:**
```
/setup_league
```

**Note:** This creates ~20+ channels, so it takes 10-15 seconds!

---

### **`/create_team_channel`** (Admin Only)

Creates a **private channel** for a specific team.

**Features:**
- Only the team owner can see it
- Admins can also see it
- Perfect for team strategy/notes

**Usage:**
```
/create_team_channel team_owner:@Player channel_name:chiefs-hq
```

**Example:**
```
/create_team_channel team_owner:@John
```
This creates `#kc-hq` (uses team abbreviation)

---

### **`/create_all_team_channels`** (Admin Only)

Creates private channels for **ALL registered teams** at once!

**Usage:**
```
/create_all_team_channels
```

**What it does:**
- Finds all registered teams
- Creates a private channel for each (e.g., `#kc-hq`, `#sf-hq`)
- Only team owner can see their channel
- Sends welcome message in each channel

---

## 🎯 Recommended Workflow

### **For a New League:**

1. **Set up channels first:**
   ```
   /setup_league
   ```

2. **Players register teams:**
   ```
   /register_team team_name:Chiefs abbreviation:KC
   /register_team team_name:49ers abbreviation:SF
   ```

3. **Create team channels:**
   ```
   /create_all_team_channels
   ```

4. **Start playing!**

---

### **For Adding One Team:**

1. **Player registers:**
   ```
   /register_team team_name:Cowboys abbreviation:DAL
   ```

2. **Admin creates their channel:**
   ```
   /create_team_channel team_owner:@NewPlayer
   ```

---

## 🎨 Customization Ideas

You can customize the channels created by editing `bot.py`:

### **Change Channel Names:**
Find this section in `bot.py`:
```python
commish_channel = await guild.create_text_channel(
    "commish-assistance",  # ← Change this
    category=league_category,
    topic="Need help? Ask the commissioners here!"  # ← And this
)
```

### **Add More Channels:**
Copy and paste a channel creation block:
```python
new_channel = await guild.create_text_channel(
    "your-channel-name",
    category=league_category,
    topic="Your channel description"
)
created_channels.append(f"#{new_channel.name}")
```

### **Change Category Names:**
```python
league_category = await guild.create_category("📊 LEAGUE INFO")  # ← Change emoji/name
```

---

## ⚠️ Important Notes

### **Permissions Required:**
- Bot needs **"Manage Channels"** permission
- Admin commands require **"League Admin"** role

### **Channel Limits:**
- Discord servers have a 500 channel limit
- `/setup_league` creates ~20 channels
- Plan accordingly for large leagues!

### **Existing Channels:**
- `/setup_league` will create new channels even if some exist
- `/create_all_team_channels` skips channels that already exist
- Be careful not to run `/setup_league` multiple times!

### **Deleting Channels:**
- Bot doesn't auto-delete channels
- Manually delete unwanted channels in Discord
- Or use Discord's built-in channel management

---

## 🔧 Troubleshooting

### **"Missing Permissions" Error**
- Make sure bot has "Manage Channels" permission
- Re-invite bot using `python generate_invite.py`

### **Commands Don't Show Up**
- Restart the bot
- Wait 2-3 minutes for sync
- Check bot has `applications.commands` scope

### **Channels Created in Wrong Place**
- Discord creates channels at the bottom by default
- Drag categories to reorder them
- Or delete and re-run `/setup_league`

### **Team Channel Not Private**
- Check channel permissions in Discord settings
- Only team owner and bot should have access
- Admins can manually adjust permissions

---

## 📊 Channel Structure Overview

```
Your Server
├─ 📊 LEAGUE INFO
│  ├─ #commish-assistance
│  ├─ #madden-polls
│  ├─ #announcements
│  ├─ #weekly-recap
│  ├─ #general-chat
│  ├─ #power-rankings
│  ├─ #breaking-news
│  └─ #league-scores
│
├─ 💰 Upgrade Opportunities
│  ├─ #gotw-potw
│  ├─ #annual-active-award
│  └─ #streaming-channel
│
├─ 🚨 Join League 🚨
│  ├─ #welcome-message
│  └─ #league-rules
│
├─ 🔊 Voice Channels
│  ├─ 🔊 Lobby
│  └─ 🔊 GOTW Gaming
│
├─ 👥 League Members
│  └─ #team-owners
│
└─ 🏈 Team Channels (created separately)
   ├─ #kc-hq (private)
   ├─ #sf-hq (private)
   └─ #dal-hq (private)
```

---

## 🎮 Example Usage Session

```bash
# 1. Generate new invite with permissions
python generate_invite.py

# 2. Kick bot, re-invite with new URL

# 3. Restart bot
python bot.py
```

Then in Discord:

```
# Admin sets up league
/setup_league

# Players join
/register_team team_name:Chiefs abbreviation:KC
/register_team team_name:49ers abbreviation:SF

# Admin creates team channels
/create_all_team_channels

# Check everything
/teams
/league_info
```

---

**Your league is now fully set up with organized channels! 🏈**
