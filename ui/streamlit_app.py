import streamlit as st
import pandas as pd
import requests
import json

# Set page configuration
st.set_page_config(
    page_title="NL to SQL Converter",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API endpoint URL
API_URL = "http://localhost:5000/api"

def main():
    st.title("Natural Language to SQL Converter")
    st.markdown("Enter your query in natural language")
    
    # Natural language query input
    nl_query = st.text_area("Enter your query:", height=100, 
                           placeholder="Example: Show me all customers from New York.")
    
    # Execute button
    if st.button("Execute Query"):
        if nl_query:
            with st.spinner("Processing your query..."):
                # Call API to process the query
                response = requests.post(
                    f"{API_URL}/query",
                    json={"query": nl_query}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Display the SQL query
                    st.subheader("Generated SQL Query")
                    st.code(result["sql_query"], language="sql")
                    
                    # Display the results
                    st.subheader("Query Results")
                    
                    if result["status"] == "success" and result["data"] and result["data"]["records"]:
                        # Convert to DataFrame and display
                        df = pd.DataFrame(result["data"]["records"])
                        st.dataframe(df, use_container_width=True)
                        
                        # Download option
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="Download results as CSV",
                            data=csv,
                            file_name="query_results.csv",
                            mime="text/csv",
                        )
                    else:
                        st.info(result["message"])
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
        else:
            st.warning("Please enter a query.")

if __name__ == "__main__":
    main()