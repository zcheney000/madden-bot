# 👑 Yessirski League - Admin Guide

**Complete guide for league commissioners and admins.**

---

## 🚀 Initial Setup

### **Step 1: Set Up All Channels**
```
/setup_league
```
Creates all league channels and categories automatically:
- 📊 LEAGUE INFO (announcements, power-rankings, etc.)
- 💰 Upgrade Opportunities
- 🏆 League Members (team-owners, general)
- 🎙️ Voice Channels

---

### **Step 2: Post Welcome Message**
```
/post_welcome
```
Posts the welcome message to #welcome-message with:
- League name: Yessirski
- Password: Ballin5
- Instructions for new members

---

### **Step 3: Update Teams Roster**
```
/update_teams_roster
```
Creates/updates the pinned teams roster in #team-owners

---

## 📋 Essential Admin Commands

### **League Management**

#### **Announce Sim Advance**
```
/announce_sim sim_type:Regular Season Week week:5
```
Posts @everyone announcement to #announcements

**Sim Types:**
- `Regular Season Week` - Requires week number
- `Playoffs` - No week needed
- `Offseason` - No week needed
- `Draft` - No week needed

**Examples:**
```
/announce_sim sim_type:Regular Season Week week:1
/announce_sim sim_type:Playoffs
/announce_sim sim_type:Offseason
/announce_sim sim_type:Draft
```

---

#### **Advance Week**
```
/advance_week
```
Manually advances to the next week (increments by 1)

---

#### **Set Season**
```
/set_season season:2
```
Sets the current season number

---

### **Team Management**

