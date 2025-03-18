from flask import Flask, request, jsonify
from app.services.nl_to_sql_service import NLToSQLConverter

# Initialize Flask app
app = Flask(__name__)

# Initialize the NLToSQLConverter instance
converter = NLToSQLConverter()

@app.route('/convert_to_sql', methods=['POST'])
def convert_to_sql():
    try:
        # Get the natural language query from the request
        data = request.get_json()
        natural_language_query = data.get("query")

        if not natural_language_query:
            return jsonify({"error": "No query provided"}), 400
        
        # Convert the natural language query to SQL
        sql_query = converter.convert_to_sql(natural_language_query)
        
        if sql_query is None:
            return jsonify({"error": "Failed to convert query to SQL"}), 500
        
        return jsonify({"sql_query": sql_query})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
