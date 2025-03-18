from flask import Blueprint, request, jsonify
from ..services.nl_to_sql_service import NLToSQLConverter
from ..services.query_service import QueryService

# Create Blueprint
api_bp = Blueprint('api', __name__)

# Initialize services
nl_to_sql_converter = NLToSQLConverter()
query_service = QueryService()

@api_bp.route('/convert', methods=['POST'])
def convert_nl_to_sql():
    data = request.json
    if not data or 'query' not in data:
        return jsonify({"status": "error", "message": "No query provided"}), 400
    
    natural_language_query = data['query']
    
    # Convert to SQL
    sql_query = nl_to_sql_converter.convert_to_sql(natural_language_query)
    
    if sql_query is None:
        return jsonify({"status": "error", "message": "Failed to convert query"}), 500
    
    return jsonify({
        "status": "success",
        "sql_query": sql_query
    })

@api_bp.route('/execute', methods=['POST'])
def execute_sql():
    data = request.json
    if not data or 'sql_query' not in data:
        return jsonify({"status": "error", "message": "No SQL query provided"}), 400
    
    sql_query = data['sql_query']
    
    # Execute SQL query
    result = query_service.execute_sql_query(sql_query)
    
    return jsonify(result)

@api_bp.route('/query', methods=['POST'])
def process_natural_language_query():
    data = request.json
    if not data or 'query' not in data:
        return jsonify({"status": "error", "message": "No query provided"}), 400
    
    natural_language_query = data['query']
    
    # Convert to SQL
    sql_query = nl_to_sql_converter.convert_to_sql(natural_language_query)
    
    if sql_query is None:
        return jsonify({"status": "error", "message": "Failed to convert query"}), 500
    
    # Execute SQL query
    result = query_service.execute_sql_query(sql_query)
    
    # Add the SQL query to the result
    result["sql_query"] = sql_query
    
    return jsonify(result)