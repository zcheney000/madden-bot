import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
import database as db

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Data file paths
DATA_DIR = 'data'
TEAMS_FILE = os.path.join(DATA_DIR, 'teams.json')
SCHEDULE_FILE = os.path.join(DATA_DIR, 'schedule.json')
STANDINGS_FILE = os.path.join(DATA_DIR, 'standings.json')
CONFIG_FILE = os.path.join(DATA_DIR, 'config.json')
GAMES_FILE = os.path.join(DATA_DIR, 'games.json')
HEAD_TO_HEAD_FILE = os.path.join(DATA_DIR, 'head_to_head.json')
NFL_TEAMS_FILE = os.path.join(DATA_DIR, 'nfl_teams.json')

# NFL Teams Database
NFL_TEAMS = {
    "AFC East": ["Buffalo Bills", "Miami Dolphins", "New England Patriots", "New York Jets"],
    "AFC North": ["Baltimore Ravens", "Cincinnati Bengals", "Cleveland Browns", "Pittsburgh Steelers"],
    "AFC South": ["Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Tennessee Titans"],
    "AFC West": ["Denver Broncos", "Kansas City Chiefs", "Las Vegas Raiders", "Los Angeles Chargers"],
    "NFC East": ["Dallas Cowboys", "New York Giants", "Philadelphia Eagles", "Washington Commanders"],
    "NFC North": ["Chicago Bears", "Detroit Lions", "Green Bay Packers", "Minnesota Vikings"],
    "NFC South": ["Atlanta Falcons", "Carolina Panthers", "New Orleans Saints", "Tampa Bay Buccaneers"],
    "NFC West": ["Arizona Cardinals", "Los Angeles Rams", "San Francisco 49ers", "Seattle Seahawks"]
}

# Team abbreviations mapping
TEAM_ABBREVIATIONS = {
    "Buffalo Bills": "BUF", "Miami Dolphins": "MIA", "New England Patriots": "NE", "New York Jets": "NYJ",
    "Baltimore Ravens": "BAL", "Cincinnati Bengals": "CIN", "Cleveland Browns": "CLE", "Pittsburgh Steelers": "PIT",
    "Houston Texans": "HOU", "Indianapolis Colts": "IND", "Jacksonville Jaguars": "JAX", "Tennessee Titans": "TEN",
    "Denver Broncos": "DEN", "Kansas City Chiefs": "KC", "Las Vegas Raiders": "LV", "Los Angeles Chargers": "LAC",
    "Dallas Cowboys": "DAL", "New York Giants": "NYG", "Philadelphia Eagles": "PHI", "Washington Commanders": "WAS",
    "Chicago Bears": "CHI", "Detroit Lions": "DET", "Green Bay Packers": "GB", "Minnesota Vikings": "MIN",
    "Atlanta Falcons": "ATL", "Carolina Panthers": "CAR", "New Orleans Saints": "NO", "Tampa Bay Buccaneers": "TB",
    "Arizona Cardinals": "ARI", "Los Angeles Rams": "LAR", "San Francisco 49ers": "SF", "Seattle Seahawks": "SEA"
}

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Helper functions for data management
def load_json(filepath, default=None):
    """Load JSON data from file"""
    if default is None:
        default = {}
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return default

def save_json(filepath, data):
    """Save JSON data to file"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

# Hybrid helper functions (use database if available, otherwise JSON)
async def get_teams_data():
    """Get teams data from database or JSON"""
    if db.pool:
        return await db.get_all_teams()
    return load_json(TEAMS_FILE)

async def get_standings_data():
    """Get standings data from database or JSON"""
    if db.pool:
        return await db.get_all_standings()
    return load_json(STANDINGS_FILE)

async def get_config_data():
    """Get config data from database or JSON"""
    if db.pool:
        return await db.get_config()
    return load_json(CONFIG_FILE)

async def get_games_data():
    """Get games data from database or JSON"""
    if db.pool:
        return await db.get_all_games()
    return load_json(GAMES_FILE)

async def get_head_to_head_data():
    """Get head-to-head data from database or JSON"""
    if db.pool:
        return await db.get_all_head_to_head()
    return load_json(HEAD_TO_HEAD_FILE)

# Initialize data files
def init_data_files():
    """Initialize data files if they don't exist"""
    if not os.path.exists(TEAMS_FILE):
        save_json(TEAMS_FILE, {})
    if not os.path.exists(SCHEDULE_FILE):
        save_json(SCHEDULE_FILE, {"games": []})
    if not os.path.exists(STANDINGS_FILE):
        save_json(STANDINGS_FILE, {})
    if not os.path.exists(CONFIG_FILE):
        save_json(CONFIG_FILE, {
            "league_name": "Madden Franchise League",
            "season": 1,
            "week": 1,
            "admin_role": "League Admin"
        })
    if not os.path.exists(GAMES_FILE):
        save_json(GAMES_FILE, [])
    if not os.path.exists(HEAD_TO_HEAD_FILE):
        save_json(HEAD_TO_HEAD_FILE, {})

@bot.event
async def on_ready():
    """Bot startup event"""
    # Initialize database
    db_connected = await db.init_db()
    if db_connected:
        print('✅ Using Supabase database')
    else:
        print('⚠️  Using JSON files (DATABASE_URL not set)')
        init_data_files()
    
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} guild(s)')
    
    # Sync slash commands to all guilds
    try:
        # Sync to each guild first (faster)
        for guild in bot.guilds:
            bot.tree.copy_global_to(guild=guild)
            synced_guild = await bot.tree.sync(guild=guild)
            print(f'Synced {len(synced_guild)} command(s) to guild: {guild.name}')
        
        # Then sync globally
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s) globally')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

@bot.event
async def on_member_join(member):
    """Send welcome message when a new member joins"""
    # Find welcome-message channel
    welcome_channel = discord.utils.get(member.guild.text_channels, name="welcome-message")
    general_channel = discord.utils.get(member.guild.text_channels, name="general")
    
    if not welcome_channel:
        return
    
    try:
        # Send detailed welcome message to #welcome-message
        embed = discord.Embed(
            title="🏈 Welcome to Yessirski League!",
            description=f"Hey {member.mention}, Welcome to Yessirski League!\n\n⚠️ **YOU HAVE 30 MINUTES** to complete the steps below or the team will be filled with another user!",
            color=discord.Color.red()
        )
        
        embed.add_field(
            name="🎮 STEP 1: JOIN LEAGUE VIA SEARCH",
            value="**LEAGUE NAME:** `Yessirski`\n**PASSWORD:** `Ballin5`",
            inline=False
        )
        
        embed.add_field(
            name="📜 STEP 2: Read the Rules",
            value="Head over to <#league-rules> to read our league rules and guidelines.",
            inline=False
        )
        
        embed.add_field(
            name="🔍 STEP 3: Check Available Teams",
            value="Use `/available_teams` to see which NFL teams are still available. Pick your favorite!",
            inline=False
        )
        
        embed.add_field(
            name="📝 STEP 4: Register Your Team",
            value="Once you've picked a team, register with:\n`/register_team team_name:Kansas City Chiefs abbreviation:KC`",
            inline=False
        )
        
        embed.add_field(
            name="💬 STEP 5: Join the Community",
            value="Check out <#general-chat> to meet other league members!",
            inline=False
        )
        
        embed.add_field(
            name="❓ Need Help?",
            value="Ask questions in <#commish-assistance> and our commissioners will help you out!",
            inline=False
        )
        
        embed.set_footer(text="⏰ Remember: 30 minutes to complete registration!")
        embed.timestamp = datetime.utcnow()
        
        await welcome_channel.send(embed=embed)
        
        # Send notification to #general-chat
        if general_channel:
            await general_channel.send(
                f"👋 Welcome {member.mention}! Check out {welcome_channel.mention} to get started! ⏰ **30 minutes to register!**"
            )
    except discord.Forbidden:
        pass  # Bot doesn't have permission to post

# Admin check decorator
def is_admin():
    """Check if user has admin role"""
    async def predicate(interaction: discord.Interaction):
        config = await get_config_data()
        admin_role_name = config.get('admin_role', 'League Admin')
        return any(role.name == admin_role_name for role in interaction.user.roles)
    return app_commands.check(predicate)

# Helper function to update teams list in #team-owners channel
async def update_teams_list(guild):
    """Update or create the pinned teams list in #team-owners channel"""
    teams_channel = discord.utils.get(guild.text_channels, name="team-owners")
    if not teams_channel:
        return
    
    teams = await get_teams_data()
    
    # Create the teams list embed
    embed = discord.Embed(
        title="📋 League Teams Roster",
        description="All registered teams and their owners:",
        color=discord.Color.gold()
    )
    
    if teams:
        # Sort teams by abbreviation
        sorted_teams = sorted(teams.items(), key=lambda x: x[1]['abbreviation'])
        
        teams_list = []
        for user_id, team in sorted_teams:
            member = guild.get_member(int(user_id))
            if member:
                teams_list.append(f"**#{team['abbreviation'].lower()}** - {member.mention}")
            else:
                teams_list.append(f"**#{team['abbreviation'].lower()}** - {team['owner']}")
        
        # Split into chunks if too long
        chunk_size = 20
        for i in range(0, len(teams_list), chunk_size):
            chunk = teams_list[i:i+chunk_size]
            embed.add_field(
                name=f"Teams ({i+1}-{min(i+chunk_size, len(teams_list))})" if len(teams_list) > chunk_size else "Teams",
                value="\n".join(chunk),
                inline=False
            )
    else:
        embed.description = "No teams registered yet. Use `/register_team` to join!"
    
    embed.set_footer(text=f"Total Teams: {len(teams)} | Last Updated")
    embed.timestamp = datetime.utcnow()
    
    try:
        # Look for existing pinned message from bot
        bot_message = None
        
        async for pin in teams_channel.pins():
            if pin.author == guild.me and pin.embeds and pin.embeds[0].title == "📋 League Teams Roster":
                bot_message = pin
                break
        
        if bot_message:
            # Update existing message
            await bot_message.edit(embed=embed)
        else:
            # Create new message and pin it
            new_message = await teams_channel.send(embed=embed)
            await new_message.pin()
    except discord.Forbidden:
        pass  # Bot doesn't have permission
    except Exception as e:
        print(f"Error updating teams list: {e}")

