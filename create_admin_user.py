#!/usr/bin/env python3
"""
Create admin user for AccessoryHub
"""

from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

def create_admin_user():
    """Create admin user"""
    print("Creating admin user...")
    
    admin_email = "testadmin@accesoryhub.com"
    admin_password = "admin123456"
    admin_name = "Admin User"
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        print(f"Registering admin user: {admin_email}")
        
        auth_response = supabase.auth.sign_up({
            "email": admin_email,
            "password": admin_password,
            "options": {
                "data": {
                    "name": admin_name,
                    "role": "admin"
                }
            }
        })
        
        if auth_response.user:
            print("✅ Admin user registration successful!")
            print(f"User ID: {auth_response.user.id}")
            
            # Try to create admin profile
            try:
                user_data = {
                    'id': auth_response.user.id,
                    'email': admin_email,
                    'name': admin_name,
                    'role': 'admin'
                }
                profile_response = supabase.table('users').insert(user_data).execute()
                if profile_response.data:
                    print("✅ Admin profile created successfully!")
            except Exception as profile_error:
                print(f"⚠️  Admin profile creation failed (may be handled by trigger): {profile_error}")
            
            print("\n🔐 ADMIN LOGIN CREDENTIALS:")
            print(f"Email: {admin_email}")
            print(f"Password: {admin_password}")
            print("\nThis admin account has access to:")
            print("- Admin dashboard at /admin")
            print("- Add/delete products")
            print("- Manage orders")
            print("- Full admin privileges")
            
            return True
        else:
            print("❌ Admin registration failed - no user data returned")
            return False
            
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        
        if "already registered" in str(e).lower():
            print(f"\n🔐 ADMIN LOGIN CREDENTIALS (admin already exists):")
            print(f"Email: {admin_email}")
            print(f"Password: {admin_password}")
            print("Admin account already exists!")
            return True
        
        return False

if __name__ == "__main__":
    print("=== AccessoryHub Admin User Creation ===")
    success = create_admin_user()
    
    if success:
        print("\n✅ Admin user setup complete!")
    else:
        print("\n❌ Admin user creation failed")

