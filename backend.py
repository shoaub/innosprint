import http.server
import sqlite3
import json

# Create an SQLite database (or connect to an existing one)
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

# Create a table for products
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        price REAL,
        image_url TEXT
    )
''')
conn.commit()

# HTTP request handler
class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/products':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Fetch products from the database
            cursor.execute('SELECT * FROM products')
            products = cursor.fetchall()

            # Convert the products to JSON and send the response
            response = json.dumps([{
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'price': row[3],
                'image_url': row[4]
            } for row in products])
            self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

if __name__ == '__main__':
    # Start the HTTP server
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, RequestHandler)
    print('Starting server on port 8000...')
    httpd.serve_forever()