# ==================== TEAM MANAGEMENT ====================

@bot.tree.command(name="register_team", description="Register your team in the league")
@app_commands.describe(
    team_name="Your team name",
    abbreviation="3-letter team abbreviation (e.g., KC, SF, DAL)"
)
async def register_team(interaction: discord.Interaction, team_name: str, abbreviation: str):
    """Register a team for the league"""
    teams = await get_teams_data()
    user_id = str(interaction.user.id)
    
    # Check if user already has a team
    if user_id in teams:
        await interaction.response.send_message(
            f"❌ You already have a team registered: **{teams[user_id]['name']}**",
            ephemeral=True
        )
        return
    
    # Check if abbreviation is already taken
    if any(team['abbreviation'].upper() == abbreviation.upper() for team in teams.values()):
        await interaction.response.send_message(
            f"❌ The abbreviation **{abbreviation.upper()}** is already taken!",
            ephemeral=True
        )
        return
    
    # Register the team
    if db.pool:
        # Use database
        success = await db.create_team(user_id, team_name, abbreviation.upper())
        if not success:
            await interaction.response.send_message(
                "❌ Failed to register team. Please try again.",
                ephemeral=True
            )
            return
    else:
        # Use JSON files
        teams[user_id] = {
            "name": team_name,
            "abbreviation": abbreviation.upper(),
            "owner": interaction.user.name,
            "owner_id": user_id
        }
        save_json(TEAMS_FILE, teams)
        
        # Initialize standings
        standings = load_json(STANDINGS_FILE)
        standings[user_id] = {
            "wins": 0,
            "losses": 0,
            "points_for": 0,
            "points_against": 0
        }
        save_json(STANDINGS_FILE, standings)
    
    embed = discord.Embed(
        title="🏈 Team Registered!",
        description=f"**{team_name}** ({abbreviation.upper()}) has joined the league!",
        color=discord.Color.green()
    )
    embed.add_field(name="Owner", value=interaction.user.mention, inline=True)
    embed.set_footer(text=f"Total Teams: {len(teams)}")
    
    await interaction.response.send_message(embed=embed)
    
    # Update the teams roster in #team-owners channel
    await update_teams_list(interaction.guild)

@bot.tree.command(name="reassign_team", description="Reassign a team to a different user (Admin only)")
@is_admin()
@app_commands.describe(
    current_owner="The current team owner (mention them)",
    new_owner="The new team owner (mention them)"
)
async def reassign_team(interaction: discord.Interaction, current_owner: discord.Member, new_owner: discord.Member):
    """Reassign a team from one user to another"""
    teams = await get_teams_data()
    standings = await get_standings_data()
    
    current_user_id = str(current_owner.id)
    new_user_id = str(new_owner.id)
    
    # Check if current owner has a team
    if current_user_id not in teams:
        await interaction.response.send_message(
            f"❌ {current_owner.mention} doesn't have a registered team!",
            ephemeral=True
        )
        return
    
    # Check if new owner already has a team
    if new_user_id in teams:
        await interaction.response.send_message(
            f"❌ {new_owner.mention} already has a team registered! Use `/remove_team` first if needed.",
            ephemeral=True
        )
        return
    
    # Get the team info
    team_info = teams[current_user_id]
    team_name = team_info['name']
    team_abbr = team_info['abbreviation']
    
    # Transfer team to new owner
    if db.pool:
        # Use database
        await db.delete_team(current_user_id)
        await db.create_team(new_user_id, team_name, team_abbr)
        # Transfer standings
        if current_user_id in standings:
            old_record = standings[current_user_id]
            await db.update_standing(
                new_user_id,
                old_record['wins'],
                old_record['losses'],
                old_record['points_for'],
                old_record['points_against']
            )
    else:
        # Use JSON files
        teams[new_user_id] = {
            "name": team_name,
            "abbreviation": team_abbr,
            "owner": new_owner.name,
            "owner_id": new_user_id
        }
        
        # Remove from old owner
        del teams[current_user_id]
        
        # Transfer standings if they exist
        if current_user_id in standings:
            standings[new_user_id] = standings[current_user_id]
            del standings[current_user_id]
        
        # Save changes
        save_json(TEAMS_FILE, teams)
        save_json(STANDINGS_FILE, standings)
    
    # Send confirmation
    embed = discord.Embed(
        title="🔄 Team Reassigned!",
        description=f"**{team_name}** ({team_abbr}) has been transferred!",
        color=discord.Color.blue()
    )
    embed.add_field(name="Previous Owner", value=current_owner.mention, inline=True)
    embed.add_field(name="New Owner", value=new_owner.mention, inline=True)
    
    await interaction.response.send_message(embed=embed)
    
    # Update the teams roster
    await update_teams_list(interaction.guild)

@bot.tree.command(name="remove_team_by_abbr", description="Remove a team by abbreviation (Admin only)")
@is_admin()
@app_commands.describe(abbreviation="Team abbreviation (e.g., KC, BUF)")
async def remove_team_by_abbr(interaction: discord.Interaction, abbreviation: str):
    """Remove a team from the league by abbreviation"""
    teams = await get_teams_data()
    
    # Find team by abbreviation
    team_user_id = None
    abbr_upper = abbreviation.upper()
    
    for user_id, team in teams.items():
        if team['abbreviation'].upper() == abbr_upper:
            team_user_id = user_id
            break
    
    if not team_user_id:
        await interaction.response.send_message(
            f"❌ No team found with abbreviation **{abbr_upper}**!",
            ephemeral=True
        )
        return
    
    # Get team info before removing
    team_info = teams[team_user_id]
    team_name = team_info['name']
    team_abbr = team_info['abbreviation']
    
    # Remove team
    if db.pool:
        await db.delete_team(team_user_id)
    else:
        del teams[team_user_id]
        standings = await get_standings_data()
        if team_user_id in standings:
            del standings[team_user_id]
        save_json(TEAMS_FILE, teams)
        save_json(STANDINGS_FILE, standings)
    
    # Send confirmation
    member = interaction.guild.get_member(int(team_user_id))
    owner_display = member.mention if member else f"User ID: {team_user_id}"
    
    embed = discord.Embed(
        title="🗑️ Team Removed!",
        description=f"**{team_name}** ({team_abbr}) has been removed from the league.",
        color=discord.Color.red()
    )
    embed.add_field(name="Previous Owner", value=owner_display, inline=True)
    embed.set_footer(text=f"Total Teams: {len(teams) - 1}")
    
    await interaction.response.send_message(embed=embed)
    
    # Update the teams roster
    await update_teams_list(interaction.guild)

@bot.tree.command(name="remove_team", description="Remove a team from the league (Admin only)")
@is_admin()
@app_commands.describe(user="The team owner to remove (mention them)")
async def remove_team(interaction: discord.Interaction, user: discord.Member):
    """Remove a team from the league"""
    teams = await get_teams_data()
    standings = await get_standings_data()
    
    user_id = str(user.id)
    
    # Check if user has a team
    if user_id not in teams:
        await interaction.response.send_message(
            f"❌ {user.mention} doesn't have a registered team!",
            ephemeral=True
        )
        return
    
    # Get team info before removing
    team_info = teams[user_id]
    team_name = team_info['name']
    team_abbr = team_info['abbreviation']
    
    # Remove team
    if db.pool:
        # Use database (standings will cascade delete)
        await db.delete_team(user_id)
    else:
        # Use JSON files
        del teams[user_id]
        
        # Remove standings if they exist
        if user_id in standings:
            del standings[user_id]
        
        # Save changes
        save_json(TEAMS_FILE, teams)
        save_json(STANDINGS_FILE, standings)
    
    # Send confirmation
    embed = discord.Embed(
        title="🗑️ Team Removed!",
        description=f"**{team_name}** ({team_abbr}) has been removed from the league.",
        color=discord.Color.red()
    )
    embed.add_field(name="Previous Owner", value=user.mention, inline=True)
    embed.set_footer(text=f"Total Teams: {len(teams)}")
    
    await interaction.response.send_message(embed=embed)
    
    # Update the teams roster
    await update_teams_list(interaction.guild)

