#!/usr/bin/env python3
import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

SUPERVISOR_TOKEN = os.environ.get('SUPERVISOR_TOKEN', '')
HA_URL = 'http://supervisor/core'

class ProxyHandler(SimpleHTTPRequestHandler):
    
    def do_GET(self):
        # Log ALL GET requests with full details
        self.log_message(f'[REQUEST] GET {self.path}')
        self.log_message(f'[HEADERS] {dict(self.headers)}')
        self.log_message(f'[CLIENT] {self.client_address}')
    
        # If it's an API call, proxy it
        if self.path.startswith('/api/'):
            self.log_message(f'[PROXY] Matched /api/ pattern - proxying')
        # Otherwise serve static files normally
        else:
            super().do_GET()
    
    def do_POST(self):
        # Log ALL POST requests
        self.log_message(f'[REQUEST] POST {self.path}')
        self.log_message(f'[HEADERS] {dict(self.headers)}')
        self.log_message(f'[CLIENT] {self.client_address}')
    
        if self.path.startswith('/api/'):
            self.log_message(f'[PROXY] Matched /api/ pattern - proxying')
        else:
            self.send_error(405, 'Method Not Allowed')
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def proxy_request(self, method):
        try:
            api_path = self.path
            full_url = f'{HA_URL}{api_path}'
            
            self.log_message(f'[PROXY] {method} {api_path}')
            
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            
            headers = {
                'Authorization': f'Bearer {SUPERVISOR_TOKEN}',
                'Content-Type': 'application/json'
            }
            
            req = Request(full_url, data=body, headers=headers, method=method)
            
            with urlopen(req, timeout=10) as response:
                response_data = response.read()
                
                self.send_response(response.status)
                self.send_header('Content-Type', response.headers.get('Content-Type', 'application/json'))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(response_data)
                
                self.log_message(f'[PROXY] -> {response.status}')
                
        except HTTPError as e:
            self.log_message(f'[PROXY] HTTP Error {e.code}')
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(e.read())
            
        except Exception as e:
            self.log_message(f'[PROXY] Error: {str(e)}')
            self.send_error(500, str(e))

if __name__ == '__main__':
    os.chdir('/var/www/html')
    if not SUPERVISOR_TOKEN:
        print('ERROR: SUPERVISOR_TOKEN not set!')
        exit(1)
    print(f'Starting Shopping Scanner proxy server on port 8099')
    print(f'Serving files from: /var/www/html')
    print(f'Proxying API calls to: {HA_URL}')
    server = HTTPServer(('0.0.0.0', 8099), ProxyHandler)
    server.serve_forever()