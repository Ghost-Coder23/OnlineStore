from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY
import sys

# Setup Supabase
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Error initializing Supabase: {e}")
    sys.exit(1)

email = "testadmin@accesoryhub.com"
password = "AdminPassword123!"
name = "Admin User"

print(f"Attempting to login and link profile for {email}...")

try:
    # 1. Sign In (since user is manually created)
    auth_response = supabase.auth.sign_in_with_password({
        "email": email, 
        "password": password
    })
    
    if auth_response.user:
        user_id = auth_response.user.id
        print(f"Login successful! User ID: {user_id}")
        
        # 2. Add to users table
        user_data = {
            'id': user_id,
            'email': email,
            'name': name
        }
        
        try:
            # Check if exists first to avoid duplicate error noise
            existing = supabase.table('users').select('*').eq('id', user_id).execute()
            if existing.data:
                print("User profile already exists in 'users' table.")
            else:
                supabase.table('users').insert(user_data).execute()
                print("Successfully added to 'users' table.")
                
            print("\n===========================================")
            print(f"ADMIN SETUP COMPLETE")
            print(f"You can now login at /login")
            print("===========================================")
            
        except Exception as table_e:
            print(f"Failed to check/insert into users table: {table_e}")
            
    else:
        print("Login failed: No user object returned.")

except Exception as e:
    print(f"Login failed: {e}")
