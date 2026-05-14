import subprocess
import json
import re
from http.server import HTTPServer, BaseHTTPRequestHandler

def get_token():
    result = subprocess.run([
        'yt-dlp',
        '--print', '%(webpage_url)s',
        '--no-download',
        '--simulate',
        'https://www.youtube.com/watch?v=jNQXAC9IVRw'
    ], capture_output=True, text=True)
    
    # Extraer visitor_data y po_token del output
    visitor = re.search(r'visitor_data=([^&\s]+)', result.stderr)
    potoken = re.search(r'po_token=([^\s]+)', result.stderr)
    
    return {
        "visitor_data": visitor.group(1) if visitor else None,
        "potoken": potoken.group(1) if potoken else None
    }

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/token' or self.path == '/get_pot':
            data = get_token()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        self.do_GET()

HTTPServer(('0.0.0.0', 8080), Handler).serve_forever()
