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

- [Full Documentation (PDF)](https://drive.google.com/file/d/1xqZEHIbxeYaFYUYOv99ceoL9l5simQ2z/view?usp=sharing) - Detailed explanation of architecture, implementation, and usage
- [Demo Video](https://drive.google.com/file/d/1WpKdoN8-zgrAzuewUglQNR3TMBhUNeWr/view?usp=sharing) - Watch the application in action

## Sample Queries

Try these example queries:
1. What are the top 5 most selling product?
2. Provide an overview of the current inventory status, including the count of products in stock for each store.
3. Calculate the processing time for orders and identify the staff members with slower processing time. 
4. How many orders were placed at each store?
5. Compare the sales performance of each store in terms of total revenue and average order value.
6. How has the total sales revenue changed over the previous quarters?
7. Identify the top 10 customers who have made the most purchases.
8. For each product category, identify the top-selling product based on total sales.

## Database Setup  

The database schema and sample data are available in the `database_resources` folder.  
Follow these steps to set up your PostgreSQL database:
1. Create a database named `bikestores`.  
2. Execute `sqlcreatetables.sql` to set up the schema.  
3. Import data in the following order:  
   - `production_categories.sql`  
   - `production_brands.sql`  
   - `sales_customers.sql`  
   - `sales_stores.sql`  
   - `production_products.sql`  
   - `sales_staffs.sql`  
   - `sales_orders.sql`  
   - `sales_order_items.sql`  
   - `production_stocks.sql`  
