"""
Migration script to move data from JSON files to Supabase
Run this once to migrate your existing league data
"""

import asyncio
import json
import os
from dotenv import load_dotenv
import database as db

# Load environment variables
load_dotenv()

def load_json(filepath):
    """Load JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {} if 'config' not in filepath else {'league_name': 'Madden Franchise League', 'season': 1, 'week': 1, 'admin_role': 'League Admin'}
    except json.JSONDecodeError:
        return {}

async def migrate_data():
    """Migrate all data from JSON to Supabase"""
    
    print("🚀 Starting migration to Supabase...")
    print("=" * 50)
    
    # Initialize database
    success = await db.init_db()
    if not success:
        print("❌ Failed to connect to database!")
        print("Make sure DATABASE_URL is set in your .env file")
        return
    
    # Load JSON data
    print("\n📂 Loading JSON files...")
    teams = load_json('data/teams.json')
    standings = load_json('data/standings.json')
    games = load_json('data/games.json')
    head_to_head = load_json('data/head_to_head.json')
    config = load_json('data/config.json')
    
    print(f"   Teams: {len(teams)}")
    print(f"   Standings: {len(standings)}")
    print(f"   Games: {len(games)}")
    print(f"   Head-to-Head: {len(head_to_head)}")
    
    # Migrate config
    print("\n⚙️  Migrating config...")
    for key, value in config.items():
        await db.set_config(key, str(value))
    print("   ✅ Config migrated")
    
    # Migrate teams
    print("\n👥 Migrating teams...")
    team_count = 0
    for user_id, team_data in teams.items():
        success = await db.create_team(
            user_id,
            team_data['name'],
            team_data['abbreviation']
        )
        if success:
            team_count += 1
            print(f"   ✅ {team_data['name']} ({team_data['abbreviation']})")
        else:
            print(f"   ⚠️  Failed to migrate {team_data['name']}")
    
    print(f"\n   Total teams migrated: {team_count}/{len(teams)}")
    
    # Migrate standings
    print("\n📊 Migrating standings...")
    standing_count = 0
    for user_id, standing_data in standings.items():
        if user_id in teams:  # Only migrate if team exists
            success = await db.update_standing(
                user_id,
                standing_data.get('wins', 0),
                standing_data.get('losses', 0),
                standing_data.get('points_for', 0),
                standing_data.get('points_against', 0)
            )
            if success:
                standing_count += 1
                record = f"{standing_data.get('wins', 0)}-{standing_data.get('losses', 0)}"
                print(f"   ✅ {teams[user_id]['abbreviation']}: {record}")
    
    print(f"\n   Total standings migrated: {standing_count}/{len(standings)}")
    
    # Migrate games
    print("\n🏈 Migrating games...")
    game_count = 0
    for game in games:
        success = await db.create_game(
            game.get('week', 1),
            game.get('winner_id', ''),
            game.get('loser_id', ''),
            game.get('winner_team', ''),
            game.get('winner_abbr', ''),
            game.get('loser_team', ''),
            game.get('loser_abbr', ''),
            game.get('winner_score', 0),
            game.get('loser_score', 0)
        )
        if success:
            game_count += 1
            print(f"   ✅ Week {game.get('week')}: {game.get('winner_abbr')} {game.get('winner_score')} - {game.get('loser_score')} {game.get('loser_abbr')}")
    
    print(f"\n   Total games migrated: {game_count}/{len(games)}")
    
    # Migrate head-to-head
    print("\n🆚 Migrating head-to-head records...")
    h2h_count = 0
    for key, data in head_to_head.items():
        parts = key.split('_')
        if len(parts) == 2:
            winner_id, loser_id = parts
            # Update multiple times if wins > 1
            for _ in range(data.get('wins', 1)):
                success = await db.update_head_to_head(winner_id, loser_id)
                if success:
                    h2h_count += 1
    
    print(f"   Total head-to-head records migrated: {h2h_count}")
    
    # Verify migration
    print("\n✅ Verifying migration...")
    db_teams = await db.get_all_teams()
    db_standings = await db.get_all_standings()
    db_games = await db.get_all_games()
    db_config = await db.get_config()
    
    print(f"   Teams in database: {len(db_teams)}")
    print(f"   Standings in database: {len(db_standings)}")
    print(f"   Games in database: {len(db_games)}")
    print(f"   Config in database: {len(db_config)} keys")
    
    # Close database connection
    await db.close_db()
    
    print("\n" + "=" * 50)
    print("🎉 Migration complete!")
    print("\nNext steps:")
    print("1. Verify data in Supabase dashboard")
    print("2. Update bot.py to use database")
    print("3. Deploy to Railway with DATABASE_URL")
    print("=" * 50)

if __name__ == "__main__":
    # Run migration
    asyncio.run(migrate_data())
