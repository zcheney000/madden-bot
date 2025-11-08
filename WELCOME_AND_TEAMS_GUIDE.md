# 👋 Welcome Message & Available Teams Guide

## New Features Added!

Your bot now has a complete onboarding system with:
1. **Welcome Message** - Auto-posted guide for new members
2. **Available Teams Checker** - See which NFL teams are available
3. **Division Browser** - Filter teams by division

---

## 🎯 New Commands

### **For Everyone:**

#### `/available_teams`
View ALL 32 NFL teams with availability status

**Shows:**
- ✅ Available teams (green checkmark)
- ❌ Taken teams (red X)
- Team abbreviations
- Organized by AFC/NFC and divisions
- Count of available teams

**Example output:**
```
🏈 Available NFL Teams

AFC (American Football Conference)

AFC East
✅ Buffalo Bills (BUF)
❌ Miami Dolphins (MIA)
✅ New England Patriots (NE)
✅ New York Jets (NYJ)

...

24/32 teams available
```

---

#### `/available_by_division`
View teams in a specific division

**Choose from:**
- AFC East, AFC North, AFC South, AFC West
- NFC East, NFC North, NFC South, NFC West

**Shows:**
- Available teams in that division
- Taken teams in that division
- Count of available vs total

**Example:**
```
/available_by_division division:AFC West

🏈 AFC West

Available:
✅ Denver Broncos (DEN)
✅ Las Vegas Raiders (LV)
✅ Los Angeles Chargers (LAC)

Taken:
❌ Kansas City Chiefs (KC)

3/4 teams available in this division
```

---

### **For Admins:**

#### `/post_welcome`
Posts a beautiful welcome message to `#welcome-message` channel

**The message includes:**
1. 📜 Step 1: Read the Rules
2. 🔍 Step 2: Check Available Teams (with `/available_teams`)
3. 📝 Step 3: Register Your Team
4. 💬 Step 4: Join the Community
5. ❓ Need Help section

**Usage:**
```
/post_welcome
```

**When to use:**
- After running `/setup_league`
- When starting a new season
- To refresh the welcome message

---

## 📋 Complete Onboarding Flow

### **For New Members:**

1. **Join Discord server**
2. **Read welcome message** in `#welcome-message`
3. **Check rules** in `#league-rules`
4. **Use `/available_teams`** to see what's available
5. **Register with `/register_team`**
6. **Auto-posted to `#teams` channel**

### **For Admins:**

1. **Set up channels:**
   ```
   /setup_league
   ```

2. **Post welcome message:**
   ```
   /post_welcome
   ```

3. **Members join and register**

4. **Check who joined:**
   ```
   /teams
   ```

---

## 🏈 NFL Teams Database

The bot includes all 32 NFL teams organized by division:

### **AFC**
- **AFC East:** Bills, Dolphins, Patriots, Jets
- **AFC North:** Ravens, Bengals, Browns, Steelers
- **AFC South:** Texans, Colts, Jaguars, Titans
- **AFC West:** Broncos, Chiefs, Raiders, Chargers

### **NFC**
- **NFC East:** Cowboys, Giants, Eagles, Commanders
- **NFC North:** Bears, Lions, Packers, Vikings
- **NFC South:** Falcons, Panthers, Saints, Buccaneers
- **NFC West:** Cardinals, Rams, 49ers, Seahawks

Each team has its official abbreviation (e.g., KC, SF, DAL).

---

## 🎮 Example Usage Session

### **Admin Setup:**
```
# 1. Create all channels
/setup_league

# 2. Post welcome message
/post_welcome

# 3. Post current teams (if any)
/post_all_teams
```

### **New Member Joins:**
```
# 1. Read welcome message (in #welcome-message)

# 2. Check available teams
/available_teams

# 3. Filter by division if needed
/available_by_division division:NFC West

# 4. Register team
/register_team team_name:San Francisco 49ers abbreviation:SF
```

### **Check Status:**
```
# See all teams
/teams

# See available teams
/available_teams

# Check standings
/standings
```

---

## 🎨 Customization

### **Change Welcome Message:**

Edit the welcome message in `bot.py` around line 948:

```python
welcome_embed = discord.Embed(
    title="🏈 Welcome to the Madden Franchise League!",  # ← Change title
    description="Ready to join the action? Follow these steps to get started!",  # ← Change description
    color=discord.Color.blue()  # ← Change color
)

# Add/edit fields:
welcome_embed.add_field(
    name="📜 Step 1: Read the Rules",
    value="Your custom text here...",
    inline=False
)
```

### **Add/Remove NFL Teams:**

Edit the `NFL_TEAMS` dictionary around line 28:

```python
NFL_TEAMS = {
    "AFC East": ["Buffalo Bills", "Miami Dolphins", ...],
    # Add custom divisions or teams here
}
```

### **Change Team Abbreviations:**

Edit `TEAM_ABBREVIATIONS` around line 40:

```python
TEAM_ABBREVIATIONS = {
    "Buffalo Bills": "BUF",
    # Customize abbreviations here
}
```

---

## 💡 Pro Tips

### **For Admins:**

1. **Pin the welcome message** in `#welcome-message`
2. **Post `/available_teams` regularly** to keep members updated
3. **Use `/post_all_teams`** weekly to update the roster
4. **Make `#welcome-message` read-only** for regular members

### **For Members:**

1. **Use `/available_by_division`** to narrow your search
2. **Check team abbreviations** before registering
3. **Register with full team name** for clarity
4. **Use the suggested abbreviation** from the available teams list

---

## 🔄 How It Works

### **Team Availability:**
- Bot compares registered teams with NFL teams database
- Matches are case-insensitive
- Shows real-time availability
- Updates automatically when teams register

### **Welcome Message:**
- Uses Discord embeds for beautiful formatting
- Links to other channels (auto-detects)
- Includes step-by-step instructions
- Can be re-posted anytime

### **Division Filtering:**
- Uses Discord's choice system (dropdown)
- Shows only 4 teams per division
- Easier to read than full list
- Perfect for mobile users

---

## 📊 Command Summary

| Command | Who | What |
|---------|-----|------|
| `/available_teams` | Everyone | View all 32 NFL teams |
| `/available_by_division` | Everyone | View teams by division |
| `/post_welcome` | Admin | Post welcome message |
| `/register_team` | Everyone | Register your team |
| `/teams` | Everyone | View registered teams |

---

## 🔄 Restart Required

After updating the code, restart the bot:

```bash
# Stop (Ctrl+C)
python bot.py
```

You should see: `Synced 19 command(s)` (was 16 before)

---

## 🎯 Quick Start Checklist

- [ ] Restart bot to load new commands
- [ ] Run `/setup_league` (if not done)
- [ ] Run `/post_welcome` in Discord
- [ ] Test `/available_teams`
- [ ] Test `/available_by_division`
- [ ] Have a member test registration
- [ ] Verify auto-post to `#teams` works

---

**Your league now has a complete onboarding system! 🏈**
