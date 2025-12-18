#!/usr/bin/env python3
"""
Script to set up proper Row Level Security (RLS) policies for the AccessoryHub database
"""

from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

def setup_rls_policies():
    print("Setting up Row Level Security policies...")
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # SQL statements to set up RLS policies
        policies = [
            # Enable RLS on all tables
            """
            ALTER TABLE users ENABLE ROW LEVEL SECURITY;
            """,
            """
            ALTER TABLE products ENABLE ROW LEVEL SECURITY;
            """,
            """
            ALTER TABLE cart_items ENABLE ROW LEVEL SECURITY;
            """,
            """
            ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
            """,
            
            # Users table policies
            """
            CREATE POLICY "Users can view their own profile" ON users
                FOR SELECT USING (auth.uid() = id);
            """,
            """
            CREATE POLICY "Users can insert their own profile" ON users
                FOR INSERT WITH CHECK (auth.uid() = id);
            """,
            """
            CREATE POLICY "Users can update their own profile" ON users
                FOR UPDATE USING (auth.uid() = id);
            """,
            
            # Products table policies (public read, admin write)
            """
            CREATE POLICY "Anyone can view products" ON products
                FOR SELECT USING (true);
            """,
            """
            CREATE POLICY "Service role can manage products" ON products
                FOR ALL USING (auth.role() = 'service_role');
            """,
            
            # Cart items policies
            """
            CREATE POLICY "Users can view their own cart items" ON cart_items
                FOR SELECT USING (auth.uid() = user_id);
            """,
            """
            CREATE POLICY "Users can insert their own cart items" ON cart_items
                FOR INSERT WITH CHECK (auth.uid() = user_id);
            """,
            """
            CREATE POLICY "Users can update their own cart items" ON cart_items
                FOR UPDATE USING (auth.uid() = user_id);
            """,
            """
            CREATE POLICY "Users can delete their own cart items" ON cart_items
                FOR DELETE USING (auth.uid() = user_id);
            """,
            
            # Orders policies
            """
            CREATE POLICY "Users can view their own orders" ON orders
                FOR SELECT USING (auth.uid() = user_id);
            """,
            """
            CREATE POLICY "Users can insert their own orders" ON orders
                FOR INSERT WITH CHECK (auth.uid() = user_id);
            """,
            """
            CREATE POLICY "Service role can manage orders" ON orders
                FOR ALL USING (auth.role() = 'service_role');
            """
        ]
        
        print("Executing RLS policy setup...")
        
        # Execute each policy
        for i, policy_sql in enumerate(policies, 1):
            try:
                print(f"Executing policy {i}...")
                response = supabase.rpc('exec_sql', {'sql': policy_sql.strip()}).execute()
                print(f"Policy {i} executed successfully")
            except Exception as e:
                print(f"Policy {i} failed: {e}")
                # Continue with other policies even if one fails
                continue
        
        print("RLS policy setup completed!")
        return True
        
    except Exception as e:
        print(f"Error setting up RLS policies: {e}")
        return False

def create_simple_policies():
    """
    Alternative approach: Create a simple service role function
    """
    print("Creating simple policies alternative...")
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Create a function to bypass RLS for user registration
        create_user_function_sql = """
        CREATE OR REPLACE FUNCTION public.handle_new_user()
        RETURNS TRIGGER AS $$
        BEGIN
          INSERT INTO public.users (id, email, name)
          VALUES (NEW.id, NEW.email, NEW.raw_user_meta_data->>'name');
          RETURN NEW;
        END;
        $$ LANGUAGE plpgsql SECURITY DEFINER;
        """
        
        # Create trigger for automatic user profile creation
        create_trigger_sql = """
        CREATE TRIGGER on_auth_user_created
          AFTER INSERT ON auth.users
          FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();
        """
        
        print("Creating user management function...")
        try:
            supabase.rpc('exec_sql', {'sql': create_user_function_sql.strip()}).execute()
            print("User function created successfully")
        except Exception as e:
            print(f"Function creation error (may already exist): {e}")
        
        print("Creating trigger...")
        try:
            supabase.rpc('exec_sql', {'sql': create_trigger_sql.strip()}).execute()
            print("Trigger created successfully")
        except Exception as e:
            print(f"Trigger creation error: {e}")
        
        return True
        
    except Exception as e:
        print(f"Error with simple policies: {e}")
        return False

if __name__ == "__main__":
    print("=== AccessoryHub RLS Policy Setup ===")
    
    # Try the simple approach first
    print("\n1. Setting up simple user management policies...")
    simple_success = create_simple_policies()
    
    if simple_success:
        print("\nSimple policies setup completed!")
        print("The trigger will automatically create user profiles when users register.")
        print("Try registering a new user now.")
    else:
        print("\nSimple policies failed. Try the manual approach below.")
    
    print("\n=== Manual Steps (if needed) ===")
    print("If the automatic setup doesn't work, you'll need to:")
    print("1. Go to your Supabase Dashboard")
    print("2. Navigate to Authentication > Settings")
    print("3. Go to Database > Tables > users")
    print("4. Disable RLS temporarily or create appropriate policies")
    print("5. Or use the service role key for user management")
