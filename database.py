"""
Database module for Supabase PostgreSQL integration
Handles all database operations for the Madden League Bot
"""

import os
import asyncpg
import json
from typing import Optional, Dict, List

# Database connection pool
pool = None

async def init_db():
    """Initialize database connection pool and create tables"""
    global pool
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("⚠️  DATABASE_URL not found, falling back to JSON files")
        return False
    
    try:
        # Create connection pool
        pool = await asyncpg.create_pool(database_url, min_size=1, max_size=10)
        print("✅ Connected to Supabase database")
        
        # Create tables
        await create_tables()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

async def create_tables():
    """Create all necessary database tables"""
    async with pool.acquire() as conn:
        # Teams table
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                user_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                abbreviation TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        
        # Standings table
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS standings (
                user_id TEXT PRIMARY KEY REFERENCES teams(user_id) ON DELETE CASCADE,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                points_for INTEGER DEFAULT 0,
                points_against INTEGER DEFAULT 0
            )
        ''')
        
        # Games table
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id SERIAL PRIMARY KEY,
                week INTEGER NOT NULL,
                winner_id TEXT REFERENCES teams(user_id),
                loser_id TEXT REFERENCES teams(user_id),
                winner_team TEXT,
                winner_abbr TEXT,
                loser_team TEXT,
                loser_abbr TEXT,
                winner_score INTEGER,
                loser_score INTEGER,
                date TIMESTAMP DEFAULT NOW()
            )
        ''')
        
        # Head to head table
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS head_to_head (
                id SERIAL PRIMARY KEY,
                winner_id TEXT REFERENCES teams(user_id),
                loser_id TEXT REFERENCES teams(user_id),
                wins INTEGER DEFAULT 1,
                UNIQUE(winner_id, loser_id)
            )
        ''')
        
        # Config table
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        ''')
        
        # Initialize default config if not exists
        await conn.execute('''
            INSERT INTO config (key, value) VALUES ('league_name', 'Madden Franchise League')
            ON CONFLICT (key) DO NOTHING
        ''')
        await conn.execute('''
            INSERT INTO config (key, value) VALUES ('season', '1')
            ON CONFLICT (key) DO NOTHING
        ''')
        await conn.execute('''
            INSERT INTO config (key, value) VALUES ('week', '1')
            ON CONFLICT (key) DO NOTHING
        ''')
        await conn.execute('''
            INSERT INTO config (key, value) VALUES ('admin_role', 'League Admin')
            ON CONFLICT (key) DO NOTHING
        ''')
        
        print("✅ Database tables created/verified")

# ==================== TEAMS ====================

async def get_all_teams() -> Dict:
    """Get all teams"""
    if not pool:
        return {}
    
    async with pool.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM teams')
        return {row['user_id']: dict(row) for row in rows}

async def get_team(user_id: str) -> Optional[Dict]:
    """Get a specific team"""
    if not pool:
        return None
    
    async with pool.acquire() as conn:
        row = await conn.fetchrow('SELECT * FROM teams WHERE user_id = $1', user_id)
        return dict(row) if row else None

async def create_team(user_id: str, name: str, abbreviation: str) -> bool:
    """Create a new team"""
    if not pool:
        return False
    
    try:
        async with pool.acquire() as conn:
            await conn.execute(
                'INSERT INTO teams (user_id, name, abbreviation) VALUES ($1, $2, $3)',
                user_id, name, abbreviation
            )
            # Also create standings entry
            await conn.execute(
                'INSERT INTO standings (user_id, wins, losses, points_for, points_against) VALUES ($1, 0, 0, 0, 0)',
                user_id
            )
        return True
    except Exception as e:
        print(f"Error creating team: {e}")
        return False

async def update_team(user_id: str, name: str, abbreviation: str) -> bool:
    """Update a team"""
    if not pool:
        return False
    
    try:
        async with pool.acquire() as conn:
            await conn.execute(
                'UPDATE teams SET name = $1, abbreviation = $2 WHERE user_id = $3',
                name, abbreviation, user_id
            )
        return True
    except Exception as e:
        print(f"Error updating team: {e}")
        return False

async def delete_team(user_id: str) -> bool:
    """Delete a team"""
    if not pool:
        return False
    
    try:
        async with pool.acquire() as conn:
            await conn.execute('DELETE FROM teams WHERE user_id = $1', user_id)
        return True
    except Exception as e:
        print(f"Error deleting team: {e}")
        return False

