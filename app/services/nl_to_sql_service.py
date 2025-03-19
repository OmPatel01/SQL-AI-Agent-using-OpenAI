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
            You are an AI assistant that converts natural language queries to PostgreSQL SQL.
            Given the following database schema for a BikeStores database:

            {self.schema_text}

            Please convert the following natural language query to a valid PostgreSQL SQL query:

            "{natural_language_query}"

            Important guidelines:
            1. Table names use underscores, not dots - use 'production_products' NOT 'production.products'
            2. For JOINs, always include equals sign (=) in join conditions, e.g.: ON table1.column = table2.column
            3. Double-check all JOIN syntax before returning
            4. Use appropriate aggregation functions (SUM, AVG, COUNT) when needed
            5. Keep column names exactly as they appear in the schema
            6. Return only the requested information, not all columns unless specified
            7. For dates, use proper PostgreSQL date formatting (YYYY-MM-DD)
            8. Include appropriate GROUP BY and ORDER BY clauses when needed
            9. Always test your query logic for syntax errors before finalizing
            10. For quantity-related questions, ensure JOINs between order_items and products are correct

            Error Handling & Query Optimization:
            11. If the natural language query is ambiguous, interpret it in the most likely business context
            12. Use appropriate indexable columns in WHERE clauses when possible
            13. Avoid using functions on indexed columns in WHERE clauses
            14. Use explicit JOINs instead of implicit joins (comma syntax)
            15. Prefer EXISTS over IN for subqueries when appropriate
            16. For large result sets, always include LIMIT clauses
            17. Use appropriate table aliases for readability and reduced typing

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