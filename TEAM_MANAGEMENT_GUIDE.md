# 🔄 Team Management Commands (Admin)

## New Admin Features

You can now manage team ownership directly from Discord!

---

## 📋 Commands

### **1. `/reassign_team`**
Transfer a team from one Discord user to another

**Usage:**
```
/reassign_team current_owner:@OldPlayer new_owner:@NewPlayer
```

**What it does:**
- Transfers the team to the new owner
- Updates team ownership in the database
- Transfers their standings/stats
- Updates the #team-owners roster
- Keeps the team name and abbreviation

**Example:**
```
/reassign_team current_owner:@John new_owner:@Mike
```

**Result:**
```
🔄 Team Reassigned!
Kansas City Chiefs (KC) has been transferred!

Previous Owner: @John
New Owner: @Mike
```

---

### **2. `/remove_team`**
Remove a team from the league completely

**Usage:**
```
/remove_team user:@PlayerName
```

**What it does:**
- Removes the team from the league
- Deletes their standings/stats
- Updates the #team-owners roster
- Makes the team available again

**Example:**
```
/remove_team user:@John
```

**Result:**
```
🗑️ Team Removed!
Kansas City Chiefs (KC) has been removed from the league.

Previous Owner: @John
Total Teams: 31
```

---

## 🎮 Use Cases

### **Scenario 1: Player Leaves, New Player Joins**
```
# Player leaves Discord
/remove_team user:@OldPlayer

# New player joins and wants that team
# They register normally
/register_team team_name:Kansas City Chiefs abbreviation:KC
```

### **Scenario 2: Transfer Team Without Removing**
```
# Player can't play anymore, friend takes over
/reassign_team current_owner:@OldPlayer new_owner:@NewPlayer

# Team, stats, and record all transfer!
```

### **Scenario 3: Wrong Person Registered**
```
# Someone registered the wrong team
/remove_team user:@WrongPerson

# They can now register the correct team
```

---

## ⚠️ Important Notes

### **Reassign Team:**
- ✅ Keeps team name and abbreviation
- ✅ Transfers all stats and standings
- ✅ New owner gets full control
- ❌ New owner must NOT already have a team
- ❌ Current owner must have a team

### **Remove Team:**
- ✅ Completely removes team from league
- ✅ Team becomes available again
- ✅ Updates roster immediately
- ⚠️ **Deletes all stats/standings** (can't be undone!)

---

## 🔒 Permissions

**Who can use these commands:**
- Only users with the "League Admin" role
- Configured in your bot settings

**Who can't use these:**
- Regular team owners
- Members without admin role

---

## 📊 What Gets Updated

When you reassign or remove a team:

### **Automatically Updated:**
1. ✅ `teams.json` - Team ownership
2. ✅ `standings.json` - Stats/records
3. ✅ `#team-owners` channel - Roster display
4. ✅ `/available_teams` - Shows team as available (if removed)
5. ✅ `/teams` command - Updated team list

### **NOT Updated (Manual):**
- Private team channels (you may want to update permissions)
- Game schedule (if games were already scheduled)

---

## 🎯 Examples

### **Example 1: Season Restart**
```
# Remove all inactive players
/remove_team user:@Player1
/remove_team user:@Player2
/remove_team user:@Player3

# Check available teams
/available_teams

# New players register
(They use /register_team normally)
```

### **Example 2: Trade Teams**
```
# Player A has Chiefs, Player B has Raiders
# They want to swap

# Remove both teams
/remove_team user:@PlayerA
/remove_team user:@PlayerB

# They re-register with swapped teams
@PlayerA: /register_team team_name:Las Vegas Raiders abbreviation:LV
@PlayerB: /register_team team_name:Kansas City Chiefs abbreviation:KC
```

### **Example 3: Friend Takes Over**
```
# Player going on vacation, friend covers
/reassign_team current_owner:@PlayerA new_owner:@Friend

# After vacation, reassign back
/reassign_team current_owner:@Friend new_owner:@PlayerA
```

---

## 🔧 Troubleshooting

### **Error: "doesn't have a registered team"**
- The mentioned user doesn't own a team
- Check with `/teams` to see who owns what

### **Error: "already has a team registered"**
- The new owner already has a team
- Use `/remove_team` on their current team first
- Or choose a different new owner

### **Team not updating in roster**
- Wait a few seconds
- Check #team-owners channel
- Try `/update_teams_roster` to force refresh

---

## 💡 Pro Tips

### **For Admins:**

1. **Before removing a team**, note their stats if you want to keep records
2. **Use reassign** instead of remove when possible (keeps stats)
3. **Check `/teams`** before reassigning to see current owners
4. **Announce changes** in your league chat
5. **Update private channels** manually if needed

### **Best Practices:**

- **Document trades/changes** in a league log
- **Announce reassignments** so everyone knows
- **Be careful with `/remove_team`** - it deletes stats!
- **Use `/reassign_team`** for temporary transfers

---

## 📋 Command Summary

| Command | What It Does | Keeps Stats? |
|---------|--------------|--------------|
| `/reassign_team` | Transfer team to new owner | ✅ Yes |
| `/remove_team` | Delete team from league | ❌ No |
| `/register_team` | Register new team | N/A |

---

## 🔄 Restart Required

After adding these commands, restart the bot:

```bash
# Stop (Ctrl+C)
python bot.py
```

You should see: `Synced 21 command(s)` (was 19 before)

---

## ✅ Quick Test

1. **Restart bot**
2. **Try:** `/reassign_team current_owner:@You new_owner:@AltAccount`
3. **Check:** #team-owners should update
4. **Verify:** `/teams` shows new owner
5. **Test remove:** `/remove_team user:@AltAccount`
6. **Check:** `/available_teams` shows team available

---

**You can now manage team ownership easily! 🏈**
