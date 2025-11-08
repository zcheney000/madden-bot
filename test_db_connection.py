import asyncio
import asyncpg
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

async def test_connection():
    database_url = os.getenv('DATABASE_URL')
    print(f"Testing connection...")
    print(f"URL (first 60 chars): {database_url[:60]}...")
    
    # Try with URL encoding for special characters
    if '*' in database_url or '@' in database_url.split('://')[1].split('@')[0]:
        print("\n⚠️  Special characters detected in password")
        print("Trying with URL-encoded password...")
        
        # Parse and rebuild URL with encoded password
        parts = database_url.split('://')
        protocol = parts[0]
        rest = parts[1]
        
        # Split user:pass from host
        auth_and_host = rest.split('@')
        user_pass = auth_and_host[0]
        host = auth_and_host[1]
        
        # Split user and pass
        user, password = user_pass.split(':')
        
        # URL encode the password
        encoded_password = quote_plus(password)
        
        # Rebuild URL
        encoded_url = f"{protocol}://{user}:{encoded_password}@{host}"
        print(f"Encoded URL (first 60 chars): {encoded_url[:60]}...")
        
        try:
            conn = await asyncpg.connect(encoded_url)
            print("\n✅ Connection successful with encoded password!")
            await conn.close()
            print(f"\nUse this in your .env file:")
            print(f"DATABASE_URL={encoded_url}")
            return
        except Exception as e:
            print(f"\n❌ Failed with encoded password: {e}")
    
    # Try original URL
    try:
        conn = await asyncpg.connect(database_url)
        print("\n✅ Connection successful!")
        await conn.close()
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check your password is correct")
        print("2. Check Supabase project is running")
        print("3. Try URL-encoding special characters in password")

if __name__ == "__main__":
    asyncio.run(test_connection())
