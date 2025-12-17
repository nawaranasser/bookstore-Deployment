import pymysql

db_config = {
    'host': "terraform-20251127172950048000000003.cmzskw2ekzje.us-east-1.rds.amazonaws.com",
    'port': 3306,
    'user': 'admin',
    'password': 'MyBookstoreDB123',
    'database': 'bookstore'
}

try:
    conn = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'], 
        password=db_config['password'],
        database=db_config['database'],
        port=db_config['port']
    )
    print("✅ SUCCESS: Connected with PyMySQL!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")