@bot.tree.command(name="assign_team", description="Assign a team to a user (Admin only)")
@is_admin()
@app_commands.describe(
    user="The Discord user to assign the team to",
    team_name="Team name (e.g., Kansas City Chiefs)",
    abbreviation="3-letter team abbreviation (e.g., KC)"
)
async def assign_team(interaction: discord.Interaction, user: discord.Member, team_name: str, abbreviation: str):
    """Admin command to assign a team to any user"""
    teams = await get_teams_data()
    standings = await get_standings_data()
    
    user_id = str(user.id)
    
    # Check if user already has a team
    if user_id in teams:
        current_team = teams[user_id]
        await interaction.response.send_message(
            f"❌ {user.mention} already has a team: **{current_team['name']}** ({current_team['abbreviation']})\n"
            f"Use `/reassign_team` or `/remove_team` first.",
            ephemeral=True
        )
        return
    
    # Check if abbreviation is already taken
    if len(abbreviation) != 2 and len(abbreviation) != 3:
        await interaction.response.send_message(
            "❌ Abbreviation must be 2-3 letters!",
            ephemeral=True
        )
        return
    
    for team in teams.values():
        if team['abbreviation'].upper() == abbreviation.upper():
            await interaction.response.send_message(
                f"❌ Abbreviation **{abbreviation.upper()}** is already taken!",
                ephemeral=True
            )
            return
    
    # Register the team
    if db.pool:
        # Use database
        success = await db.create_team(user_id, team_name, abbreviation.upper())
        if not success:
            await interaction.response.send_message(
                "❌ Failed to assign team. Please try again.",
                ephemeral=True
            )
            return
    else:
        # Use JSON files
        teams[user_id] = {
            "name": team_name,
            "abbreviation": abbreviation.upper(),
            "owner": user.name,
            "owner_id": user_id
        }
        save_json(TEAMS_FILE, teams)
        
        # Initialize standings
        standings[user_id] = {
            "wins": 0,
            "losses": 0,
            "points_for": 0,
            "points_against": 0
        }
        save_json(STANDINGS_FILE, standings)
    
    embed = discord.Embed(
        title="🏈 Team Assigned!",
        description=f"**{team_name}** ({abbreviation.upper()}) has been assigned!",
        color=discord.Color.green()
    )
    embed.add_field(name="Owner", value=user.mention, inline=True)
    embed.add_field(name="Assigned By", value=interaction.user.mention, inline=True)
    embed.set_footer(text=f"Total Teams: {len(teams)}")
    
    await interaction.response.send_message(embed=embed)
    
    # Update the teams roster in #team-owners channel
    await update_teams_list(interaction.guild)

@bot.tree.command(name="teams", description="View all registered teams")
async def teams_command(interaction: discord.Interaction):
    """Display all registered teams"""
    try:
        teams_data = await get_teams_data()
        
        if not teams_data:
            await interaction.response.send_message("❌ No teams registered yet!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="🏈 Registered Teams",
            color=discord.Color.blue()
        )
        
        for user_id, team in teams_data.items():
            member = interaction.guild.get_member(int(user_id))
            owner_mention = member.mention if member else team.get('owner', 'Unknown')
            embed.add_field(
                name=f"{team['abbreviation']} - {team['name']}",
                value=f"Owner: {owner_mention}",
                inline=False
            )
        
        embed.set_footer(text=f"Total Teams: {len(teams_data)}")
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(f"Error in teams command: {e}")
        import traceback
        traceback.print_exc()
        await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)

@bot.tree.command(name="my_team", description="View your team information")
async def my_team(interaction: discord.Interaction):
    """Display user's team information"""
    teams = await get_teams_data()
    standings = await get_standings_data()
    user_id = str(interaction.user.id)
    
    if user_id not in teams:
        await interaction.response.send_message(
            "❌ You don't have a team registered! Use `/register_team` to register.",
            ephemeral=True
        )
        return
    
    team = teams[user_id]
    record = standings.get(user_id, {"wins": 0, "losses": 0, "points_for": 0, "points_against": 0})
    
    embed = discord.Embed(
        title=f"🏈 {team['name']} ({team['abbreviation']})",
        color=discord.Color.gold()
    )
    embed.add_field(name="Owner", value=interaction.user.mention, inline=True)
    embed.add_field(name="Record", value=f"{record['wins']}-{record['losses']}", inline=True)
    embed.add_field(name="Points For", value=str(record['points_for']), inline=True)
    embed.add_field(name="Points Against", value=str(record['points_against']), inline=True)
    
    point_diff = record['points_for'] - record['points_against']
    embed.add_field(name="Point Differential", value=f"{point_diff:+d}", inline=True)
    
    await interaction.response.send_message(embed=embed)

# ==================== STANDINGS ====================

@bot.tree.command(name="standings", description="View league standings")
async def standings(interaction: discord.Interaction):
    """Display league standings"""
    teams = await get_teams_data()
    standings = await get_standings_data()
    
    if not teams:
        await interaction.response.send_message("❌ No teams registered yet!", ephemeral=True)
        return
    
    # Sort teams by wins, then point differential
    sorted_teams = sorted(
        standings.items(),
        key=lambda x: (x[1]['wins'], x[1]['points_for'] - x[1]['points_against']),
        reverse=True
    )
    
    embed = discord.Embed(
        title="🏆 League Standings",
        color=discord.Color.purple()
    )
    
    description = "```\n"
    description += f"{'Rank':<6}{'Team':<20}{'W-L':<8}{'PF':<6}{'PA':<6}{'Diff':<6}\n"
    description += "-" * 52 + "\n"
    
    for rank, (user_id, record) in enumerate(sorted_teams, 1):
        if user_id not in teams:
            continue
        team = teams[user_id]
        team_name = f"{team['abbreviation']}"
        w_l = f"{record['wins']}-{record['losses']}"
        pf = record['points_for']
        pa = record['points_against']
        diff = pf - pa
        
        description += f"{rank:<6}{team_name:<20}{w_l:<8}{pf:<6}{pa:<6}{diff:+<6}\n"
    
    description += "```"
    embed.description = description
    
    config = load_json(CONFIG_FILE)
    embed.set_footer(text=f"Season {config.get('season', 1)} - Week {config.get('week', 1)}")
    
    await interaction.response.send_message(embed=embed)

# ==================== GAME RESULTS ====================

@bot.tree.command(name="report_game", description="Report a game result (Admin only)")
@is_admin()
@app_commands.describe(
    winner="The winning team's owner",
    loser="The losing team's owner",
    winner_score="Winner's score",
    loser_score="Loser's score"
)
async def report_game(
    interaction: discord.Interaction,
    winner: discord.Member,
    loser: discord.Member,
    winner_score: int,
    loser_score: int
):
    """Report a game result"""
    # Defer response to prevent timeout
    await interaction.response.defer()
    
    try:
        teams = await get_teams_data()
        standings = await get_standings_data()
        config = await get_config_data()
        
        winner_id = str(winner.id)
        loser_id = str(loser.id)
        
        if winner_id not in teams or loser_id not in teams:
            await interaction.followup.send("❌ One or both users don't have registered teams!", ephemeral=True)
            return
        
        # Update standings
        if db.pool:
            # Use database
            winner_record = standings[winner_id]
            loser_record = standings[loser_id]
            
            await db.update_standing(
                winner_id,
                winner_record['wins'] + 1,
                winner_record['losses'],
                winner_record['points_for'] + winner_score,
                winner_record['points_against'] + loser_score
            )
            
            await db.update_standing(
                loser_id,
                loser_record['wins'],
                loser_record['losses'] + 1,
                loser_record['points_for'] + loser_score,
                loser_record['points_against'] + winner_score
            )
            
            # Record game
            await db.create_game(
                config.get('week', 1),
                winner_id,
                loser_id,
                teams[winner_id]['name'],
                teams[winner_id]['abbreviation'],
                teams[loser_id]['name'],
                teams[loser_id]['abbreviation'],
                winner_score,
                loser_score
            )
            
            # Update head-to-head
            await db.update_head_to_head(winner_id, loser_id)
        else:
            # Use JSON files
            standings[winner_id]['wins'] += 1
            standings[winner_id]['points_for'] += winner_score
            standings[winner_id]['points_against'] += loser_score
            
            standings[loser_id]['losses'] += 1
            standings[loser_id]['points_for'] += loser_score
            standings[loser_id]['points_against'] += winner_score
            
            save_json(STANDINGS_FILE, standings)
            
            # Add to schedule/results
            schedule = load_json(SCHEDULE_FILE)
            game_result = {
                "week": config.get('week', 1),
                "winner": teams[winner_id]['name'],
                "loser": teams[loser_id]['name'],
                "winner_score": winner_score,
                "loser_score": loser_score,
                "date": datetime.now().isoformat()
            }
            schedule['games'].append(game_result)
            save_json(SCHEDULE_FILE, schedule)
        
        embed = discord.Embed(
            title="🏈 Game Result",
            description=f"**{teams[winner_id]['name']}** defeats **{teams[loser_id]['name']}**",
            color=discord.Color.green()
        )
        embed.add_field(name="Final Score", value=f"{winner_score} - {loser_score}", inline=True)
        embed.add_field(name="Week", value=str(config.get('week', 1)), inline=True)
        
        await interaction.followup.send(embed=embed)
    except Exception as e:
        print(f"Error in report_game: {e}")
        import traceback
        traceback.print_exc()
        await interaction.followup.send(f"❌ Error reporting game: {str(e)}", ephemeral=True)

