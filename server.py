from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    print(f"Serveur démarré sur le port {port}")
    print(f"Ouvrez votre navigateur et accédez à : http://localhost:{port}/auth.html")
    
    httpd.serve_forever()

if __name__ == '__main__':
    run() 