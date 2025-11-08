# 📋 Teams Roster System - Updated!

## What Changed?

The `#teams` channel now maintains a **single pinned message** that shows all teams in a clean list format:

```
📋 League Teams Roster

#buf - @PlayerName
#kc - @PlayerName  
#sf - @PlayerName
#dal - @PlayerName

Total Teams: 4 | Last Updated: [timestamp]
```

---

## 🎯 How It Works

### **Automatic Updates:**
- When someone registers with `/register_team`, the roster **automatically updates**
- The bot finds the pinned message and edits it
- If no pinned message exists, it creates one and pins it
- Teams are sorted alphabetically by abbreviation

### **Format:**
- **#abbreviation** - @DiscordMention
- Example: **#kc** - @JohnDoe

---

## 📝 Commands

### **For Everyone:**
- `/register_team` - Register your team (auto-updates roster)

### **For Admins:**
- `/update_teams_roster` - Manually update/create the roster
- Use this if the roster gets out of sync

---

## 🚀 Setup

### **First Time:**

1. **Create #teams channel** (or run `/setup_league`)

2. **Initialize the roster:**
   ```
   /update_teams_roster
   ```

3. **Done!** Future registrations will auto-update

---

### **If You Already Have Teams:**

1. **Run the update command:**
   ```
   /update_teams_roster
   ```

2. **The bot will:**
   - Create a new pinned message with all teams
   - Format: #abbreviation - @mention
   - Sort alphabetically

---

## 💡 Features

### **Pinned Message:**
- Bot creates ONE message and pins it
- Updates the same message each time
- No spam in the channel!

### **Auto-Sorting:**
- Teams sorted by abbreviation (A-Z)
- Easy to find specific teams

### **Live Updates:**
- Updates immediately when someone registers
- Shows Discord mentions (clickable)
- Timestamp shows last update

### **Handles Large Leagues:**
- Splits into multiple fields if >20 teams
- Shows "Teams (1-20)", "Teams (21-32)", etc.

---

## 🎮 Example Flow

### **Admin Setup:**
```
/setup_league
  → Creates #teams channel

/update_teams_roster
  → Creates pinned roster message
```

### **Players Register:**
```
Player1: /register_team team_name:Kansas City Chiefs abbreviation:KC
  → Roster updates to show: #kc - @Player1

Player2: /register_team team_name:San Francisco 49ers abbreviation:SF
  → Roster updates to show:
    #kc - @Player1
    #sf - @Player2

Player3: /register_team team_name:Buffalo Bills abbreviation:BUF
  → Roster updates to show (sorted):
    #buf - @Player3
    #kc - @Player1
    #sf - @Player2
```

---

## 🔧 Technical Details

### **How It Finds the Message:**
1. Looks for pinned messages in #teams
2. Finds message from bot with title "📋 League Teams Roster"
3. Edits that message
4. If not found, creates new one

### **Permissions Needed:**
- Send Messages
- Embed Links
- Manage Messages (for pinning)

### **What Gets Shown:**
- Team abbreviation (lowercase with #)
- Discord mention (clickable @username)
- Total team count
- Last updated timestamp

---

## 📊 What It Looks Like

```
📋 League Teams Roster
All registered teams and their owners:

Teams
#buf - @Player1
#chi - @Player2
#dal - @Player3
#den - @Player4
#det - @Player5
#gb - @Player6
#kc - @Player7
#lac - @Player8
#lar - @Player9
#lv - @Player10
#mia - @Player11
#min - @Player12
#ne - @Player13
#no - @Player14
#nyg - @Player15
#nyj - @Player16
#phi - @Player17
#pit - @Player18
#sf - @Player19
#sea - @Player20

Total Teams: 20 | Last Updated
[timestamp]
```

---

## 🔄 Migration from Old System

If you were using the old system that posted individual messages:

1. **Clean up old messages** (optional - delete old announcements)

2. **Run the new command:**
   ```
   /update_teams_roster
   ```

3. **Pin the new message** (bot does this automatically)

4. **Future registrations** will update this message

---

## ⚠️ Important Notes

### **One Message Only:**
- Bot maintains ONE pinned message
- Don't manually create multiple roster messages
- If you want to refresh, just run `/update_teams_roster`

### **Pinning:**
- Bot automatically pins the message
- Don't unpin it - bot needs to find it to update
- If unpinned, bot will create a new one

### **Sorting:**
- Always sorted by abbreviation
- Can't customize sort order
- Makes it easy to find teams alphabetically

---

## 🎯 Commands Summary

| Command | Who | What |
|---------|-----|------|
| `/register_team` | Everyone | Register + auto-update roster |
| `/update_teams_roster` | Admin | Manually update roster |
| `/teams` | Everyone | View teams (command response) |

---

## 🔄 Restart Required

Restart the bot to load changes:

```bash
# Stop (Ctrl+C)
python bot.py
```

You should see: `Synced 19 command(s)`

---

## ✅ Quick Test

1. **Restart bot**
2. **Run:** `/update_teams_roster`
3. **Check #teams** - should see pinned roster
4. **Register a test team** - roster should update
5. **Check it's still pinned** ✓

---

**Your #teams channel now has a clean, auto-updating roster! 🏈**
