import os
from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langchain_community.utilities import SQLDatabase
from ..database.connection import DatabaseConnection

# Load environment variables
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class QueryService:
    def __init__(self):
        self.db_connection = DatabaseConnection()
        
        # Setup for direct SQL execution
        self.db_uri = os.getenv("DATABASE_URI")  # Make sure this is set in your .env file
    
    def execute_nl_query(self, natural_language_query, nl_to_sql_service=None):
        """
        Execute a natural language query using the provided NL to SQL service.
        
        Args:
            natural_language_query (str): The natural language query to execute
            nl_to_sql_service: An instance of the NLToSQLConverter class (optional)
            
        Returns:
            dict: A dictionary containing the query results and metadata
        """
        try:
            # If no service is provided, return an error
            if nl_to_sql_service is None:
                return {
                    "status": "error",
                    "message": "NL to SQL service not provided",
                    "data": None
                }
            
            # Convert natural language to SQL
            sql_query = nl_to_sql_service.convert_to_sql(natural_language_query)
            
            # Check if the result is an error message
            if sql_query.startswith("ERROR:"):
                return {
                    "status": "error",
                    "message": sql_query,
                    "data": None
                }
            
            # Execute the generated SQL query
            query_result = self.execute_sql_query(sql_query)
            
            # If the SQL execution was successful, add the SQL query to the result
            if query_result["status"] == "success":
                query_result["data"]["sql_query"] = sql_query
            else:
                query_result["data"] = {"sql_query": sql_query}
            
            return query_result
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error executing natural language query: {str(e)}",
                "data": None
            }
    
    def execute_sql_query(self, sql_query):
        """
        Execute a SQL query and return the results.
        
        Args:
            sql_query (str): The SQL query to execute
            
        Returns:
            dict: A dictionary containing the query results and metadata
        """
        try:
            # Execute the query
            result_df = self.db_connection.execute_query(sql_query)
            
            if result_df is None:
                return {
                    "status": "error",
                    "message": "Error executing query",
                    "data": None
                }
            
            if result_df.empty and sql_query.strip().lower().startswith(("select", "show")):
                return {
                    "status": "success",
                    "message": "Query executed successfully, but no results were returned",
                    "data": {
                        "records": [],
                        "columns": [],
                        "row_count": 0
                    }
                }
            
            # Convert the DataFrame to a dictionary
            if not result_df.empty:
                records = result_df.to_dict(orient="records")
                columns = result_df.columns.tolist()
            else:
                records = []
                columns = []
            
            return {
                "status": "success",
                "message": "Query executed successfully",
                "data": {
                    "records": records,
                    "columns": columns,
                    "row_count": len(records)
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error executing query: {str(e)}",
                "data": None
            }