#### **Assign Team to User**
```
/assign_team user:@PlayerName team_name:Kansas City Chiefs abbreviation:KC
```
Register a team for any Discord user (even if they haven't done it themselves)

**Use when:**
- New member needs help registering
- You want to pre-assign teams
- Someone can't figure out the command

---

#### **Reassign Team to New Owner**
```
/reassign_team current_owner:@OldPlayer new_owner:@NewPlayer
```
Transfer a team from one user to another

**Use when:**
- Player leaves league
- Team ownership changes
- Need to swap teams

---

#### **Remove Team**
```
/remove_team user:@PlayerName
```
Removes a team from the league entirely

**Use when:**
- Player quits
- Need to free up a team
- Correcting mistakes

---

### **Game Reporting**

#### **Report Game (Admin)**
```
/report_game week:1 winner:@Player1 loser:@Player2 winner_score:28 loser_score:21
```
Report a game result for any two players

**Use when:**
- Players can't/won't report
- Fixing incorrect reports
- Manually entering results
- Offline games

**Note:** Players can report their own games with `/report_my_game`

---

### **Channel Management**

#### **Post Power Rankings**
```
/post_power_rankings
```
Manually posts power rankings to #power-rankings channel

**Use when:**
- Want to refresh rankings
- After fixing game errors
- Initial setup

**Note:** Rankings auto-update when players use `/report_my_game`

---

#### **Update Teams Roster**
```
/update_teams_roster
```
Updates the pinned teams list in #team-owners

**Use when:**
- Teams are added/removed
- Need to refresh the list
- After reassignments

---

#### **Post Welcome Message**
```
/post_welcome
```
Posts welcome message to #welcome-message

**Use when:**
- Initial setup
- Message gets unpinned
- Need to refresh info

---

#### **Create Team Channel**
```
/create_team_channel user:@PlayerName
```
Creates a private channel for a specific team

---

#### **Create All Team Channels**
```
/create_all_team_channels
```
Creates private channels for ALL registered teams at once

---

### **League Data**

#### **Reset League**
```
/reset_league
```
⚠️ **DANGER:** Resets ALL league data (teams, standings, games, etc.)

**Use when:**
- Starting a new season
- Testing/development
- Complete restart needed

**Warning:** This cannot be undone!

---

## 🎯 Common Admin Workflows

### **Weekly Sim Routine**

```
1. Sim to next week in Madden
2. /announce_sim sim_type:Regular Season Week week:5
3. Wait for players to play games
4. Check #power-rankings for auto-updates
5. Verify all games reported
6. Repeat next week
```

---

### **New Member Joins**

```
1. Member joins Discord (auto welcome message sent)
2. Member picks team and uses /register_team
   OR
   You use: /assign_team user:@NewMember team_name:Chiefs abbreviation:KC
3. /update_teams_roster (updates the list)
4. /create_team_channel user:@NewMember (optional)
```

---

### **Player Leaves League**

```
1. /remove_team user:@LeavingPlayer
2. /update_teams_roster
3. Announce team is available
4. New player can register that team
```

---

### **Transfer Team Ownership**

```
1. /reassign_team current_owner:@OldPlayer new_owner:@NewPlayer
2. /update_teams_roster
3. Notify both players
```

---

### **Fix Incorrect Game Report**

```
Option 1: Delete and re-report
(Currently no delete command - would need manual data edit)

Option 2: Report correct game
/report_game week:1 winner:@CorrectWinner loser:@CorrectLoser winner_score:28 loser_score:21
```

---

### **Start of Playoffs**

```
1. Regular season ends in Madden
2. /announce_sim sim_type:Playoffs
3. Monitor playoff games
4. Players report results to you
5. You manually track bracket
```

---

### **Offseason Management**

```
1. Season ends
2. /announce_sim sim_type:Offseason
3. Players manage rosters in Madden
4. Free agency period
5. Prepare for draft
```

---

### **Draft Day**

```
1. /announce_sim sim_type:Draft
2. Conduct draft in Madden
3. Players make selections
4. After draft: /announce_sim sim_type:Regular Season Week week:1
5. Start new season!
```

---

## 📊 Monitoring Commands

### **View League Info**
```
/league_info
```
Shows current season, week, and team count

---

### **View Standings**
```
/standings
```
See all team records and stats

---

### **View Power Rankings**
```
/power_rankings
```
See rankings with tiebreakers

---

### **View Recent Games**
```
/recent_games
```
See last 5 games reported

---

### **View All Teams**
```
/teams
```
See all registered teams and owners

---

## 🔧 Troubleshooting

### **Commands Not Showing Up**

**Solution:**
1. Restart the bot
2. Wait 1-2 minutes for Discord to sync
3. Try restarting Discord client
4. Check bot has proper permissions

---

### **Power Rankings Not Updating**

**Solution:**
1. Check #power-rankings channel exists
2. Run `/post_power_rankings` manually
3. Verify bot has "Send Messages" permission
4. Check if games are being reported correctly

---

### **Welcome Message Not Sending**

**Solution:**
1. Check #welcome-message channel exists
2. Verify bot has "Send Messages" permission
3. Run `/post_welcome` manually
4. Check bot is online

---

### **Player Can't Register Team**

**Solution:**
1. Check if team is already taken (`/teams`)
2. Verify they're using correct team name
3. Use `/assign_team` to register for them
4. Check bot permissions

---

### **@everyone Not Working in Announcements**

**Solution:**
1. Check bot has "Mention @everyone" permission
2. Verify in #announcements channel settings
3. Check server-wide bot permissions

---

## 💡 Pro Tips

### **Best Practices:**

1. **Announce before simming** - Give 24hr notice when possible
2. **Consistent schedule** - Sim same day/time each week
3. **Monitor reports** - Check `/recent_games` regularly
4. **Update rosters** - Run `/update_teams_roster` after changes
5. **Pin important messages** - Pin sim announcements
6. **Backup data** - Save `data/` folder periodically

### **Communication:**

1. **Use #announcements** - For all official league news
2. **Use #commish-assistance** - For player questions
3. **Use #general** - For casual chat
4. **DM for issues** - Private matters

### **Organization:**

1. **Track deadlines** - Set game deadlines
2. **Monitor activity** - Check who's playing
3. **Enforce rules** - Be consistent
4. **Stay active** - Respond to questions

---

## 🎮 Admin Command Quick Reference

| Command | What It Does | When to Use |
|---------|--------------|-------------|
| `/announce_sim` | Announce sim advance | Every sim |
| `/assign_team` | Register team for user | New members |
| `/reassign_team` | Transfer team | Ownership change |
| `/remove_team` | Delete team | Player quits |
| `/report_game` | Report any game | Manual entry |
| `/post_power_rankings` | Update rankings | Force refresh |
| `/update_teams_roster` | Update team list | After changes |
| `/post_welcome` | Post welcome msg | Setup/refresh |
| `/advance_week` | Increment week | Manual advance |
| `/set_season` | Set season number | New season |
| `/setup_league` | Create all channels | Initial setup |
| `/reset_league` | ⚠️ Delete all data | New league |

---

## 📁 Data Files

The bot stores data in `data/` folder:

- `teams.json` - All registered teams
- `standings.json` - Win/loss records
- `games.json` - All game results
- `head_to_head.json` - H2H matchups
- `config.json` - League settings
- `schedule.json` - Game schedule

**Backup regularly!** Copy the `data/` folder to save league state.

---

## 🔒 Permissions Needed

### **Bot Permissions:**
- ✅ Send Messages
- ✅ Embed Links
- ✅ Attach Files
- ✅ Read Message History
- ✅ Mention @everyone
- ✅ Manage Messages (for pinning)
- ✅ Manage Channels (for setup)

### **Admin Role:**
- ✅ "League Admin" role (configurable in `config.json`)
- ✅ All admin commands require this role

---

## 🎯 Season Management

### **Start of Season:**
```
1. /reset_league (if new league)
2. /setup_league (if new server)
3. /set_season season:1
4. /post_welcome
5. Wait for team registrations
6. /announce_sim sim_type:Regular Season Week week:1
```

### **During Season:**
```
1. Weekly: /announce_sim sim_type:Regular Season Week week:X
2. Monitor game reports
3. Check /power_rankings
4. Answer questions in #commish-assistance
```

### **End of Season:**
```
1. /announce_sim sim_type:Playoffs
2. Manage playoff bracket
3. Crown champion! 🏆
4. /announce_sim sim_type:Offseason
5. /announce_sim sim_type:Draft
6. /set_season season:2
7. /announce_sim sim_type:Regular Season Week week:1
```

---

## ✅ Admin Checklist

### **Daily:**
- [ ] Check #commish-assistance for questions
- [ ] Monitor game reports
- [ ] Respond to player issues

### **Weekly:**
- [ ] Announce sim advance
- [ ] Verify all games reported
- [ ] Check power rankings
- [ ] Update any team changes

### **Monthly:**
- [ ] Backup data folder
- [ ] Review league rules
- [ ] Check for inactive players
- [ ] Plan special events

### **Seasonal:**
- [ ] Announce playoffs
- [ ] Manage offseason
- [ ] Conduct draft
- [ ] Start new season

---

## 🆘 Need Help?

### **Bot Issues:**
1. Check bot is online
2. Verify permissions
3. Restart bot
4. Check error logs

### **Player Issues:**
1. Use `/assign_team` to help
2. Explain commands clearly
3. Point to PLAYER_GUIDE.md
4. Be patient and helpful

### **League Issues:**
1. Communicate clearly
2. Be consistent with rules
3. Stay organized
4. Have fun! 🏈

---

## 🎯 Summary

✅ **Setup:** `/setup_league` creates everything  
✅ **Sims:** `/announce_sim` alerts members  
✅ **Teams:** `/assign_team`, `/reassign_team`, `/remove_team`  
✅ **Games:** `/report_game` for manual entry  
✅ **Updates:** Auto-updates for most things  
✅ **Monitoring:** Check standings, rankings, games  
✅ **Communication:** Use #announcements for official news  

**You have all the tools to run a professional league! 🏈👑**

---

**Questions? Check `/help` or refer to this guide!**
