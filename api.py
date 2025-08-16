from flask import Flask, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS to allow your Flutter app (especially on web) to call the API
CORS(app)

# --- Database Connection Helper ---
def get_db_connection(database):
    """Establishes a connection to the specified database."""
    # This function is well-written and doesn't need changes.
    return mysql.connector.connect(
        host='localhost',
        user='YOUR_USERNAME',
        password='YOUR_PASSWORD',  # <-- Make sure this is your correct password
        database=database
    )

# --- Generic Query Helper ---
def fetch_all_from_table(database, table_name):
    """
    Fetches all records from a specified table.
    Returns a list of dictionaries on success or a dictionary with an error on failure.
    """
    conn = None  # Initialize conn to None
    try:
        conn = get_db_connection(database)
        cursor = conn.cursor(dictionary=True)
        # Note: Using f-strings for table names is safe here because the names are
        # hardcoded in your routes. Never use this pattern with user-provided input
        # to avoid SQL injection vulnerabilities.
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as err:
        print(f"Database Error in '{database}': {err}") # Log the error for debugging
        return {"error": str(err)}
    finally:
        # This improved finally block ensures no errors if the connection itself fails
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# --- Endpoints ---
@app.route('/api/opportunities', methods=['GET'])
def get_opportunities():
    """Fetch all records from 'opportunities' table in 'unstop_data'."""
    result = fetch_all_from_table('unstop_data', 'opportunities')
    
    # --- IMPROVEMENT: Check for error and set status code ---
    if isinstance(result, dict) and 'error' in result:
        # If the helper returned an error, send a 500 status code
        return jsonify(result), 500
    
    # Otherwise, send the data with a 200 OK status code (default)
    return jsonify(result)

@app.route('/api/hackathons', methods=['GET'])
def get_hackathons():
    """Fetch all records from 'hackathons' table in 'devpost_data'."""
    result = fetch_all_from_table('devpost_data', 'hackathons')

    # --- IMPROVEMENT: Check for error and set status code ---
    if isinstance(result, dict) and 'error' in result:
        # If the helper returned an error, send a 500 status code
        return jsonify(result), 500

    # Otherwise, send the data with a 200 OK status code (default)
    return jsonify(result)

# --- Run Flask App ---
if __name__ == '__main__':
    # Use 0.0.0.0 to make the server accessible from other devices on your network
    app.run(host='0.0.0.0', port=5000, debug=True)
