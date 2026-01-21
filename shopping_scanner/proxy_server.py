#!/usr/bin/env python3
import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

SUPERVISOR_TOKEN = os.environ.get('SUPERVISOR_TOKEN', '')
HA_URL = 'http://supervisor/core'

# Debug token at startup
print(f'[DEBUG] SUPERVISOR_TOKEN available: {bool(SUPERVISOR_TOKEN)}')
print(f'[DEBUG] Token length: {len(SUPERVISOR_TOKEN) if SUPERVISOR_TOKEN else 0}')
if SUPERVISOR_TOKEN:
    print(f'[DEBUG] Token starts with: {SUPERVISOR_TOKEN[:30]}...')
class ProxyHandler(SimpleHTTPRequestHandler):
    
    def do_GET(self):
        # Log ALL GET requests with full details
        self.log_message(f'[REQUEST] GET {self.path}')
        self.log_message(f'[HEADERS] {dict(self.headers)}')
        self.log_message(f'[CLIENT] {self.client_address}')
        
        # Handle ingress paths like /api/hassio_ingress/.../api/states
        if '/api/' in self.path:
            # Extract the /api/... part (use rfind to get the last occurrence)
            api_index = self.path.rfind('/api/')
            actual_api_path = self.path[api_index:]
            self.log_message(f'[PROXY] Matched /api/ pattern - proxying: {actual_api_path}')
            self.proxy_request('GET', actual_api_path)
        # Otherwise serve static files normally
        else:
            self.log_message(f'[STATIC] Serving static file')
            super().do_GET()
    
    def do_POST(self):
        # Log ALL POST requests
        self.log_message(f'[REQUEST] POST {self.path}')
        self.log_message(f'[HEADERS] {dict(self.headers)}')
        self.log_message(f'[CLIENT] {self.client_address}')
        
        # Handle ingress paths
        if '/api/' in self.path:
            api_index = self.path.rfind('/api/')
            actual_api_path = self.path[api_index:]
            self.log_message(f'[PROXY] Matched /api/ pattern - proxying: {actual_api_path}')
            self.proxy_request('POST', actual_api_path)
        else:
            self.send_error(405, 'Method Not Allowed')
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def proxy_request(self, method, api_path=None):
        try:
            # Use provided api_path or fall back to self.path
            if api_path is None:
                api_path = self.path
                
            full_url = f'{HA_URL}{api_path}'
            
            self.log_message(f'[PROXY] {method} {api_path} -> {full_url}')
            
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            
            headers = {
                'Authorization': f'Bearer {SUPERVISOR_TOKEN}',
                'Content-Type': 'application/json'
            }
            self.log_message(f'[PROXY] Token present: {bool(SUPERVISOR_TOKEN)}')
            self.log_message(f'[PROXY] Token length: {len(SUPERVISOR_TOKEN) if SUPERVISOR_TOKEN else 0}')
            self.log_message(f'[PROXY] Token preview: {SUPERVISOR_TOKEN[:20] if SUPERVISOR_TOKEN else "NONE"}...')
            
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
            error_body = e.read()
            self.log_message(f'[PROXY] Error response: {error_body.decode("utf-8", errors="ignore")}')
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(error_body)
            
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
