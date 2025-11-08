# 🏈 Madden Franchise League Discord Bot

A comprehensive Discord bot for managing your Madden franchise league, including team registration, standings tracking, game results, and more!

## Features

### 🎮 Team Management
- **Register Teams**: Players can register their teams with custom names and abbreviations
- **View Teams**: See all registered teams and their owners
- **Team Info**: Check your team's record and stats

### 🏆 Standings & Stats
- **League Standings**: Automatically tracked wins, losses, points for/against
- **Point Differential**: Track scoring margins
- **Recent Games**: View recent game results

### 📊 League Management (Admin Only)
- **Report Games**: Record game results and automatically update standings
- **Advance Week**: Move the league to the next week
- **Season Management**: Track multiple seasons
- **League Reset**: Start fresh when needed

## Setup Instructions

### 1. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Under "Privileged Gateway Intents", enable:
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent
5. Click "Reset Token" and copy your bot token (keep this secret!)

### 2. Invite Bot to Your Server

1. In the Developer Portal, go to "OAuth2" → "URL Generator"
2. Select scopes:
   - ✅ `bot`
   - ✅ `applications.commands`
3. Select bot permissions:
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Read Message History
   - ✅ Use Slash Commands
4. Copy the generated URL and open it in your browser
5. Select your server and authorize the bot

### 3. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 4. Configure the Bot

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Discord credentials:
   ```env
   DISCORD_BOT_TOKEN=your_bot_token_here
   DISCORD_APPLICATION_ID=your_application_id_here
   DISCORD_CLIENT_SECRET=your_client_secret_here
   DISCORD_PUBLIC_KEY=your_public_key_here
   ```

   **Note**: Only `DISCORD_BOT_TOKEN` is required. The others are optional and stored for future features.

3. **Quick Invite Link**: Run `python generate_invite.py` to get your bot invite URL

### 5. Set Up Admin Role

1. In your Discord server, create a role called "League Admin"
2. Assign this role to league commissioners/admins
3. (Optional) You can change the admin role name in `data/config.json` after first run

### 6. Run the Bot

```bash
python bot.py
```

You should see:
```
[Bot Name] has connected to Discord!
Bot is in X guild(s)
Synced X command(s)
```

## Commands

### Player Commands
- `/register_team <team_name> <abbreviation>` - Register your team in the league
- `/teams` - View all registered teams
- `/my_team` - View your team information
- `/standings` - View league standings
- `/recent_games [count]` - View recent game results (default: 5)
- `/league_info` - View league information
- `/help` - View all available commands

### Admin Commands (Requires "League Admin" role)
- `/report_game <winner> <loser> <winner_score> <loser_score>` - Report a game result
- `/advance_week` - Advance to the next week
- `/set_season <season>` - Set the current season number
- `/reset_league` - Reset all league data (use with caution!)

## Usage Example

### Starting a New League

1. **Players Register Teams**:
   ```
   /register_team team_name:Chiefs abbreviation:KC
   /register_team team_name:49ers abbreviation:SF
   ```

2. **Admin Reports Game Results**:
   ```
   /report_game winner:@Player1 loser:@Player2 winner_score:28 loser_score:21
   ```

3. **Check Standings**:
   ```
   /standings
   ```

4. **Advance to Next Week**:
   ```
   /advance_week
   ```

## Data Storage

The bot stores all data in JSON files in the `data/` directory:
- `teams.json` - Team registrations
- `standings.json` - Win/loss records and stats
- `schedule.json` - Game results history
- `config.json` - League settings (season, week, admin role)

## API Keys Explained

### 🔑 What Each Credential Does

| Credential | Purpose | Required? | Used In This Bot |
|------------|---------|-----------|------------------|
| **Bot Token** | Authenticates your bot to Discord's API | ✅ **YES** | Logs the bot into Discord |
| **Application ID** | Identifies your app (same as Client ID) | ⚠️ Optional | For generating invite URLs |
| **Client Secret** | OAuth2 authentication for web apps | ❌ No | Not used (no web login feature) |
| **Public Key** | Verifies HTTP interactions from Discord | ❌ No | Not used (using Gateway API) |

### Why Store All Keys?

Even though only the **Bot Token** is required right now, storing all credentials in `.env` is useful for:
- **Future Features**: If you add OAuth2 login or HTTP interactions later
- **Reference**: Easy access to your app's credentials
- **Invite URLs**: Application ID is needed for bot invite links

The bot currently uses Discord's **Gateway API** (websocket connection), which only needs the bot token. The other credentials would be needed if you build additional features like:
- Web dashboard with Discord login (needs Client Secret)
- HTTP-based slash commands (needs Public Key)
- Advanced OAuth2 flows (needs Application ID + Client Secret)

## Customization

You can customize the bot by editing `data/config.json`:
```json
{
    "league_name": "Your League Name",
    "season": 1,
    "week": 1,
    "admin_role": "League Admin"
}
```

## Troubleshooting

### Bot doesn't respond to commands
- Make sure the bot has proper permissions in your server
- Check that slash commands are enabled
- Wait a few minutes for commands to sync after first startup

### "Missing Permissions" error
- Ensure the bot role has necessary permissions
- Check that the bot can read/send messages in the channel

### Commands not showing up
- Try running `/help` to trigger command sync
- Restart the bot
- Check Discord's server settings → Integrations

## Support

For issues or questions, please check:
1. Make sure all dependencies are installed
2. Verify your bot token is correct in `.env`
3. Check that the bot has proper permissions
4. Review the console output for error messages

## Future Features (Ideas)

- Schedule generation
- Player stats tracking
- Trade management
- Draft system
- Weekly matchup notifications
- Playoff bracket generation
- Awards and achievements

---

**Enjoy your Madden Franchise League! 🏈**
