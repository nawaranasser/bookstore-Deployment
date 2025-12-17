from flask import Flask, jsonify
import pymysql
import os

app = Flask(__name__)

# Database configuration from environment variables
def get_db_config():
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', '3306')),
        'user': os.getenv('DB_USER', 'admin'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'bookstore')
    }

def get_db_connection():
    config = get_db_config()
    return pymysql.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=config['database'],
        port=config['port'],
        cursorclass=pymysql.cursors.DictCursor
    )

def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL
            )
        ''')
        
        cursor.execute("SELECT COUNT(*) FROM books")
        if cursor.fetchone()[0] == 0:
            sample_books = [
                ("The DevOps Handbook", "Gene Kim"),
                ("The Phoenix Project", "Gene Kim"),
                ("The Unicorn Project", "Gene Kim")
            ]
            cursor.executemany("INSERT INTO books (title, author) VALUES (%s, %s)", sample_books)
            conn.commit()
            
        cursor.close()
        conn.close()
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")

@app.route('/books', methods=['GET'])
def get_books():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author FROM books")
        books = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(books)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

# Don't initialize DB at startup - let it happen on first request
# init_db()

if __name__ == '__main__':
    # Initialize DB when the app starts inside EC2
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)