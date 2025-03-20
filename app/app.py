# from flask import Flask, request, jsonify
# from app.services.nl_to_sql_service import NLToSQLConverter

# # Initialize Flask app
# app = Flask(__name__)

# # Initialize the NLToSQLConverter instance
# converter = NLToSQLConverter()

# @app.route('/convert_to_sql', methods=['POST'])
# def convert_to_sql():
#     try:
#         # Get the natural language query from the request
#         data = request.get_json()
#         natural_language_query = data.get("query")

#         if not natural_language_query:
#             return jsonify({"error": "No query provided"}), 400
        
#         # Convert the natural language query to SQL
#         sql_query = converter.convert_to_sql(natural_language_query)
        
#         if sql_query is None:
#             return jsonify({"error": "Failed to convert query to SQL"}), 500
        
#         return jsonify({"sql_query": sql_query})
    
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)

import logging
import traceback
from flask import Flask, request, jsonify
from app.services.langchain_service import LangchainService
from app.services.nl_to_sql_service import NLToSQLConverter

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize the LangchainService and NLToSQLConverter instances
langchain_service = LangchainService()
nl_to_sql_converter = NLToSQLConverter()

@app.route('/api/convert_query', methods=['POST'])
def convert_query():
    try:
        # Log the incoming request
        logger.debug("Received request to /api/convert_query")
        
        # Get the query from the request
        data = request.get_json()
        if not data:
            logger.error("No JSON data in request")
            return jsonify({"status": "error", "message": "No data provided"}), 400
            
        query = data.get('query')
        logger.debug(f"Received query: {query}")
        
        # Check if the query is valid
        if not query:
            logger.error("No query provided in request data")
            return jsonify({"status": "error", "message": "No query provided"}), 400
        
        # Process the query using LangchainService
        logger.debug("Processing query with LangchainService")
        result = langchain_service.query_with_agent(query)
        logger.debug(f"Result: {result}")
        
        if result.get("status") == "error":
            logger.error(f"Error in query processing: {result.get('message')}")
            return jsonify(result), 500
            
        return jsonify(result)
    
    except Exception as e:
        # Log the full exception traceback
        error_traceback = traceback.format_exc()
        logger.error(f"Error processing query: {str(e)}\n{error_traceback}")
        
        # Return a more detailed error response
        return jsonify({
            "status": "error",
            "message": "Failed to convert query",
            "error": str(e),
            "traceback": error_traceback
        }), 500

@app.route('/convert_to_sql', methods=['POST'])
def convert_to_sql():
    try:
        # Get the natural language query from the request
        data = request.get_json()
        natural_language_query = data.get("query")

        if not natural_language_query:
            return jsonify({"error": "No query provided"}), 400
        
        # Convert the natural language query to SQL using NLToSQLConverter
        sql_query = nl_to_sql_converter.convert_to_sql(natural_language_query)
        
        if sql_query is None:
            return jsonify({"error": "Failed to convert query to SQL"}), 500
        
        return jsonify({"sql_query": sql_query})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/get_tables', methods=['GET'])
def get_tables():
    try:
        logger.debug("Received request to /api/get_tables")
        
        tables = langchain_service.get_tables()
        logger.debug(f"Retrieved tables: {tables}")
        
        return jsonify({"status": "success", "tables": tables})
    except Exception as e:
        error_traceback = traceback.format_exc()
        logger.error(f"Error retrieving tables: {str(e)}\n{error_traceback}")
        
        return jsonify({
            "status": "error",
            "message": "Failed to retrieve tables",
            "error": str(e),
            "traceback": error_traceback
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
