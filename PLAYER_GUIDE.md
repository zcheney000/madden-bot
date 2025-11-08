# 🏈 Yessirski League - Player Guide

**Welcome to the league! Here's everything you need to know.**

---

## 🚀 Getting Started

### **Step 1: Join the Discord**
You're already here! ✅

### **Step 2: Join the Madden League**
In Madden, search for the league:
- **League Name:** `Yessirski`
- **Password:** `Ballin5`

### **Step 3: Pick Your Team**
Check which teams are available:
```
/available_teams
```

### **Step 4: Register Your Team**
Register in Discord:
```
/register_team team_name:Kansas City Chiefs abbreviation:KC
```

**That's it! You're in the league!** 🎉

---

## 📋 Essential Commands

### **Check Available Teams**
```
/available_teams
```
Shows all 32 NFL teams with ✅ (available) or ❌ (taken)

---

### **Register Your Team**
```
/register_team team_name:Kansas City Chiefs abbreviation:KC
```
- Use the **full team name** (e.g., Kansas City Chiefs)
- Use the **2-3 letter abbreviation** (e.g., KC)

**Examples:**
```
/register_team team_name:Buffalo Bills abbreviation:BUF
/register_team team_name:Los Angeles Chargers abbreviation:LAC
/register_team team_name:Dallas Cowboys abbreviation:DAL
```

---

### **View Your Team**
```
/my_team
```
Shows:
- Your team name
- Your record (W-L)
- Points for/against
- Point differential

---

### **View All Teams**
```
/teams
```
See everyone's teams and their owners

---

## 🎮 Playing Games

### **After You Play a Game:**

Report your result with this command:
```
/report_my_game week:1 my_score:28 opponent_abbr:KC opponent_score:21
```

**Parameters:**
- `week` - Current week number (ask admin if unsure)
- `my_score` - Your score
- `opponent_abbr` - Opponent's team abbreviation (e.g., KC, BUF, LAC)
- `opponent_score` - Their score

**Examples:**

**If you won 35-28 against the Bills in Week 1:**
```
/report_my_game week:1 my_score:35 opponent_abbr:BUF opponent_score:28
```

**If you lost 21-31 against the Chiefs in Week 2:**
```
/report_my_game week:2 my_score:21 opponent_abbr:KC opponent_score:31
```

**What happens:**
- ✅ Your record updates automatically
- ✅ Standings update
- ✅ Power rankings recalculate
- ✅ You see a win/loss confirmation

---

## 📊 Checking Standings

### **View Standings**
```
/standings
```
Shows everyone's record, points, and ranking

---

### **View Power Rankings**
```
/power_rankings
```
Shows rankings with smart tiebreakers:
1. **Best record** (most wins)
2. **Head-to-head** (if you played each other)
3. **Point differential** (if no head-to-head)

---

### **View Recent Games**
```
/recent_games
```
See the last 5 games played in the league

---

## 🆘 Need Help?

### **Get Command List**
```
/help
```
Shows all available commands

---

### **Ask in Discord**
- **#commish-assistance** - Ask the commissioners
- **#general** - Ask other players

---

## 📖 Quick Reference

### **Most Used Commands:**

| Command | What It Does |
|---------|--------------|
| `/available_teams` | See which teams are open |
| `/register_team` | Register your team |
| `/my_team` | View your team info |
| `/report_my_game` | Report a game result |
| `/power_rankings` | See rankings |
| `/standings` | See standings |

---

## 🎯 Common Questions

### **Q: How do I find team abbreviations?**
A: Use `/teams` or `/available_teams` - abbreviations are shown in parentheses (e.g., KC, BUF)

### **Q: What if I enter the wrong score?**
A: Contact an admin - they can fix it with `/report_game`

### **Q: Can I change my team?**
A: Contact an admin - they can reassign teams

### **Q: What week are we on?**
A: Check `/league_info` or ask in #general

### **Q: Do I report wins AND losses?**
A: Yes! Report every game you play (win or loss)