# ==================== STANDINGS ====================

async def get_all_standings() -> Dict:
    """Get all standings"""
    if not pool:
        return {}
    
    async with pool.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM standings')
        return {row['user_id']: dict(row) for row in rows}

async def get_standing(user_id: str) -> Optional[Dict]:
    """Get a specific team's standing"""
    if not pool:
        return None
    
    async with pool.acquire() as conn:
        row = await conn.fetchrow('SELECT * FROM standings WHERE user_id = $1', user_id)
        return dict(row) if row else None

async def update_standing(user_id: str, wins: int, losses: int, points_for: int, points_against: int) -> bool:
    """Update a team's standing"""
    if not pool:
        return False
    
    try:
        async with pool.acquire() as conn:
            await conn.execute(
                '''UPDATE standings 
                   SET wins = $1, losses = $2, points_for = $3, points_against = $4 
                   WHERE user_id = $5''',
                wins, losses, points_for, points_against, user_id
            )
        return True
    except Exception as e:
        print(f"Error updating standing: {e}")
        return False

# ==================== GAMES ====================

async def get_all_games() -> List[Dict]:
    """Get all games"""
    if not pool:
        return []
    
    async with pool.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM games ORDER BY date DESC')
        return [dict(row) for row in rows]

async def get_recent_games(limit: int = 5) -> List[Dict]:
    """Get recent games"""
    if not pool:
        return []
    
    async with pool.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM games ORDER BY date DESC LIMIT $1', limit)
        return [dict(row) for row in rows]

async def create_game(week: int, winner_id: str, loser_id: str, winner_team: str, winner_abbr: str,
                     loser_team: str, loser_abbr: str, winner_score: int, loser_score: int) -> bool:
    """Create a new game record"""
    if not pool:
        return False
    
    try:
        async with pool.acquire() as conn:
            await conn.execute(
                '''INSERT INTO games (week, winner_id, loser_id, winner_team, winner_abbr, 
                                     loser_team, loser_abbr, winner_score, loser_score)
                   VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)''',
                week, winner_id, loser_id, winner_team, winner_abbr, loser_team, loser_abbr,
                winner_score, loser_score
            )
        return True
    except Exception as e:
        print(f"Error creating game: {e}")
        return False

# ==================== HEAD TO HEAD ====================

async def get_all_head_to_head() -> Dict:
    """Get all head-to-head records"""
    if not pool:
        return {}
    
    async with pool.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM head_to_head')
        result = {}
        for row in rows:
            key = f"{row['winner_id']}_{row['loser_id']}"
            result[key] = {"wins": row['wins']}
        return result

async def update_head_to_head(winner_id: str, loser_id: str) -> bool:
    """Update head-to-head record"""
    if not pool:
        return False
    
    try:
        async with pool.acquire() as conn:
            await conn.execute(
                '''INSERT INTO head_to_head (winner_id, loser_id, wins)
                   VALUES ($1, $2, 1)
                   ON CONFLICT (winner_id, loser_id)
                   DO UPDATE SET wins = head_to_head.wins + 1''',
                winner_id, loser_id
            )
        return True
    except Exception as e:
        print(f"Error updating head-to-head: {e}")
        return False

# ==================== CONFIG ====================

async def get_config() -> Dict:
    """Get all config values"""
    if not pool:
        return {
            'league_name': 'Madden Franchise League',
            'season': 1,
            'week': 1,
            'admin_role': 'League Admin'
        }
    
    async with pool.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM config')
        config = {}
        for row in rows:
            key = row['key']
            value = row['value']
            # Convert numeric strings to integers
            if key in ['season', 'week']:
                config[key] = int(value)
            else:
                config[key] = value
        return config

async def set_config(key: str, value: str) -> bool:
    """Set a config value"""
    if not pool:
        return False
    
    try:
        async with pool.acquire() as conn:
            await conn.execute(
                '''INSERT INTO config (key, value) VALUES ($1, $2)
                   ON CONFLICT (key) DO UPDATE SET value = $2''',
                key, str(value)
            )
        return True
    except Exception as e:
        print(f"Error setting config: {e}")
        return False

async def close_db():
    """Close database connection pool"""
    global pool
    if pool:
        await pool.close()
        print("✅ Database connection closed")
