from flask import Flask, jsonify
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Database connection setup using environment variables
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT', 5432)  # Default to 5432 if not set
    )
    return conn

# Check connection and table existence
try:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = cur.fetchall()
    print("Tables in database:", tables)
    if ('FactTest1',) not in tables:
        print("Table 'FactTest1' does not exist.")
    else:
        print("Table 'FactTest1' exists.")
    cur.close()
    conn.close()
except Exception as e:
    print(f"An error occurred: {e}")

@app.route('/data', methods=['GET'])
def get_data():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # Attempt to query using quotes to handle case sensitivity
        query = 'SELECT * FROM "FactTest1"'
        print(f"Executing query: {query}")
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        data = []
        for row in rows:
            data.append({
                'id_fact': row[0],
                'FK_TypeRecharge': row[1],
                'TypeRecharge': row[2],
                'NombreRecharge': row[3],
                'TotalRechargeTNDHT': row[4],
                'TotalRechargeTNDTTC_Digital': row[5],
                'PourcentageRechargeDigitalVsGlobal': row[6],
                'PourcentageNombreRechargeDigitalVsGlobal': row[7],
                'Date': row[8],
                'NbrOptionGlobal': row[9],
                'MontantOptionGlobal': row[10],
                'NbrOptionDigital': row[11],
                'MontantOptionDigital': row[12],
                'NbrDataGlobal': row[13],
                'MontantDataGlobal': row[14],
                'NbrDataDigital': row[15],
                'MontantDataDigital': row[16]
            })
        
        return jsonify(data)
    except Exception as e:
        print(f"An error occurred while querying the database: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

