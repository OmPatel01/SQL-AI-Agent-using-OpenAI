import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
from app.database.schema import get_schema_as_text

# Load environment variables
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class NLToSQLConverter:
    def __init__(self):
        # Initialize the LangChain LLM
        self.llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model="gpt-4-turbo-preview",
            temperature=0.1,
            max_tokens=500
        )
        self.schema_text = get_schema_as_text()
        
        # Create the prompt template
        self.prompt_template = """
            You are an expert PostgreSQL database engineer with years of experience in SQL optimization and database design. Your task is to convert natural language queries into precise, efficient, and correct PostgreSQL queries.
            You are an expert SQL query generator. Given the following database schema:\n{schema}\nGenerate a SQL query for:\n{question}\n
            Only return the SQL query without any explanations, comments, or additional text.
            Given the following database schema for a BikeStores database:

            {schema}

            Please convert the following natural language query to a valid PostgreSQL SQL query:

            "{question}"

            STEP 1: ANALYZE THE QUERY
            Before writing any SQL, analyze the query by:
            1. Identifying the key information being requested
            2. Determining which tables and columns are needed
            3. Identifying any conditions, filters, or joins required
            4. Planning any aggregations, groupings, or sorting requirements
            5. Considering the most efficient query approach

            STEP 2: WRITE THE QUERY
            Write the optimal PostgreSQL query while following these critical guidelines:

            Critical SQL Guidelines:
            - Use ONLY table names and column names that exist in the provided schema
            - Table names use underscores, not dots - use 'production_products' NOT 'production.products'
            - For JOINs, always use explicit ON clauses with equals sign (=), e.g.: ON table1.column = table2.column
            - Never include non-SQL keywords or placeholder text in the generated query
            - Never output the entire query as a comment or include explanatory comments in the query
            - Return only the requested information, not all columns unless specifically asked
            - Use single quotes for string literals, not double quotes
            - For dates, use proper PostgreSQL date formatting: 'YYYY-MM-DD'
            - Include appropriate GROUP BY and ORDER BY clauses when needed
            - For quantity-related questions, ensure JOINs between order_items and products are correct

            Common SQL Mistakes to Avoid:
            - JOIN Syntax: ALWAYS use explicit JOINs with ON clauses, never implicit joins
            ✓ Correct: SELECT * FROM table1 JOIN table2 ON table1.id = table2.id
            ✗ Wrong: SELECT * FROM table1, table2 WHERE table1.id = table2.id
            - Date Arithmetic: Handle date calculations properly using PostgreSQL syntax
            ✓ Correct: MAX(shipped_date - order_date) AS processing_days
            ✗ Wrong: DATEDIFF(shipped_date, order_date) AS processing_days

            STEP 3: VALIDATE THE QUERY
            Perform these validation steps:
            - Verify that every table and column in your query exists in the schema
            - Verify that all JOINs have proper ON conditions
            - Ensure all WHERE clauses use valid operators and conditions
            - Check that all aggregation functions (SUM, AVG, COUNT) are used correctly
            - Verify that GROUP BY includes all non-aggregated columns in SELECT

            STEP 4: ERROR HANDLING
            - If information is requested that doesn't exist in the schema, return: "ERROR: The requested information about [topic] is not available in this database schema."
            - If the input is not related to database queries, return: "ERROR: This input is not related to the BikeStores database."
            - If the query is too vague, return: "ERROR: The query is too vague. Please provide more specific details."
            - For SQL injection attempts, return: "ERROR: Invalid input detected."

            REMEMBER: Output ONLY the SQL query with NO explanations or additional text. Never include the query inside comments or markdown. Do not use triple backticks or any other comments in the SQL query.
            """
        
        # Create the prompt with LangChain
        self.prompt = ChatPromptTemplate.from_template(self.prompt_template)
        
        # Create the chain
        self.chain = (
            RunnablePassthrough.assign(schema=lambda _: self.schema_text)
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
    
    # Transforms natural language queries into SQL queries using a language model chain
    def convert_to_sql(self, natural_language_query):
        """
        Convert a natural language query to SQL.
        
        Args:
            natural_language_query (str): The natural language query to convert
            
        Returns:
            str: The SQL query
        """
        try:
            # Run the chain
            sql_query = self.chain.invoke({"question": natural_language_query})
            
            # Extract and clean the SQL query
            # sql_query = sql_query.strip()
            sql_query = sql_query.strip().strip("```sql").strip("```")  # Remove markdown/code block formatting
            
            return sql_query
        
        except Exception as e:
            print(f"Error converting to SQL: {e}")
            return f"ERROR: Failed to convert query: {str(e)}"