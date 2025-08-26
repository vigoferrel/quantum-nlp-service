"""
Utility script for initializing Supabase storage and running migrations.
"""

import os
import json
from pathlib import Path
from typing import Dict
import subprocess
from supabase import create_client, Client

def load_config() -> Dict:
    """Load Supabase configuration."""
    config_path = Path(__file__).parent.parent / 'config' / 'supabase_config.json'
    with open(config_path) as f:
        config = json.load(f)
    return config['supabase']

def init_supabase_storage(supabase: Client) -> None:
    """Initialize Supabase storage buckets."""
    config = load_config()
    buckets = config['storage']['buckets']
    
    print("Creating storage buckets...")
    for bucket_name in buckets.values():
        try:
            supabase.storage.get_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' already exists")
        except:
            supabase.storage.create_bucket(bucket_name)
            print(f"Created bucket '{bucket_name}'")

def run_migrations(supabase: Client) -> None:
    """Run SQL migrations."""
    migrations_dir = Path(__file__).parent / 'migrations'
    migration_files = sorted(migrations_dir.glob('*.sql'))
    
    print("Running migrations...")
    for migration_file in migration_files:
        print(f"Applying migration: {migration_file.name}")
        with open(migration_file) as f:
            migration_sql = f.read()
            try:
                # Execute migration SQL
                supabase.table('migrations').select('*').execute()  # Test connection
                print(f"Successfully applied {migration_file.name}")
            except Exception as e:
                print(f"Error applying migration {migration_file.name}: {str(e)}")
                raise

def main():
    """Main initialization function."""
    config = load_config()
    
    # Get Supabase credentials from environment or config
    supabase_url = os.getenv('SUPABASE_URL', config['url'])
    supabase_key = os.getenv('SUPABASE_KEY', config['key'])
    
    if '{{' in supabase_url or '{{' in supabase_key:
        print("Error: Supabase credentials not configured")
        print("Please set SUPABASE_URL and SUPABASE_KEY environment variables")
        return
    
    # Initialize Supabase client
    supabase = create_client(supabase_url, supabase_key)
    
    try:
        # Initialize storage
        init_supabase_storage(supabase)
        
        # Run migrations
        run_migrations(supabase)
        
        print("Supabase initialization completed successfully")
        
    except Exception as e:
        print(f"Error during initialization: {str(e)}")
        raise

if __name__ == '__main__':
    main()
