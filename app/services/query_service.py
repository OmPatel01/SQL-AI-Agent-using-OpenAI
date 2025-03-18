from ..database.connection import DatabaseConnection

class QueryService:
    def __init__(self):
        self.db_connection = DatabaseConnection()
    
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
                    "data": None
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