@bot.tree.command(name="recent_games", description="View recent game results")
@app_commands.describe(count="Number of recent games to show (default: 5)")
async def recent_games(interaction: discord.Interaction, count: Optional[int] = 5):
    """Display recent game results"""
    if db.pool:
        games = await db.get_recent_games(count)
    else:
        schedule = load_json(SCHEDULE_FILE)
        games = schedule.get('games', [])[-count:]
        games.reverse()
    
    if not games:
        await interaction.response.send_message("❌ No games have been played yet!", ephemeral=True)
        return
    
    embed = discord.Embed(
        title="📊 Recent Games",
        color=discord.Color.blue()
    )
    
    for game in games:
        # Handle both database and JSON formats
        winner_name = game.get('winner_team') or game.get('winner')
        loser_name = game.get('loser_team') or game.get('loser')
        result = f"**{winner_name}** {game['winner_score']} - {game['loser_score']} **{loser_name}**"
        embed.add_field(
            name=f"Week {game['week']}",
            value=result,
            inline=False
        )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="report_my_game", description="Report your game result")
@app_commands.describe(
    week="Week number",
    my_score="Your score",
    opponent_abbr="Opponent's team abbreviation (e.g., KC, BUF)",
    opponent_score="Opponent's score"
)
async def report_my_game(interaction: discord.Interaction, week: int, my_score: int, opponent_abbr: str, opponent_score: int):
    """User reports their own game result"""
    # Defer response to prevent timeout
    await interaction.response.defer()
    
    try:
        teams = await get_teams_data()
        standings = await get_standings_data()
        
        user_id = str(interaction.user.id)
        
        # Check if user has a team
        if user_id not in teams:
            await interaction.followup.send(
                "❌ You don't have a registered team! Use `/register_team` first.",
                ephemeral=True
            )
            return
        
        # Find opponent by abbreviation
        opponent_id = None
        opponent_abbr_upper = opponent_abbr.upper()
        for uid, team in teams.items():
            if team['abbreviation'].upper() == opponent_abbr_upper:
                opponent_id = uid
                break
        
        if not opponent_id:
            await interaction.followup.send(
                f"❌ No team found with abbreviation **{opponent_abbr_upper}**!",
                ephemeral=True
            )
            return
        
        if opponent_id == user_id:
            await interaction.followup.send(
                "❌ You can't play against yourself!",
                ephemeral=True
            )
            return
        
        my_team = teams[user_id]
        opp_team = teams[opponent_id]
        
        # Determine winner and loser
        if my_score > opponent_score:
            winner_id = user_id
            loser_id = opponent_id
            winner_score = my_score
            loser_score = opponent_score
            result_text = "🎉 **Victory!**"
            color = discord.Color.green()
        elif my_score < opponent_score:
            winner_id = opponent_id
            loser_id = user_id
            winner_score = opponent_score
            loser_score = my_score
            result_text = "😔 **Defeat**"
            color = discord.Color.red()
        else:
            await interaction.followup.send(
                "❌ Ties are not allowed! Please enter the correct scores.",
                ephemeral=True
            )
            return
        
        # Update standings
        if db.pool:
            # Use database
            winner_record = standings[winner_id]
            loser_record = standings[loser_id]
            
            await db.update_standing(
                winner_id,
                winner_record['wins'] + 1,
                winner_record['losses'],
                winner_record['points_for'] + winner_score,
                winner_record['points_against'] + loser_score
            )
            
            await db.update_standing(
                loser_id,
                loser_record['wins'],
                loser_record['losses'] + 1,
                loser_record['points_for'] + loser_score,
                loser_record['points_against'] + winner_score
            )
            
            # Record game
            await db.create_game(
                week,
                winner_id,
                loser_id,
                teams[winner_id]['name'],
                teams[winner_id]['abbreviation'],
                teams[loser_id]['name'],
                teams[loser_id]['abbreviation'],
                winner_score,
                loser_score
            )
            
            # Update head-to-head
            await db.update_head_to_head(winner_id, loser_id)
        else:
            # Use JSON files
            standings[winner_id]['wins'] += 1
            standings[winner_id]['points_for'] += winner_score
            standings[winner_id]['points_against'] += loser_score
            
            standings[loser_id]['losses'] += 1
            standings[loser_id]['points_for'] += loser_score
            standings[loser_id]['points_against'] += winner_score
            
            save_json(STANDINGS_FILE, standings)
            
            # Record game
            games = load_json(GAMES_FILE)
            game_record = {
                "week": week,
                "winner_id": winner_id,
                "loser_id": loser_id,
                "winner_team": teams[winner_id]['name'],
                "winner_abbr": teams[winner_id]['abbreviation'],
                "loser_team": teams[loser_id]['name'],
                "loser_abbr": teams[loser_id]['abbreviation'],
                "winner_score": winner_score,
                "loser_score": loser_score,
                "date": datetime.utcnow().isoformat()
            }
            games.append(game_record)
            save_json(GAMES_FILE, games)
            
            # Update head-to-head record
            head_to_head = load_json(HEAD_TO_HEAD_FILE)
            h2h_key = f"{winner_id}_{loser_id}"
            if h2h_key not in head_to_head:
                head_to_head[h2h_key] = {"wins": 0}
            head_to_head[h2h_key]["wins"] += 1
            save_json(HEAD_TO_HEAD_FILE, head_to_head)
        
        # Send confirmation
        embed = discord.Embed(
            title=result_text,
            description=f"**{my_team['name']}** {my_score} - {opponent_score} **{opp_team['name']}**",
            color=color
        )
        embed.add_field(name="Week", value=str(week), inline=True)
        embed.add_field(name="Your Record", value=f"{standings[user_id]['wins']}-{standings[user_id]['losses']}", inline=True)
        embed.set_footer(text="Game recorded! Power rankings updated in #power-rankings")
        
        await interaction.followup.send(embed=embed)
        
        # Auto-update power rankings channel
        await update_power_rankings_channel(interaction.guild)
    except Exception as e:
        print(f"Error in report_my_game: {e}")
        import traceback
        traceback.print_exc()
        await interaction.followup.send(f"❌ Error reporting game: {str(e)}", ephemeral=True)

# ==================== POWER RANKINGS ====================

def calculate_power_rankings(teams_data, standings_data, head_to_head_data):
    """Calculate power rankings with tiebreakers"""
    rankings = []
    
    for user_id, team in teams_data.items():
        if user_id not in standings_data:
            continue
        
        record = standings_data[user_id]
        rankings.append({
            'user_id': user_id,
            'team_name': team['name'],
            'abbreviation': team['abbreviation'],
            'wins': record['wins'],
            'losses': record['losses'],
            'points_for': record['points_for'],
            'points_against': record['points_against'],
            'point_diff': record['points_for'] - record['points_against']
        })
    
    # Sort with custom tiebreaker logic
    def compare_teams(team1, team2):
        # First: Compare by wins (more wins = better)
        if team1['wins'] != team2['wins']:
            return team2['wins'] - team1['wins']
        
        # Tied in wins, check head-to-head
        h2h_key1 = f"{team1['user_id']}_{team2['user_id']}"
        h2h_key2 = f"{team2['user_id']}_{team1['user_id']}"
        
        if h2h_key1 in head_to_head_data:
            return -1  # team1 beat team2
        elif h2h_key2 in head_to_head_data:
            return 1   # team2 beat team1
        
        # No head-to-head, use point differential
        return team2['point_diff'] - team1['point_diff']
    
    from functools import cmp_to_key
    rankings.sort(key=cmp_to_key(compare_teams))
    
    return rankings

@bot.tree.command(name="power_rankings", description="View power rankings with tiebreakers")
async def power_rankings(interaction: discord.Interaction):
    """Display power rankings"""
    teams = await get_teams_data()
    standings = await get_standings_data()
    head_to_head = await get_head_to_head_data()
    
    if not teams:
        await interaction.response.send_message("❌ No teams registered yet!", ephemeral=True)
        return
    
    rankings = calculate_power_rankings(teams, standings, head_to_head)
    
    if not rankings:
        await interaction.response.send_message(
            "❌ No teams in standings yet! Teams will appear here once registered.",
            ephemeral=True
        )
        return
    
    embed = discord.Embed(
        title="⚡ Power Rankings",
        color=discord.Color.gold()
    )
    
    rank_text = "```\n"
    rank_text += f"{'#':<4}{'Team':<20}{'Record':<10}{'PF':<6}{'PA':<6}{'Diff':<6}\n"
    rank_text += "-" * 52 + "\n"
    
    for rank, team in enumerate(rankings, 1):
        record = f"{team['wins']}-{team['losses']}"
        rank_text += f"{rank:<4}{team['abbreviation']:<20}{record:<10}{team['points_for']:<6}{team['points_against']:<6}{team['point_diff']:+<6}\n"
    
    rank_text += "```"
    embed.description = rank_text
    
    embed.add_field(
        name="📊 Tiebreaker Rules",
        value="1️⃣ Best Record\n2️⃣ Head-to-Head Result\n3️⃣ Point Differential",
        inline=False
    )
    
    config = load_json(CONFIG_FILE)
    embed.set_footer(text=f"Season {config.get('season', 1)} - Week {config.get('week', 1)} | {len(rankings)} teams")
    
    await interaction.response.send_message(embed=embed)

