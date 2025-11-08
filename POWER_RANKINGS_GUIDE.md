# ⚡ Power Rankings System

## Overview

Your league now has an **automated power rankings system** that updates as players report their game results!

---

## 🎮 How It Works

### **For Players:**

Players report their own game results using a simple command:

```
/report_my_game week:1 my_score:28 opponent_abbr:KC opponent_score:21
```

### **What Happens:**
1. ✅ Game is recorded
2. ✅ Standings are updated automatically
3. ✅ Head-to-head record is saved
4. ✅ Power rankings recalculate
5. ✅ Player sees win/loss confirmation

---

## 📋 Commands

### **1. `/report_my_game`** (Everyone)
Report your game result

**Parameters:**
- `week` - Week number (e.g., 1, 2, 3)
- `my_score` - Your score (e.g., 28)
- `opponent_abbr` - Opponent's team abbreviation (e.g., KC, BUF, LAC)
- `opponent_score` - Opponent's score (e.g., 21)

**Example:**
```
/report_my_game week:1 my_score:35 opponent_abbr:BUF opponent_score:28
```

**Result (if you won):**
```
🎉 Victory!
Kansas City Chiefs 35 - 28 Buffalo Bills

Week: 1
Your Record: 1-0

Game recorded! Check /power_rankings to see updated standings.
```

**Result (if you lost):**
```
😔 Defeat
Kansas City Chiefs 21 - 28 Buffalo Bills

Week: 1
Your Record: 0-1

Game recorded! Check /power_rankings to see updated standings.
```

---

### **2. `/power_rankings`** (Everyone)
View the power rankings

**Shows:**
- Rank (1-32)
- Team abbreviation
- Record (W-L)
- Points For (PF)
- Points Against (PA)
- Point Differential (+/-)

**Example Output:**
```
⚡ Power Rankings
Rankings based on record, head-to-head, and point differential

#   Team                Record    PF    PA    Diff  
----------------------------------------------------
1   KC                  3-0       84    56    +28   
2   BUF                 3-0       91    70    +21   
3   LAC                 2-1       77    63    +14   
4   LV                  2-1       70    63    +7    
5   CIN                 0-3       42    77    -35   

📊 Tiebreaker Rules
1️⃣ Best Record
2️⃣ Head-to-Head Result
3️⃣ Point Differential

Season 1 - Week 3
```

---

## 🏆 Ranking System

### **Tiebreaker Order:**

#### **1. Best Record** (Primary)
Team with more wins ranks higher

**Example:**
- Team A: 3-0 → Rank #1
- Team B: 2-1 → Rank #2

---

#### **2. Head-to-Head** (If tied in record)
If two teams have the same record AND have played each other, the winner ranks higher

**Example:**
- Team A: 2-1 (beat Team B)
- Team B: 2-1 (lost to Team A)
- **Result:** Team A ranks higher

---

#### **3. Point Differential** (If no head-to-head)
If two teams have the same record but haven't played each other, use point differential

**Example:**
- Team A: 2-1, +15 point diff
- Team B: 2-1, +10 point diff
- **Result:** Team A ranks higher

---

## 📊 Automatic Updates

### **When Teams Register:**
- Teams automatically show as 0-0
- Appear in power rankings immediately
- Ready to report games

### **When Games Are Reported:**
- ✅ Wins/Losses updated
- ✅ Points For/Against updated
- ✅ Point differential recalculated
- ✅ Head-to-head record saved
- ✅ Rankings re-sorted with tiebreakers

---

## 🎯 Usage Examples

### **Example 1: Report a Win**
```
Player: /report_my_game week:1 my_score:31 opponent_abbr:LV opponent_score:24

Bot Response:
🎉 Victory!
Kansas City Chiefs 31 - 24 Las Vegas Raiders

Week: 1
Your Record: 1-0
```

### **Example 2: Report a Loss**
```
Player: /report_my_game week:2 my_score:17 opponent_abbr:BUF opponent_score:28

Bot Response:
😔 Defeat
Kansas City Chiefs 17 - 28 Buffalo Bills

Week: 2
Your Record: 1-1
```

### **Example 3: Check Rankings**
```
Player: /power_rankings

Bot shows:
1. BUF (2-0, +25 diff)
2. KC (1-1, +7 diff)
3. LV (0-2, -32 diff)
```

---

## 🔒 Validation

### **Prevents:**
- ❌ Playing against yourself
- ❌ Reporting ties (must have a winner)
- ❌ Invalid team abbreviations
- ❌ Users without registered teams

