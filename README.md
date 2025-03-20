# Natural Language to SQL Query Execution AI Agent

This project converts natural language questions into SQL queries and executes them against a database, providing comprehensive results.

## Project Structure

- **app/app.py**: Main Flask application entry point
- **app/api/routes.py**: API endpoints for query processing
- **app/services/nl_to_sql_service.py**: Natural language to SQL conversion using LangChain
- **app/services/query_service.py**: SQL query execution and result formatting
- **app/services/langchain_service.py**: Advanced LangChain capabilities with SQL reasoning
- **app/database/**: Database connection and schema management
- **ui/streamlit_app.py**: Streamlit-based user interface

## Quick Start

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure your database connection in `.env`
4. Run the application: `python main.py`
5. Access the UI at http://localhost:8501

## Documentation & Demo

- [Full Documentation (PDF)](link-to-your-documentation.pdf) - Detailed explanation of architecture, implementation, and usage
- [Demo Video](link-to-your-video) - Watch the application in action

## Sample Queries

Try these example queries:
- "Show me all customers from California"
- "What's the total revenue by product category?"
- "List the top 5 salespeople by order volume"