async def update_power_rankings_channel(guild):
    """Update the power rankings in the #power-rankings channel"""
    channel = discord.utils.get(guild.text_channels, name="power-rankings")
    if not channel:
        return
    
    teams = await get_teams_data()
    standings = await get_standings_data()
    head_to_head = await get_head_to_head_data()
    
    if not teams:
        return
    
    rankings = calculate_power_rankings(teams, standings, head_to_head)
    
    if not rankings:
        return
    
    # Delete old messages in the channel
    try:
        async for message in channel.history(limit=100):
            if message.author == guild.me:
                await message.delete()
    except discord.Forbidden:
        pass
    
    # Create new power rankings embed
    embed = discord.Embed(
        title="⚡ POWER RANKINGS",
        color=discord.Color.gold()
    )
    
    rank_text = "```\n"
    rank_text += f"{'#':<4}{'Team':<20}{'Record':<10}{'PF':<6}{'PA':<6}{'Diff':<6}\n"
    rank_text += "-" * 52 + "\n"
    
    for rank, team in enumerate(rankings, 1):
        record = f"{team['wins']}-{team['losses']}"
        rank_text += f"{rank:<4}{team['abbreviation']:<20}{record:<10}{team['points_for']:<6}{team['points_against']:<6}{team['point_diff']:+<6}\n"
    
    rank_text += "```"
    embed.description = rank_text
    
    embed.add_field(
        name="📊 Tiebreaker Rules",
        value="1️⃣ Best Record\n2️⃣ Head-to-Head Result\n3️⃣ Point Differential",
        inline=False
    )
    
    config = load_json(CONFIG_FILE)
    embed.set_footer(text=f"Season {config.get('season', 1)} - Week {config.get('week', 1)} | {len(rankings)} teams | Auto-updates after each game")
    embed.timestamp = datetime.utcnow()
    
    try:
        await channel.send(embed=embed)
    except discord.Forbidden:
        pass

@bot.tree.command(name="post_power_rankings", description="Post power rankings to #power-rankings channel (Admin only)")
@is_admin()
async def post_power_rankings(interaction: discord.Interaction):
    """Post power rankings to the power-rankings channel"""
    channel = discord.utils.get(interaction.guild.text_channels, name="power-rankings")
    if not channel:
        await interaction.response.send_message(
            "❌ #power-rankings channel not found! Create it first with `/setup_league`",
            ephemeral=True
        )
        return
    
    await interaction.response.defer()
    await update_power_rankings_channel(interaction.guild)
    
    await interaction.followup.send(
        f"✅ Power rankings posted to {channel.mention}!",
        ephemeral=True
    )

# ==================== LEAGUE MANAGEMENT ====================

@bot.tree.command(name="advance_week", description="Advance to the next week (Admin only)")
@is_admin()
async def advance_week(interaction: discord.Interaction):
    """Advance the league to the next week"""
    config = await get_config_data()
    new_week = config.get('week', 1) + 1
    
    if db.pool:
        await db.set_config('week', str(new_week))
    else:
        config['week'] = new_week
        save_json(CONFIG_FILE, config)
    
    embed = discord.Embed(
        title="📅 Week Advanced",
        description=f"The league has advanced to **Week {config['week']}**",
        color=discord.Color.green()
    )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="set_season", description="Set the current season (Admin only)")
@is_admin()
@app_commands.describe(season="Season number")
async def set_season(interaction: discord.Interaction, season: int):
    """Set the current season"""
    if db.pool:
        await db.set_config('season', str(season))
    else:
        config = load_json(CONFIG_FILE)
        config['season'] = season
        save_json(CONFIG_FILE, config)
    
    await interaction.response.send_message(f"✅ Season set to **{season}**", ephemeral=True)

@bot.tree.command(name="announce_sim", description="Announce sim advance to members (Admin only)")
@is_admin()
@app_commands.describe(
    sim_type="Type of sim",
    week="Week number (only for regular season)"
)
@app_commands.choices(sim_type=[
    app_commands.Choice(name="Regular Season Week", value="regular"),
    app_commands.Choice(name="Playoffs", value="playoffs"),
    app_commands.Choice(name="Offseason", value="offseason"),
    app_commands.Choice(name="Draft", value="draft")
])
async def announce_sim(interaction: discord.Interaction, sim_type: str, week: Optional[int] = None):
    """Announce sim advance to the league"""
    announcements_channel = discord.utils.get(interaction.guild.text_channels, name="announcements")
    
    if not announcements_channel:
        await interaction.response.send_message(
            "❌ #announcements channel not found! Create it first with `/setup_league`",
            ephemeral=True
        )
        return
    
    config = load_json(CONFIG_FILE)
    
    # Create announcement based on sim type
    if sim_type == "regular":
        if week is None:
            await interaction.response.send_message(
                "❌ Please specify the week number for regular season sim!",
                ephemeral=True
            )
            return
        
        # Update config
        config['week'] = week
        save_json(CONFIG_FILE, config)
        
        embed = discord.Embed(
            title="🏈 SIM ADVANCE - REGULAR SEASON",
            description=f"@everyone\n\n**The league has simmed to Week {week}!**",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="⏰ What You Need to Do:",
            value=(
                f"1️⃣ Play your Week {week} game\n"
                f"2️⃣ Report your result with `/report_my_game`\n"
                f"3️⃣ Check updated `/power_rankings`"
            ),
            inline=False
        )
        embed.add_field(
            name="📊 Current Status",
            value=f"**Season {config.get('season', 1)}** - **Week {week}**",
            inline=False
        )
        embed.set_footer(text="Good luck this week! 🏆")
        
    elif sim_type == "playoffs":
        embed = discord.Embed(
            title="🏆 SIM ADVANCE - PLAYOFFS",
            description="@everyone\n\n**The league has simmed to the PLAYOFFS!**",
            color=discord.Color.gold()
        )
        embed.add_field(
            name="🎯 Playoff Time!",
            value=(
                "The regular season is over!\n"
                "Check your playoff matchups in Madden.\n"
                "Time to compete for the championship! 🏆"
            ),
            inline=False
        )
        embed.add_field(
            name="⏰ What You Need to Do:",
            value=(
                "1️⃣ Check your playoff bracket\n"
                "2️⃣ Play your playoff game\n"
                "3️⃣ Report results to commissioners"
            ),
            inline=False
        )
        embed.set_footer(text="May the best team win! 🏆")
        
    elif sim_type == "offseason":
        embed = discord.Embed(
            title="🌴 SIM ADVANCE - OFFSEASON",
            description="@everyone\n\n**The league has simmed to the OFFSEASON!**",
            color=discord.Color.purple()
        )
        embed.add_field(
            name="📋 Offseason Activities",
            value=(
                "✅ Free Agency\n"
                "✅ Re-sign your players\n"
                "✅ Prepare for the draft\n"
                "✅ Make roster moves"
            ),
            inline=False
        )
        embed.add_field(
            name="⏰ What You Need to Do:",
            value=(
                "1️⃣ Manage your roster\n"
                "2️⃣ Sign free agents\n"
                "3️⃣ Prepare your draft board\n"
                "4️⃣ Stay active in Discord!"
            ),
            inline=False
        )
        embed.set_footer(text="Build your championship team! 🏗️")
        
    elif sim_type == "draft":
        embed = discord.Embed(
            title="🎓 SIM ADVANCE - DRAFT",
            description="@everyone\n\n**The league has simmed to the DRAFT!**",
            color=discord.Color.green()
        )
        embed.add_field(
            name="🎯 Draft Time!",
            value=(
                "Time to build your future!\n"
                "Make your picks wisely.\n"
                "Scout your prospects! 🔍"
            ),
            inline=False
        )
        embed.add_field(
            name="⏰ What You Need to Do:",
            value=(
                "1️⃣ Review your draft board\n"
                "2️⃣ Make your selections\n"
                "3️⃣ Consider trading picks\n"
                "4️⃣ Build for the future!"
            ),
            inline=False
        )
        embed.set_footer(text="Draft your next superstar! ⭐")
    
    embed.timestamp = datetime.utcnow()
    
    await interaction.response.defer()
    
    # Send announcement
    await announcements_channel.send(embed=embed)
    
    # Confirm to admin
    await interaction.followup.send(
        f"✅ Sim announcement posted to {announcements_channel.mention}!",
        ephemeral=True
    )

@bot.tree.command(name="league_info", description="View league information")
async def league_info(interaction: discord.Interaction):
    """Display league information"""
    config = await get_config_data()
    teams = await get_teams_data()
    schedule = load_json(SCHEDULE_FILE)
    
    embed = discord.Embed(
        title=f"🏈 {config.get('league_name', 'Madden Franchise League')}",
        color=discord.Color.gold()
    )
    embed.add_field(name="Season", value=str(config.get('season', 1)), inline=True)
    embed.add_field(name="Week", value=str(config.get('week', 1)), inline=True)
    embed.add_field(name="Teams", value=str(len(teams)), inline=True)
    embed.add_field(name="Games Played", value=str(len(schedule.get('games', []))), inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="reset_league", description="Reset all league data (Admin only)")
@is_admin()
async def reset_league(interaction: discord.Interaction):
    """Reset all league data"""
    save_json(TEAMS_FILE, {})
    save_json(SCHEDULE_FILE, {"games": []})
    save_json(STANDINGS_FILE, {})
    
    embed = discord.Embed(
        title="⚠️ League Reset",
        description="All league data has been reset!",
        color=discord.Color.red()
    )
    
    await interaction.response.send_message(embed=embed)

# ==================== HELP ====================