### **Allows:**
- ✅ Any score
- ✅ Any week number
- ✅ Multiple games per week
- ✅ Games in any order

---

## 💡 Pro Tips

### **For Players:**

1. **Check abbreviations** with `/teams` or `/available_teams`
2. **Report games promptly** after playing
3. **Double-check scores** before submitting
4. **Use correct week number** for tracking

### **For Admins:**

1. **Admins can still use** `/report_game` for manual entry
2. **Monitor** `/recent_games` for accuracy
3. **Set week** with `/advance_week` after each week
4. **Both systems work together** (admin + player reporting)

---

## 📈 Tiebreaker Scenarios

### **Scenario 1: Clear Winner**
```
Team A: 3-0
Team B: 2-1
Team C: 1-2

Rankings: A, B, C (by record)
```

### **Scenario 2: Head-to-Head Tiebreaker**
```
Team A: 2-1 (beat Team B in Week 2)
Team B: 2-1 (lost to Team A in Week 2)
Team C: 1-2

Rankings: A, B, C
(A ranks above B due to head-to-head win)
```

### **Scenario 3: Point Differential Tiebreaker**
```
Team A: 2-1, +18 point diff (haven't played B)
Team B: 2-1, +12 point diff (haven't played A)
Team C: 1-2, -5 point diff

Rankings: A, B, C
(A ranks above B due to better point differential)
```

### **Scenario 4: Three-Way Tie**
```
Team A: 2-1, +10 (beat B, lost to C)
Team B: 2-1, +8 (lost to A, beat C)
Team C: 2-1, +15 (beat A, lost to B)

Rankings: C, A, B
(No clear head-to-head, so point differential decides)
```

---

## 🔄 Data Tracked

### **Per Team:**
- Wins
- Losses
- Points For
- Points Against
- Point Differential

### **Per Game:**
- Week played
- Winner/Loser
- Scores
- Date/Time
- Team abbreviations

### **Head-to-Head:**
- Who beat whom
- Used for tiebreakers
- Tracks all matchups

---

## 🎮 Player Workflow

```
1. Join league → Register team
   ↓
2. Play game in Madden
   ↓
3. Report result: /report_my_game week:1 my_score:28 opponent_abbr:KC opponent_score:21
   ↓
4. See confirmation (Win/Loss)
   ↓
5. Check rankings: /power_rankings
   ↓
6. Repeat for next game!
```

---

## 📁 Files Created

The bot automatically creates and manages:
- `data/games.json` - All game records
- `data/head_to_head.json` - Head-to-head matchups
- `data/standings.json` - Updated with each game
- `data/teams.json` - Team registrations

---

## 🔄 Restart Required

After adding these features, restart the bot:

```bash
# Stop (Ctrl+C)
python bot.py
```

You should see: `Synced 24 command(s)` (was 22 before)

---

## ✅ Quick Test

### **Test the System:**

1. **Register 2 teams:**
   ```
   /register_team team_name:Chiefs abbreviation:KC
   /assign_team user:@Friend team_name:Bills abbreviation:BUF
   ```

2. **Check initial rankings:**
   ```
   /power_rankings
   
   Both teams show 0-0
   ```

3. **Report a game:**
   ```
   /report_my_game week:1 my_score:28 opponent_abbr:BUF opponent_score:21
   ```

4. **Check updated rankings:**
   ```
   /power_rankings
   
   KC: 1-0 (Rank #1)
   BUF: 0-1 (Rank #2)
   ```

---

## 🆚 vs. Admin Report

### **Player Command (`/report_my_game`):**
- ✅ Players report their own games
- ✅ Simple: just enter your score and opponent
- ✅ Automatic win/loss detection
- ✅ Shows personalized confirmation
- ✅ Empowers players

### **Admin Command (`/report_game`):**
- ✅ Admins report any game
- ✅ Requires selecting both users
- ✅ Good for corrections
- ✅ Good for offline games
- ✅ Admin oversight

**Both work together!** Players can self-report, admins can fix errors.

---

## 🎯 Summary

✅ **Players report games** with `/report_my_game`  
✅ **Automatic standings** update  
✅ **Power rankings** with smart tiebreakers  
✅ **Head-to-head tracking** for accuracy  
✅ **Point differential** as final tiebreaker  
✅ **Real-time updates** after each game  

**Your league now has a professional ranking system! 🏈**
