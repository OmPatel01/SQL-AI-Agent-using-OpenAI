import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from ..database.connection import DatabaseConnection
from ..database.schema import get_schema_as_text

# Load environment variables
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class LangChainService:
    def __init__(self):
        self.db_connection = DatabaseConnection()
        
        # Setup for LangChain SQL interaction
        self.db_uri = os.getenv("DATABASE_URI")  # Make sure this is set in your .env file
        self.schema_text = get_schema_as_text()

        try:
            if self.db_uri:
                self.db = SQLDatabase.from_uri(
                    self.db_uri,
                    include_tables=None,  # Include all tables
                    sample_rows_in_table_info=3,  # Number of sample rows to include in table info
                )
                
                self.llm = ChatOpenAI(
                    api_key=OPENAI_API_KEY,
                    model="gpt-4-turbo-preview",
                    temperature=0.1
                )
                
                # Create SQL Database Toolkit
                self.toolkit = SQLDatabaseToolkit(
                    db=self.db,
                    llm=self.llm
                )
                
                # Create SQL Agent
                self.agent = create_sql_agent(
                    llm=self.llm,
                    toolkit=self.toolkit,
                    verbose=True,
                    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                    top_k=10  # Show only top-k tables for in case of many tables
                )
                
                self.initialized = True
            else:
                self.initialized = False
                print("DATABASE_URI not found in environment variables.")
                
        except Exception as e:
            self.initialized = False
            print(f"Error initializing LangChain components: {e}")
    
    def query_with_agent(self, natural_language_query):
        """
        Execute a natural language query using the LangChain SQL agent.
        The agent can perform complex reasoning and choose the best tools.
        
        Args:
            natural_language_query (str): The natural language query to execute
            
        Returns:
            dict: A dictionary containing the query results and metadata
        """
        if not self.initialized:
            return {
                "status": "error",
                "message": "LangChain SQL agent not initialized",
                "data": None
            }
        
        try:
            # Execute the query with the agent
            result = self.agent.invoke({
                "input": f"""
                    You are an expert in writing optimized SQL queries for a PostgreSQL database.
                    Use only valid PostgreSQL functions for date and time calculations, such as:
                    
                    - AGE(order_date, ship_date)
                    - EXTRACT(YEAR FROM order_date)
                    - DATE_PART('day', ship_date - order_date)
                    
                    Generate and execute an efficient SQL query to answer the following question:
                    
                    Question: {natural_language_query}
                    
                    Return only the SQL query and the results, without additional explanations.
                    """
            })
            
            # Extract the result and any intermediate SQL queries
            output = result.get("output", "No output")
            
            # Try to extract the SQL query from the agent's thoughts
            sql_query = "SQL query not visible in agent's output"
            for action in result.get("intermediate_steps", []):
                if "query" in str(action).lower() or "select" in str(action).lower():
                    try:
                        sql_parts = str(action).split("```sql")
                        if len(sql_parts) > 1:
                            sql_query = sql_parts[1].split("```")[0].strip()
                    except:
                        pass
            
            return {
                "status": "success",
                "message": "Query executed successfully via LangChain Agent",
                "data": {
                    "result": output,
                    "sql_query": sql_query,
                    "full_trace": str(result.get("intermediate_steps", "No trace available"))
                }
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error executing query with LangChain agent: {str(e)}",
                "data": None
            }
    
    def direct_database_query(self, natural_language_query):
        """
        A simpler method that directly queries the database without the full agent framework.
        This is faster but less powerful than the agent-based approach.
        
        Args:
            natural_language_query (str): The natural language query to execute
            
        Returns:
            dict: A dictionary containing the query results and metadata
        """
        if not self.initialized:
            return {
                "status": "error",
                "message": "LangChain database components not initialized",
                "data": None
            }
        
        try:
            # Get the schema
            schema = get_schema_as_text()
            
            # Create a prompt
            prompt = f"""
                You are an expert in PostgreSQL SQL queries. Follow these guidelines:

                - Use only valid PostgreSQL date/time functions:
                - AGE(order_date, ship_date)
                - EXTRACT(YEAR FROM order_date)
                - DATE_PART('day', ship_date - order_date)
                
                - Ensure correct table references and joins.

                Given the following database schema:

                {schema}

                Generate a PostgreSQL-compatible SQL query to answer the following question:
                {natural_language_query}

                Return only the SQL query with no explanations or additional text.
                """
            
            # Generate SQL
            response = self.llm.invoke(prompt)
            sql_query = response.content.strip()
            
            if sql_query.startswith("```sql"):
                sql_query = sql_query.replace("```sql", "", 1)
            if sql_query.endswith("```"):
                sql_query = sql_query[:-3]
            
            sql_query = sql_query.strip()
            
            # Execute the query
            result = self.db.run(sql_query)
            
            return {
                "status": "success",
                "message": "Query executed successfully",
                "data": {
                    "result": result,
                    "sql_query": sql_query
                }
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error with direct database query: {str(e)}",
                "data": None
            }