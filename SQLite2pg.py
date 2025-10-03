import sqlite3
import psycopg2
from supabase import create_client

#Variables, change as
database_name = 'your-database.db'  #SQLite3
supabase_url = 'your-supabase-url'
supabase_key = 'your-supabase-key'


# Connect to SQLite
sqlite_conn = sqlite3.connect(database_name)
sqlite_cur = sqlite_conn.cursor()

# Connect to Supabase

supabase = create_client(supabase_url, supabase_key)

# Get all tables
sqlite_cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = sqlite_cur.fetchall()

for table in tables:
    table_name = table[0]
    sqlite_cur.execute(f"SELECT * FROM {table_name}")
    rows = sqlite_cur.fetchall()
    
    # Get column names
    columns = [description[0] for description in sqlite_cur.description]
    
    # Insert into Supabase
    for row in rows:
        data = dict(zip(columns, row))
        supabase.table(table_name).insert(data).execute()