@bot.tree.command(name="help", description="View all available commands")
async def help_command(interaction: discord.Interaction):
    """Display help information"""
    embed = discord.Embed(
        title="🏈 Madden Franchise Bot - Commands",
        description="Here are all available commands:",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🔍 Team Selection",
        value=(
            "`/available_teams` - View all available NFL teams\n"
            "`/available_by_division` - View teams by division"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📋 Team Management",
        value=(
            "`/register_team` - Register your team\n"
            "`/teams` - View all teams\n"
            "`/my_team` - View your team info"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🏆 Standings & Results",
        value=(
            "`/standings` - View league standings\n"
            "`/power_rankings` - View power rankings\n"
            "`/report_my_game` - Report your game result\n"
            "`/recent_games` - View recent results"
        ),
        inline=False
    )
    
    embed.add_field(
        name="ℹ️ League Info",
        value="`/league_info` - View league information",
        inline=False
    )
    
    embed.add_field(
        name="👑 Admin Commands",
        value=(
            "`/report_game` - Report a game result\n"
            "`/announce_sim` - Announce sim advance\n"
            "`/advance_week` - Advance to next week\n"
            "`/set_season` - Set current season\n"
            "`/assign_team` - Assign team to any user\n"
            "`/reassign_team` - Transfer team to new owner\n"
            "`/remove_team` - Remove a team from league\n"
            "`/reset_league` - Reset all data"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🏗️ Channel Setup (Admin)",
        value=(
            "`/setup_league` - Create all league channels\n"
            "`/create_team_channel` - Create private team channel\n"
            "`/create_all_team_channels` - Create channels for all teams\n"
            "`/create_matchup` - Create matchup channel for two teams\n"
            "`/archive_matchups` - Delete old week matchup channels\n"
            "`/update_teams_roster` - Update teams roster in #teams\n"
            "`/post_welcome` - Post welcome message\n"
            "`/post_power_rankings` - Post rankings to #power-rankings"
        ),
        inline=False
    )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ping", description="Test if the bot is responding")
async def ping(interaction: discord.Interaction):
    """Simple ping command to test bot responsiveness"""
    await interaction.response.send_message("🏈 Pong! Bot is working!")

# ==================== CHANNEL MANAGEMENT ====================

@bot.tree.command(name="setup_league", description="Create all league channels and categories (Admin only)")
@is_admin()
async def setup_league(interaction: discord.Interaction):
    """Set up complete league channel structure"""
    await interaction.response.defer()  # This might take a while
    
    guild = interaction.guild
    created_channels = []
    
    try:
        # Create main league category
        league_category = await guild.create_category("📊 LEAGUE INFO")
        created_channels.append(f"Category: {league_category.name}")
        
        # Create channels in league category
        commish_channel = await guild.create_text_channel(
            "commish-assistance",
            category=league_category,
            topic="Need help? Ask the commissioners here!"
        )
        created_channels.append(f"#{commish_channel.name}")
        
        polls_channel = await guild.create_text_channel(
            "madden-polls",
            category=league_category,
            topic="League polls and voting"
        )
        created_channels.append(f"#{polls_channel.name}")
        
        announcements_channel = await guild.create_text_channel(
            "announcements",
            category=league_category,
            topic="📢 Official league announcements"
        )
        created_channels.append(f"#{announcements_channel.name}")
        
        recap_channel = await guild.create_text_channel(
            "weekly-recap",
            category=league_category,
            topic="Weekly game recaps and highlights"
        )
        created_channels.append(f"#{recap_channel.name}")
        
        chat_channel = await guild.create_text_channel(
            "general-chat",
            category=league_category,
            topic="💬 General league discussion"
        )
        created_channels.append(f"#{chat_channel.name}")
        
        rankings_channel = await guild.create_text_channel(
            "power-rankings",
            category=league_category,
            topic="Team power rankings and analysis"
        )
        created_channels.append(f"#{rankings_channel.name}")
        
        news_channel = await guild.create_text_channel(
            "breaking-news",
            category=league_category,
            topic="🚨 Breaking league news and updates"
        )
        created_channels.append(f"#{news_channel.name}")
        
        scores_channel = await guild.create_text_channel(
            "league-scores",
            category=league_category,
            topic="📊 Game scores and results"
        )
        created_channels.append(f"#{scores_channel.name}")
        
        # Create upgrade opportunities category
        upgrade_category = await guild.create_category("💰 Upgrade Opportunities")
        created_channels.append(f"Category: {upgrade_category.name}")
        
        gotw_channel = await guild.create_text_channel(
            "gotw-potw",
            category=upgrade_category,
            topic="Game/Player of the Week rewards"
        )
        created_channels.append(f"#{gotw_channel.name}")
        
        awards_channel = await guild.create_text_channel(
            "annual-active-award",
            category=upgrade_category,
            topic="Annual activity awards"
        )
        created_channels.append(f"#{awards_channel.name}")
        
        streaming_channel = await guild.create_text_channel(
            "streaming-channel",
            category=upgrade_category,
            topic="Stream your games here!"
        )
        created_channels.append(f"#{streaming_channel.name}")
        
        # Create join league category
        join_category = await guild.create_category("🚨 Join League 🚨")
        created_channels.append(f"Category: {join_category.name}")
        
        welcome_channel = await guild.create_text_channel(
            "welcome-message",
            category=join_category,
            topic="👋 Welcome to the league!"
        )
        created_channels.append(f"#{welcome_channel.name}")
        
        rules_channel = await guild.create_text_channel(
            "league-rules",
            category=join_category,
            topic="📜 Read the league rules"
        )
        created_channels.append(f"#{rules_channel.name}")
        
        # Create voice channels category
        voice_category = await guild.create_category("🔊 Voice Channels")
        created_channels.append(f"Category: {voice_category.name}")
        
        lobby_voice = await guild.create_voice_channel(
            "Lobby",
            category=voice_category
        )
        created_channels.append(f"🔊 {lobby_voice.name}")
        
        gaming_voice = await guild.create_voice_channel(
            "GOTW Gaming",
            category=voice_category
        )
        created_channels.append(f"🔊 {gaming_voice.name}")
        
        # Create league members category
        members_category = await guild.create_category("👥 League Members")
        created_channels.append(f"Category: {members_category.name}")
        
        owners_channel = await guild.create_text_channel(
            "team-owners",
            category=members_category,
            topic="📋 All registered teams - auto-updated when teams register"
        )
        created_channels.append(f"#{owners_channel.name}")
        
        # Success message
        embed = discord.Embed(
            title="✅ League Channels Created!",
            description="Successfully set up all league channels and categories",
            color=discord.Color.green()
        )
        
        # Add created channels to embed
        channels_text = "\n".join(created_channels[:25])  # Discord embed limit
        if len(created_channels) > 25:
            channels_text += f"\n... and {len(created_channels) - 25} more"
        
        embed.add_field(name="Created Channels", value=channels_text, inline=False)
        embed.set_footer(text=f"Total: {len(created_channels)} items created")
        
        await interaction.followup.send(embed=embed)
        
    except discord.Forbidden:
        await interaction.followup.send(
            "❌ I don't have permission to create channels! Make sure I have 'Manage Channels' permission.",
            ephemeral=True
        )
    except Exception as e:
        await interaction.followup.send(
            f"❌ Error creating channels: {str(e)}",
            ephemeral=True
        )

@bot.tree.command(name="create_team_channel", description="Create a private channel for a team (Admin only)")
@is_admin()
@app_commands.describe(
    team_owner="The team owner to create a channel for",
    channel_name="Custom channel name (optional)"
)
async def create_team_channel(
    interaction: discord.Interaction,
    team_owner: discord.Member,
    channel_name: Optional[str] = None
):
    """Create a private channel for a specific team"""
    teams = await get_teams_data()
    user_id = str(team_owner.id)
    
    if user_id not in teams:
        await interaction.response.send_message(
            f"❌ {team_owner.mention} doesn't have a registered team!",
            ephemeral=True
        )
        return
    
    team = teams[user_id]
    
    # Use custom name or team abbreviation
    if not channel_name:
        channel_name = f"{team['abbreviation'].lower()}-hq"
    
    try:
        # Find or create Team Channels category
        category = discord.utils.get(interaction.guild.categories, name="🏈 Team Channels")
        if not category:
            category = await interaction.guild.create_category("🏈 Team Channels")
        
        # Set permissions - only team owner and admins can see
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            team_owner: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        
        # Create the channel
        channel = await interaction.guild.create_text_channel(
            channel_name,
            category=category,
            topic=f"Private channel for {team['name']} ({team_owner.name})",
            overwrites=overwrites
        )
        
        embed = discord.Embed(
            title="🏈 Team Channel Created!",
            description=f"Created private channel for **{team['name']}**",
            color=discord.Color.green()
        )
        embed.add_field(name="Channel", value=channel.mention, inline=True)
        embed.add_field(name="Owner", value=team_owner.mention, inline=True)
        
        await interaction.response.send_message(embed=embed)
        
        # Send welcome message in the new channel
        welcome_embed = discord.Embed(
            title=f"Welcome to {team['name']} HQ!",
            description=f"This is your private team channel, {team_owner.mention}!",
            color=discord.Color.blue()
        )
        welcome_embed.add_field(
            name="🔒 Privacy",
            value="Only you and admins can see this channel. Other members cannot view it.",
            inline=False
        )
        welcome_embed.add_field(
            name="💡 What's this for?",
            value=(
                "• Use bot commands here (keeps other channels clean!)\n"
                "• Store team notes and strategy\n"
                "• Track your roster moves\n"
                "• Keep important reminders\n"
                "• Anything else team-related!"
            ),
            inline=False
        )
        welcome_embed.add_field(
            name="🤖 Useful Commands",
            value=(
                "`/my_team` - View your team stats\n"
                "`/report_my_game` - Report game results\n"
                "`/power_rankings` - Check rankings\n"
                "`/standings` - View standings"
            ),
            inline=False
        )
        welcome_embed.set_footer(text="Use this channel to stay organized! 🏈")
        await channel.send(embed=welcome_embed)
        
    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ I don't have permission to create channels!",
            ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"❌ Error creating channel: {str(e)}",
            ephemeral=True
        )

@bot.tree.command(name="create_all_team_channels", description="Create private channels for all teams (Admin only)")
@is_admin()
async def create_all_team_channels(interaction: discord.Interaction):
    """Create private channels for all registered teams"""
    await interaction.response.defer()
    
    teams = await get_teams_data()
    
    if not teams:
        await interaction.followup.send("❌ No teams registered yet!", ephemeral=True)
        return
    
    try:
        # Find or create Team Channels category
        category = discord.utils.get(interaction.guild.categories, name="🏈 Team Channels")
        if not category:
            category = await interaction.guild.create_category("🏈 Team Channels")
        
        created_channels = []
        
        for user_id, team in teams.items():
            member = interaction.guild.get_member(int(user_id))
            if not member:
                continue
            
            channel_name = f"{team['abbreviation'].lower()}-hq"
            
            # Check if channel already exists
            existing = discord.utils.get(interaction.guild.text_channels, name=channel_name)
            if existing:
                continue
            
            # Set permissions
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                interaction.guild.me: discord.PermissionOverwrite(read_messages=True)
            }
            
            # Create channel
            channel = await interaction.guild.create_text_channel(
                channel_name,
                category=category,
                topic=f"Private channel for {team['name']} ({member.name})",
                overwrites=overwrites
            )
            
            created_channels.append(f"{channel.mention} - {team['name']}")
            
            # Send welcome message
            welcome_embed = discord.Embed(
                title=f"Welcome to {team['name']} HQ!",
                description=f"This is your private team channel, {member.mention}!",
                color=discord.Color.blue()
            )
            await channel.send(embed=welcome_embed)
        
        if created_channels:
            embed = discord.Embed(
                title="✅ Team Channels Created!",
                description=f"Created {len(created_channels)} team channel(s)",
                color=discord.Color.green()
            )
            embed.add_field(
                name="Channels",
                value="\n".join(created_channels[:10]),
                inline=False
            )
            if len(created_channels) > 10:
                embed.add_field(
                    name="And more...",
                    value=f"+{len(created_channels) - 10} more channels",
                    inline=False
                )
        else:
            embed = discord.Embed(
                title="ℹ️ No Channels Created",
                description="All team channels already exist!",
                color=discord.Color.blue()
            )
        
        await interaction.followup.send(embed=embed)
        
    except discord.Forbidden:
        await interaction.followup.send(
            "❌ I don't have permission to create channels!",
            ephemeral=True
        )
    except Exception as e:
        await interaction.followup.send(
            f"❌ Error: {str(e)}",
            ephemeral=True
        )

@bot.tree.command(name="create_matchup", description="Create a matchup channel for two teams (Admin only)")
@is_admin()
@app_commands.describe(
    team1_abbr="First team's abbreviation (e.g., KC)",
    team2_abbr="Second team's abbreviation (e.g., BUF)",
    week="Week number for this matchup"
)
async def create_matchup(interaction: discord.Interaction, team1_abbr: str, team2_abbr: str, week: int):
    """Create a private matchup channel for two teams to schedule their game"""
    teams = await get_teams_data()
    
    # Find teams by abbreviation
    team1_id = None
    team2_id = None
    team1_abbr_upper = team1_abbr.upper()
    team2_abbr_upper = team2_abbr.upper()
    
    for user_id, team in teams.items():
        if team['abbreviation'].upper() == team1_abbr_upper:
            team1_id = user_id
        if team['abbreviation'].upper() == team2_abbr_upper:
            team2_id = user_id
    
    if not team1_id:
        await interaction.response.send_message(
            f"❌ No team found with abbreviation **{team1_abbr_upper}**!",
            ephemeral=True
        )
        return
    
    if not team2_id:
        await interaction.response.send_message(
            f"❌ No team found with abbreviation **{team2_abbr_upper}**!",
            ephemeral=True
        )
        return
    
    if team1_id == team2_id:
        await interaction.response.send_message(
            "❌ A team can't play against itself!",
            ephemeral=True
        )
        return
    
    team1 = teams[team1_id]
    team2 = teams[team2_id]
    
    # Get Discord members
    member1 = interaction.guild.get_member(int(team1_id))
    member2 = interaction.guild.get_member(int(team2_id))
    
    if not member1 or not member2:
        await interaction.response.send_message(
            "❌ One or both team owners are not in the server!",
            ephemeral=True
        )
        return
    
    await interaction.response.defer()
    
    try:
        # Find or create Matchups category
        category = discord.utils.get(interaction.guild.categories, name="🎮 Week Matchups")
        if not category:
            category = await interaction.guild.create_category("🎮 Week Matchups")
        
        # Create channel name
        channel_name = f"week{week}-{team1['abbreviation'].lower()}-vs-{team2['abbreviation'].lower()}"
        
        # Set permissions - only the two team owners and admins can see
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member1: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            member2: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        
        # Create the channel
        channel = await interaction.guild.create_text_channel(
            channel_name,
            category=category,
            topic=f"Week {week}: {team1['name']} vs {team2['name']}",
            overwrites=overwrites
        )
        
        # Send matchup announcement in the channel
        matchup_embed = discord.Embed(
            title=f"🏈 Week {week} Matchup",
            description=f"{member1.mention} vs {member2.mention}",
            color=discord.Color.orange()
        )
        matchup_embed.add_field(
            name="Matchup",
            value=f"**{team1['name']}** ({team1['abbreviation']})\n🆚\n**{team2['name']}** ({team2['abbreviation']})",
            inline=False
        )
        matchup_embed.add_field(
            name="⏰ What You Need to Do:",
            value=(
                "1️⃣ Coordinate a time to play your game\n"
                "2️⃣ Play your Week {week} matchup\n"
                "3️⃣ Winner reports the result with `/report_my_game`"
            ).format(week=week),
            inline=False
        )
        matchup_embed.add_field(
            name="💬 Use This Channel To:",
            value=(
                "• Schedule your game time\n"
                "• Communicate with your opponent\n"
                "• Discuss any issues\n"
                "• Coordinate reschedules if needed"
            ),
            inline=False
        )
        matchup_embed.set_footer(text="Good luck to both teams! 🏆")
        
        await channel.send(embed=matchup_embed)
        
        # Confirm to admin
        confirm_embed = discord.Embed(
            title="✅ Matchup Channel Created!",
            description=f"Created matchup channel for Week {week}",
            color=discord.Color.green()
        )
        confirm_embed.add_field(name="Channel", value=channel.mention, inline=False)
        confirm_embed.add_field(
            name="Matchup",
            value=f"{team1['abbreviation']} ({member1.mention}) vs {team2['abbreviation']} ({member2.mention})",
            inline=False
        )
        
        await interaction.followup.send(embed=confirm_embed)
        
    except discord.Forbidden:
        await interaction.followup.send(
            "❌ I don't have permission to create channels!",
            ephemeral=True
        )
    except Exception as e:
        await interaction.followup.send(
            f"❌ Error creating matchup channel: {str(e)}",
            ephemeral=True
        )

@bot.tree.command(name="archive_matchups", description="Archive/delete matchup channels for a specific week (Admin only)")
@is_admin()
@app_commands.describe(
    week="Week number to archive (e.g., 1, 2, 3)"
)
async def archive_matchups(interaction: discord.Interaction, week: int):
    """Archive or delete all matchup channels for a specific week"""
    await interaction.response.defer()
    
    try:
        # Find the Week Matchups category
        category = discord.utils.get(interaction.guild.categories, name="🎮 Week Matchups")
        if not category:
            await interaction.followup.send(
                "❌ No matchup channels found! The 🎮 Week Matchups category doesn't exist.",
                ephemeral=True
            )
            return
        
        # Find all channels for this week
        week_prefix = f"week{week}-"
        channels_to_delete = []
        
        for channel in category.text_channels:
            if channel.name.startswith(week_prefix):
                channels_to_delete.append(channel)
        
        if not channels_to_delete:
            await interaction.followup.send(
                f"❌ No matchup channels found for Week {week}!",
                ephemeral=True
            )
            return
        
        # Delete the channels
        deleted_count = 0
        deleted_names = []
        
        for channel in channels_to_delete:
            try:
                deleted_names.append(channel.name)
                await channel.delete()
                deleted_count += 1
            except discord.Forbidden:
                pass
            except Exception:
                pass
        
        # Send confirmation
        embed = discord.Embed(
            title="🗑️ Matchup Channels Archived",
            description=f"Deleted {deleted_count} matchup channel(s) for Week {week}",
            color=discord.Color.green()
        )
        
        if deleted_names:
            channels_list = "\n".join([f"• #{name}" for name in deleted_names[:10]])
            if len(deleted_names) > 10:
                channels_list += f"\n• ... and {len(deleted_names) - 10} more"
            
            embed.add_field(
                name="Deleted Channels",
                value=channels_list,
                inline=False
            )
        
        embed.set_footer(text="Week archived! Server is clean. ✨")
        
        await interaction.followup.send(embed=embed)
        
    except discord.Forbidden:
        await interaction.followup.send(
            "❌ I don't have permission to delete channels!",
            ephemeral=True
        )
    except Exception as e:
        await interaction.followup.send(
            f"❌ Error archiving matchups: {str(e)}",
            ephemeral=True
        )

@bot.tree.command(name="update_teams_roster", description="Update the teams roster in #team-owners channel (Admin only)")
@is_admin()
async def update_teams_roster(interaction: discord.Interaction):
    """Update or create the pinned teams roster in #team-owners channel"""
    teams = await get_teams_data()
    
    # Find #team-owners channel
    teams_channel = discord.utils.get(interaction.guild.text_channels, name="team-owners")
    if not teams_channel:
        await interaction.response.send_message(
            "❌ #team-owners channel not found! Create it first with `/setup_league`",
            ephemeral=True
        )
        return
    
    await interaction.response.defer()
    
    try:
        # Update the roster
        await update_teams_list(interaction.guild)
        
        await interaction.followup.send(
            f"✅ Updated teams roster in {teams_channel.mention}!",
            ephemeral=True
        )
        
    except discord.Forbidden:
        await interaction.followup.send(
            "❌ I don't have permission to post in that channel!",
            ephemeral=True
        )
    except Exception as e:
        await interaction.followup.send(
            f"❌ Error: {str(e)}",
            ephemeral=True
        )

# ==================== WELCOME & AVAILABLE TEAMS ====================

@bot.tree.command(name="post_welcome", description="Post welcome message to welcome-message channel (Admin only)")
@is_admin()
async def post_welcome(interaction: discord.Interaction):
    """Post welcome message to the welcome-message channel"""
    # Find welcome channel
    welcome_channel = discord.utils.get(interaction.guild.text_channels, name="welcome-message")
    if not welcome_channel:
        await interaction.response.send_message(
            "❌ #welcome-message channel not found! Create it first with `/setup_league`",
            ephemeral=True
        )
        return
    
    await interaction.response.defer()
    
    try:
        # Create welcome embed (general version without @mention)
        welcome_embed = discord.Embed(
            title="🏈 Welcome to Yessirski League!",
            description="Welcome to Yessirski League!\n\n⚠️ **YOU HAVE 30 MINUTES** to complete the steps below or the team will be filled with another user!",
            color=discord.Color.red()
        )
        
        welcome_embed.add_field(
            name="🎮 STEP 1: JOIN LEAGUE VIA SEARCH",
            value="**LEAGUE NAME:** `Yessirski`\n**PASSWORD:** `Ballin5`",
            inline=False
        )
        
        welcome_embed.add_field(
            name="📜 STEP 2: Read the Rules",
            value="Head over to <#league-rules> to read our league rules and guidelines.",
            inline=False
        )
        
        welcome_embed.add_field(
            name="🔍 STEP 3: Check Available Teams",
            value="Use `/available_teams` to see which NFL teams are still available. Pick your favorite!",
            inline=False
        )
        
        welcome_embed.add_field(
            name="📝 STEP 4: Register Your Team",
            value="Once you've picked a team, register with:\n`/register_team team_name:Kansas City Chiefs abbreviation:KC`",
            inline=False
        )
        
        welcome_embed.add_field(
            name="💬 STEP 5: Join the Community",
            value="Check out <#general-chat> to meet other league members!",
            inline=False
        )
        
        welcome_embed.add_field(
            name="❓ Need Help?",
            value="Ask questions in <#commish-assistance> and our commissioners will help you out!",
            inline=False
        )
        
        welcome_embed.set_footer(text="⏰ Remember: 30 minutes to complete registration!")
        welcome_embed.timestamp = datetime.utcnow()
        
        await welcome_channel.send(embed=welcome_embed)
        
        await interaction.followup.send(
            f"✅ Posted welcome message to {welcome_channel.mention}!",
            ephemeral=True
        )
        
    except discord.Forbidden:
        await interaction.followup.send(
            "❌ I don't have permission to post in that channel!",
            ephemeral=True
        )
    except Exception as e:
        await interaction.followup.send(
            f"❌ Error: {str(e)}",
            ephemeral=True
        )

@bot.tree.command(name="available_teams", description="View all available NFL teams")
async def available_teams(interaction: discord.Interaction):
    """Display all available NFL teams"""
    teams = await get_teams_data()
    
    # Get list of taken team names and abbreviations
    taken_teams = set()
    taken_abbrs = set()
    for team_data in teams.values():
        taken_teams.add(team_data['name'].lower())
        taken_abbrs.add(team_data['abbreviation'].upper())
    
    # Helper function to check if a team is taken
    def is_team_taken(nfl_team, abbr):
        nfl_lower = nfl_team.lower()
        # Check exact match
        if nfl_lower in taken_teams:
            return True
        # Check if abbreviation is taken
        if abbr in taken_abbrs:
            return True
        # Check if any taken team name is part of the NFL team name
        for taken in taken_teams:
            if taken in nfl_lower or nfl_lower in taken:
                return True
        return False
    
    # Build available teams by division
    embed = discord.Embed(
        title="🏈 Available NFL Teams",
        description="Teams marked with ✅ are available. Teams marked with ❌ are taken.",
        color=discord.Color.green()
    )
    
    afc_divisions = ["AFC East", "AFC North", "AFC South", "AFC West"]
    nfc_divisions = ["NFC East", "NFC North", "NFC South", "NFC West"]
    
    taken_count = 0
    
    # AFC Teams
    afc_text = ""
    for division in afc_divisions:
        afc_text += f"\n**{division}**\n"
        for team in NFL_TEAMS[division]:
            abbr = TEAM_ABBREVIATIONS[team]
            is_taken = is_team_taken(team, abbr)
            if is_taken:
                taken_count += 1
            status = "❌" if is_taken else "✅"
            afc_text += f"{status} {team} ({abbr})\n"
    
    embed.add_field(name="AFC (American Football Conference)", value=afc_text, inline=False)
    
    # NFC Teams
    nfc_text = ""
    for division in nfc_divisions:
        nfc_text += f"\n**{division}**\n"
        for team in NFL_TEAMS[division]:
            abbr = TEAM_ABBREVIATIONS[team]
            is_taken = is_team_taken(team, abbr)
            if is_taken:
                taken_count += 1
            status = "❌" if is_taken else "✅"
            nfc_text += f"{status} {team} ({abbr})\n"
    
    embed.add_field(name="NFC (National Football Conference)", value=nfc_text, inline=False)
    
    # Count available teams
    total_teams = sum(len(teams_list) for teams_list in NFL_TEAMS.values())
    available_count = total_teams - taken_count
    
    embed.set_footer(text=f"{available_count}/{total_teams} teams available")
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="available_by_division", description="View available teams by division")
@app_commands.describe(division="Choose a division")
@app_commands.choices(division=[
    app_commands.Choice(name="AFC East", value="AFC East"),
    app_commands.Choice(name="AFC North", value="AFC North"),
    app_commands.Choice(name="AFC South", value="AFC South"),
    app_commands.Choice(name="AFC West", value="AFC West"),
    app_commands.Choice(name="NFC East", value="NFC East"),
    app_commands.Choice(name="NFC North", value="NFC North"),
    app_commands.Choice(name="NFC South", value="NFC South"),
    app_commands.Choice(name="NFC West", value="NFC West"),
])
async def available_by_division(interaction: discord.Interaction, division: str):
    """Display available teams in a specific division"""
    teams = load_json(TEAMS_FILE)
    
    # Get list of taken team names and abbreviations
    taken_teams = set()
    taken_abbrs = set()
    for team_data in teams.values():
        taken_teams.add(team_data['name'].lower())
        taken_abbrs.add(team_data['abbreviation'].upper())
    
    # Helper function to check if a team is taken
    def is_team_taken(nfl_team, abbr):
        nfl_lower = nfl_team.lower()
        # Check exact match
        if nfl_lower in taken_teams:
            return True
        # Check if abbreviation is taken
        if abbr in taken_abbrs:
            return True
        # Check if any taken team name is part of the NFL team name
        for taken in taken_teams:
            if taken in nfl_lower or nfl_lower in taken:
                return True
        return False
    
    embed = discord.Embed(
        title=f"🏈 {division}",
        description="Available teams in this division:",
        color=discord.Color.blue()
    )
    
    division_teams = NFL_TEAMS[division]
    available_list = []
    taken_list = []
    
    for team in division_teams:
        abbr = TEAM_ABBREVIATIONS[team]
        if is_team_taken(team, abbr):
            taken_list.append(f"❌ {team} ({abbr})")
        else:
            available_list.append(f"✅ {team} ({abbr})")
    
    if available_list:
        embed.add_field(name="Available", value="\n".join(available_list), inline=False)
    
    if taken_list:
        embed.add_field(name="Taken", value="\n".join(taken_list), inline=False)
    
    embed.set_footer(text=f"{len(available_list)}/{len(division_teams)} teams available in this division")
    
    await interaction.response.send_message(embed=embed)

# Run the bot
if __name__ == "__main__":
    # Get token from environment variable
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    if not TOKEN:
        print("ERROR: DISCORD_BOT_TOKEN environment variable not set!")
        print("Please set your Discord bot token as an environment variable.")
        exit(1)
    
    bot.run(TOKEN)
