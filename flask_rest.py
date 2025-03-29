from dotenv import load_dotenv
import urllib.parse as up
import os
from flask import Flask, request
import psycopg2
from flasgger import Swagger

load_dotenv()

app = Flask(__name__)
swagger = Swagger(app)

# Function to establish a connection to the PostgreSQL database.
def connect_db():
    db_url = os.getenv("DATABASE_URL")
    return psycopg2.connect(db_url)

# Function to convert natural language queries to SQL queries.
def convert_to_sql(nl_query):
    mappings = {
        "show all customers" : "SELECT * FROM mock_data;",
        "get total sales" : "SELECT SUM(price*quantity) FROM mock_data;",
        "list top 5 products" : "SELECT * FROM mock_data order by quantity desc limit 5"
    }
    
    # Check if the provided natural language query exists in the mapping.
    if nl_query.lower() not in mappings:
        raise ValueError ("Query cannot be translated")
    return mappings[nl_query.lower()]

# API Endpoint to execute the SQL query and return results.
@app.route("/query", methods= ['POST'])
def fetch():
    
    """
    Fetch Queries
    ---
    description: |
      This endpoint converts a natural language query into an SQL query and executes it.
      **Accepted Inputs:**  
      - Show all customers (Gets you all the details).
      - Get total sales (Fetches you the total sales till date).
      - List top 5 products (Gets you the top 5 products depending upon the quantity).
      
    parameters:
      - name: Name your Demand.
        in: body
        required: true
        schema:
          type: object
          properties:
            query:
              type: string
              description: The query to be transformed.
    responses:
      200:
        description: Successfully retrieved query details.
      400:
        description: Please refer to the error shown.
    """
    #Extracting data from the incomming request.
    data = request.get_json()
    nl_query = data.get("query")
    
    try:
        # Convert natural language to SQL.
        sql_query = convert_to_sql(nl_query)
        
        # Connect to the database and execute the query.
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(sql_query)
        
        # Fetch column names and query results.
        column = [desc[0] for desc in cur.description]
        result = [dict(zip(column,row)) for row in cur.fetchall()]
        
        # Close database connection.
        cur.close()
        conn.close()
        
        #Returning the result.
        return {"result" : result},200
    
    #Handling Errors.
    except Exception as e:
        return {"Error" : str(e)},400

# API Endpoint to return the SQL query without executing it.
@app.route("/explain", methods = ["GET"])
def explain():
    
    """
    Fetch Queries
    ---
    description: |
      This endpoint converts a natural language query into an SQL query and display's that.
      **Accepted Inputs:**  
      - Show all customers. 
      - Get total sales. 
      - List top 5 products.
      
    parameters:
      - name: Name your Demand.
        in: query
        type: string
        required: true
        description: The query to be transformed.
    responses:
      200:
        description: Successfully retrieved query. 
      400:
        description: Please refer to the error shown.
    """
    
    #Extracting data from the incomming request.
    data = request.get_json()
    nl_query = data.get("query")
    
    try:
        # Convert natural language to SQL.
        sql_query = convert_to_sql(nl_query)
        return {"Query": nl_query, "Sql_translation": sql_query} #Returning the sql query in original format.
    
    #Handling Errors.
    except Exception as e:
        return {"Error" : str(e)},400
    
# API Endpoint to validate if a given natural language query can be translated into SQL.
@app.route("/validate", methods = ["POST"])
def validate():
    
    """
    Fetch Queries
    ---
    parameters:
      - name: Name your Demand.
        in: body
        required: true
        schema:
          type: object
          properties:
            query:
              type: string
              description: The query to be transformed.
    responses:
      200:
        description: Successfully validated the query.
      400:
        description: Please refer to the error shown.
    """
    
    #Extracting data from the incomming request.
    data = request.get_json()
    nl_query = data.get("query")
    
    try:
        # Convert natural language to SQL.
        sql_query = convert_to_sql(nl_query)
        return {"Valid" : True},200 #Returning the validity of the SQL query.
    
    #Handling Errors.
    except Exception as e :
        return {"Valid" : False},400 #Returning the validity of the SQL query.
    
if __name__ == "__main__":
    app.run(debug=True)

    
