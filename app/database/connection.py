import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Create database connection string
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

class DatabaseConnection:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
    
    # Executes a SQL query against the database and returns results as a pandas DataFrame
    def execute_query(self, query):
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query))
                if result.returns_rows:
                    return pd.DataFrame(result.fetchall(), columns=result.keys())
                return pd.DataFrame()
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
    

    # Retrieves column names, data types, and nullable status for a specified table
    def get_table_schema(self, table_name):
        query = f"""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = '{table_name}'
        """
        return self.execute_query(query)
    
    # Returns a list of all table names in the public schema of the database
    def get_all_tables(self):
        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        """
        result = self.execute_query(query)
        return result["table_name"].tolist() if result is not None else []
    
    # Builds a complete database schema dictionary with details for all tables
    def get_database_schema(self):
        tables = self.get_all_tables()
        schema = {}
        
        for table in tables:
            schema[table] = self.get_table_schema(table).to_dict(orient="records")
            
        return schema
    
