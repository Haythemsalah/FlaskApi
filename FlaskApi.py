from flask import Flask, jsonify
import psycopg2

# Initialize the Flask application
app = Flask(__name__)

# Database connection setup
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="MyDash",
        user="postgres",
        password="haythem"
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
    app.run(debug=True)
