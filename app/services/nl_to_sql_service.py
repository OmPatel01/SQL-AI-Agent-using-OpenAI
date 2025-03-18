import os
from openai import OpenAI
from dotenv import load_dotenv
from app.database.schema import get_schema_as_text

# Load environment variables
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class NLToSQLConverter:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.schema_text = get_schema_as_text()
    
    def convert_to_sql(self, natural_language_query):
        """
        Convert a natural language query to SQL.
        
        Args:
            natural_language_query (str): The natural language query to convert
            
        Returns:
            str: The SQL query
        """
        try:
            # Create a prompt for the OpenAI model
            prompt = f"""
            You are an AI assistant that converts natural language queries to SQL.
            Given the following database schema for a BikeStores database:
            
            {self.schema_text}
            
            Please convert the following natural language query to a valid PostgreSQL SQL query:
            
            "{natural_language_query}"
            
            Important guidelines:
            1. Use schema qualifiers (e.g., production.products, sales.customers) in your query
            2. For JOINs, explicitly specify the join conditions
            3. Use appropriate aggregation functions (SUM, AVG, COUNT) when needed
            4. Keep column names exactly as they appear in the schema
            5. Return only the requested information, not all columns unless specified
            6. For dates, use proper PostgreSQL date formatting
            7. Include appropriate GROUP BY and ORDER BY clauses when needed
            
            Return ONLY the SQL query without any explanations or markdown formatting.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a SQL expert that converts natural language to SQL queries."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # Lower temperature for more consistent output
                max_tokens=500
            )
            
            # Extract the SQL query from the response
            sql_query = response.choices[0].message.content.strip()
            
            return sql_query
        
        except Exception as e:
            print(f"Error converting to SQL: {e}")
            return None

print("ok")