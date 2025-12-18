from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY
import sys

# Setup Supabase
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"Error initializing Supabase: {e}")
    sys.exit(1)

bucket_name = "product-images"

print(f"Checking for bucket: {bucket_name}...")

try:
    # List buckets
    buckets = supabase.storage.list_buckets()
    bucket_names = [b.name for b in buckets]
    print(f"Existing buckets: {bucket_names}")

    if bucket_name not in bucket_names:
        print(f"Bucket '{bucket_name}' not found. Attempting to create it...")
        try:
            # Create public bucket
            supabase.storage.create_bucket(bucket_name, options={"public": True})
            print(f"Successfully created bucket: {bucket_name}")
        except Exception as create_e:
            print(f"Failed to create bucket: {create_e}")
            print("You may need to create it manually in the Supabase Dashboard.")
    else:
        print(f"Bucket '{bucket_name}' already exists.")

except Exception as e:
    print(f"Error checking storage: {e}")
