from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY
import sys

print(f"Connecting to: {SUPABASE_URL}")

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Try a simple read
    print("Attempting to read 'products' table...")
    response = supabase.table('products').select('*').limit(1).execute()
    print("Connection successful!")
    print(f"Data: {response.data}")
    
except Exception as e:
    print(f"Connection failed: {e}")
