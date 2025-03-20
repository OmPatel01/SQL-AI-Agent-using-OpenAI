from connection import DatabaseConnection

# Initialize database connection
db = DatabaseConnection()

# Test if the connection is working by fetching table names
print("Checking database connection...")

#Verify database connection by retrieving all tables
tables = db.get_all_tables()
if tables:
    print(f"Connected successfully! Tables found: {tables}")
else:
    print("No tables found or connection failed.")

# Optional: Check database schema
schema = db.get_database_schema()
print("Database Schema:", schema)
