import os

# Define the project structure
project_structure = {
    "nl_to_sql": {
        "app": {
            "__init__.py": "",
            "config.py": "",
            "database": {
                "__init__.py": "",
                "connection.py": "",
                "schema.py": ""
            },
            "models": {
                "__init__.py": "",
                "query_result.py": ""
            },
            "services": {
                "__init__.py": "",
                "nl_to_sql_service.py": "",
                "query_service.py": ""
            },
            "utils": {
                "__init__.py": "",
                "formatters.py": "",
                "validators.py": ""
            },
            "api": {
                "__init__.py": "",
                "routes.py": ""
            }
        },
        "ui": {
            "__init__.py": "",
            "streamlit_app.py": ""
        },
        "tests": {
            "__init__.py": "",
            "test_nl_to_sql.py": "",
            "test_query_execution.py": ""
        },
        "data": {
            "sample_queries.json": ""
        },
        ".env": "",
        ".gitignore": "",
        "requirements.txt": "",
        "README.md": "",
        "main.py": ""
    }
}

# Function to create the directory structure and files
def create_structure(base_path, structure):
    for name, value in structure.items():
        path = os.path.join(base_path, name)
        
        if isinstance(value, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, value)  # Recursively create subdirectories
        else:
            with open(path, 'w') as file:
                file.write(value)

# Set the base directory where you want to create the structure
base_dir = 'nl_to_sql'  # Adjust if your base directory has a different name
os.makedirs(base_dir, exist_ok=True)

# Create the folder structure and files
create_structure(base_dir, project_structure)

print("Project structure created successfully.")
