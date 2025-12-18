#!/usr/bin/env python3
"""
Create a test user account for AccessoryHub
"""

from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

def create_test_user():
    """Create a test user account"""
    print("Creating test user account...")
    



    # Test user credentials
    test_email = "user@test.com"
    test_password = "user123456"
    test_name = "Test User"
    
    try:
        # Create Supabase client
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        print(f"Registering user: {test_email}")
        
        # Register the user
        auth_response = supabase.auth.sign_up({
            "email": test_email,
            "password": test_password,
            "options": {
                "data": {
                    "name": test_name
                }
            }
        })
        
        if auth_response.user:
            print("✅ User registration successful!")
            print(f"User ID: {auth_response.user.id}")
            print(f"Email: {test_email}")
            print(f"Password: {test_password}")
            
            # Try to create user profile (if RLS is properly configured)
            try:
                user_data = {
                    'id': auth_response.user.id,
                    'email': test_email,
                    'name': test_name
                }
                profile_response = supabase.table('users').insert(user_data).execute()
                if profile_response.data:
                    print("✅ User profile created successfully!")
                else:
                    print("⚠️  Profile creation response was empty (may be handled by trigger)")
            except Exception as profile_error:
                print(f"⚠️  Profile creation failed (may be handled by trigger): {profile_error}")
            
            print("\n🔐 LOGIN CREDENTIALS:")
            print(f"Email: {test_email}")
            print(f"Password: {test_password}")
            print("\nYou can now use these credentials to login to your AccessoryHub application!")
            
            return True
        else:
            print("❌ Registration failed - no user data returned")
            return False
            
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        
        # Check if it's a "user already exists" error
        if "already registered" in str(e).lower() or "already been registered" in str(e).lower():
            print(f"\n🔐 LOGIN CREDENTIALS (user already exists):")
            print(f"Email: {test_email}")
            print(f"Password: {test_password}")
            print("This user already exists, you can login with these credentials!")
            return True
        
        return False

if __name__ == "__main__":
    print("=== AccessoryHub Test User Creation ===")
    success = create_test_user()
    
    if success:
        print("\n✅ Test user setup complete!")
    else:
        print("\n❌ Test user creation failed")

