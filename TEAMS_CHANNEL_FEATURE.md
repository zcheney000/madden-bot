# 📋 Teams Channel Feature

## What's New?

The bot now automatically posts team registrations to a `#teams` channel!

---

## 🎯 How It Works

### **When Someone Registers:**

```
/register_team team_name:Chiefs abbreviation:KC
```

**The bot will:**
1. ✅ Register the team (as before)
2. 📢 **Automatically post to #teams channel** with:
   - Team name and abbreviation
   - Owner's Discord name and mention
   - Total number of teams

---

## 📝 Example

When a player registers, this appears in `#teams`:

```
🏈 New Team Registered!

Team: Chiefs (KC)
Owner: @JohnDoe (JohnDoe#1234)
Total Teams: 5
```

---

## 🏗️ Setup

### **Option 1: Create with `/setup_league`**

The `#teams` channel is now automatically created when you run:
```
/setup_league
```

It will be in the **👥 League Members** category.

### **Option 2: Create Manually**

If you already ran `/setup_league`, just create a channel named exactly:
```
teams
```

The bot will find it automatically!

---

## 📊 New Admin Command: `/post_all_teams`

Post all currently registered teams to the `#teams` channel at once!

**Usage:**
```
/post_all_teams
```

**What it does:**
- Creates a nice embed with ALL registered teams
- Shows team name, abbreviation, and owner
- Perfect for updating the channel after multiple registrations

**Example output:**
```
🏈 All Registered Teams
Total Teams: 3

KC - Chiefs
Owner: @Player1 (Player1#1234)

SF - 49ers
Owner: @Player2 (Player2#5678)

DAL - Cowboys
Owner: @Player3 (Player3#9012)
```

---

## 🎮 Workflow Examples

### **Starting Fresh:**

1. **Admin sets up channels:**
   ```
   /setup_league
   ```

2. **Players register teams:**
   ```
   /register_team team_name:Chiefs abbreviation:KC
   /register_team team_name:49ers abbreviation:SF
   ```
   *(Each registration automatically posts to #teams)*

3. **Done!** The #teams channel is automatically updated.

---

### **If You Already Have Teams:**

1. **Create #teams channel** (if not exists)

2. **Post all existing teams:**
   ```
   /post_all_teams
   ```

3. **Future registrations** will auto-post!

---

## ⚙️ Technical Details

### **Channel Name:**
- Must be exactly: `teams` (lowercase, no spaces)
- Bot searches for this name automatically

### **Permissions:**
- Bot needs "Send Messages" permission in #teams
- Bot needs "Embed Links" permission

### **Location:**
- Created in **👥 League Members** category by `/setup_league`
- Can be moved anywhere, bot finds it by name

### **What Gets Posted:**
- Team name
- Team abbreviation (3 letters)
- Owner's Discord mention
- Owner's Discord username
- Total team count
- Timestamp

---

## 🔧 Customization

Want to change what gets posted? Edit this section in `bot.py`:

```python
# Around line 150
announcement_embed = discord.Embed(
    title="🏈 New Team Registered!",  # ← Change title
    color=discord.Color.blue()  # ← Change color
)
announcement_embed.add_field(name="Team", value=f"**{team_name}** ({abbreviation.upper()})", inline=False)
announcement_embed.add_field(name="Owner", value=f"{interaction.user.mention} ({interaction.user.name})", inline=False)
# Add more fields here if you want!
```

---

## 💡 Tips

### **Keep #teams Clean:**
- Consider making it read-only for regular members
- Only bot and admins can post
- Members can see all registrations

### **Pin Important Messages:**
- Pin the "All Registered Teams" message
- Update it weekly with `/post_all_teams`

### **Use for Announcements:**
- Bot posts there automatically
- Great place for team-related news

---

## 🎯 Commands Summary

| Command | Who Can Use | What It Does |
|---------|-------------|--------------|
| `/register_team` | Everyone | Register team + auto-post to #teams |
| `/post_all_teams` | Admin | Post all teams to #teams at once |
| `/setup_league` | Admin | Creates #teams channel (and others) |

---

## 🔄 Restart Required

After updating the bot code, restart it:

```bash
# Stop the bot (Ctrl+C)
python bot.py
```

You should see: `Synced 16 command(s)` (was 15 before)

---

**Your #teams channel will now stay automatically updated! 🏈**
