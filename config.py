import os

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://elvwrlwvgolsbtfguppm.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVsdndybHd2Z29sc2J0Zmd1cHBtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU1ODc4NzIsImV4cCI6MjA4MTE2Mzg3Mn0.dHsgJoK5REiiV3d6bLqu3mSVWGRpwJSxEiAKA9lNd0o')

# Flask configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