### **Q: What if my opponent doesn't report?**
A: You can report it! The system knows who won/lost based on scores

---

## 📝 Step-by-Step: Your First Game

### **Before the Game:**
1. Check your matchup (ask admin or check schedule)
2. Note your opponent's abbreviation (`/teams`)
3. Note the current week (`/league_info`)

### **Play the Game:**
4. Play your Madden game
5. Note the final score

### **After the Game:**
6. Report the result:
   ```
   /report_my_game week:1 my_score:35 opponent_abbr:BUF opponent_score:28
   ```

7. Check your updated record:
   ```
   /my_team
   ```

8. Check the rankings:
   ```
   /power_rankings
   ```

**Done!** 🎉

---

## 🏆 Example Game Flow

```
You: /available_teams
Bot: Shows Bills are available ✅

You: /register_team team_name:Buffalo Bills abbreviation:BUF
Bot: Team registered! 🏈

[Week 1 - You play against Chiefs]

You: /report_my_game week:1 my_score:31 opponent_abbr:KC opponent_score:28
Bot: 🎉 Victory! Buffalo Bills 31 - 28 Kansas City Chiefs
     Your Record: 1-0

You: /power_rankings
Bot: Shows you ranked #1! ⚡

[Week 2 - You play against Chargers]

You: /report_my_game week:2 my_score:21 opponent_abbr:LAC opponent_score:24
Bot: 😔 Defeat. Buffalo Bills 21 - 24 Los Angeles Chargers
     Your Record: 1-1

You: /my_team
Bot: Shows your 1-1 record and stats
```

---

## 💡 Pro Tips

### **For Success:**

1. **Report games promptly** - Don't forget after playing!
2. **Double-check abbreviations** - Use `/teams` to verify
3. **Check rankings often** - See where you stand
4. **Ask questions** - Use #commish-assistance
5. **Have fun!** - It's a game! 🏈

### **Common Mistakes:**

❌ **Wrong:** `/report_my_game week:1 my_score:28 opponent_abbr:Chiefs opponent_score:21`
- Don't use full team name for opponent

✅ **Right:** `/report_my_game week:1 my_score:28 opponent_abbr:KC opponent_score:21`
- Use abbreviation (KC)

---

❌ **Wrong:** `/register_team team_name:Chiefs abbreviation:KC`
- Use full team name

✅ **Right:** `/register_team team_name:Kansas City Chiefs abbreviation:KC`
- Full name required

---

## 🎮 Command Templates

### **Copy & Paste These:**

**Register Team:**
```
/register_team team_name:FULL_TEAM_NAME abbreviation:ABR
```

**Report Win:**
```
/report_my_game week:WEEK_# my_score:YOUR_SCORE opponent_abbr:OPP_ABR opponent_score:THEIR_SCORE
```

**Check Your Team:**
```
/my_team
```

**Check Rankings:**
```
/power_rankings
```

---

## 📱 Quick Start Checklist

- [ ] Joined Madden league (Yessirski / Ballin5)
- [ ] Checked available teams (`/available_teams`)
- [ ] Registered my team (`/register_team`)
- [ ] Verified registration (`/my_team`)
- [ ] Checked current week (`/league_info`)
- [ ] Ready to play! 🏈

---

## 🔗 Important Channels

- **#welcome-message** - Start here
- **#league-rules** - Read the rules
- **#team-owners** - See all registered teams
- **#general** - Chat with everyone
- **#commish-assistance** - Get help from admins

---

## 🎯 Summary

### **To Join:**
1. `/available_teams` - Pick a team
2. `/register_team` - Register it

### **To Play:**
1. Play your Madden game
2. `/report_my_game` - Report the result

### **To Check:**
1. `/my_team` - Your stats
2. `/power_rankings` - See rankings
3. `/standings` - See standings

---

**That's all you need to know! Welcome to Yessirski League! 🏈**

**Questions? Ask in #commish-assistance!**
