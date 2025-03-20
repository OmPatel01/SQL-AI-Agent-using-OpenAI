from flask import Blueprint, request, jsonify
from ..services.nl_to_sql_service import NLToSQLConverter
from ..services.query_service import QueryService
from ..services.langchain_service import LangChainService

# Create Blueprint
api_bp = Blueprint('api', __name__)

# Initialize services
nl_to_sql_converter = NLToSQLConverter()
query_service = QueryService()
langchain_service = LangChainService()  # Add the new service

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

# New endpoints for LangChain service

@api_bp.route('/langchain/direct', methods=['POST'])
def langchain_direct_query():
    data = request.json
    if not data or 'query' not in data:
        return jsonify({"status": "error", "message": "No query provided"}), 400
    
    natural_language_query = data['query']
    
    try:
        # Use direct query method from LangChain service
        result = langchain_service.direct_query(natural_language_query)
        return jsonify({
            "status": "success",
            "result": result
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to process query: {str(e)}"
        }), 500

@api_bp.route('/langchain/agent', methods=['POST'])
def langchain_agent_query():
    data = request.json
    if not data or 'query' not in data:
        return jsonify({"status": "error", "message": "No query provided"}), 400
    
    natural_language_query = data['query']
    
    try:
        # Use agent-based query method from LangChain service
        result = langchain_service.agent_query(natural_language_query)
        return jsonify({
            "status": "success",
            "result": result
        })
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": f"Failed to process query: {str(e)}"
        }), 500