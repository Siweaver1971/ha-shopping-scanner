#!/usr/bin/env python3
import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

SUPERVISOR_TOKEN = os.environ.get('SUPERVISOR_TOKEN', '')
HA_URL = 'http://supervisor/core'

class ProxyHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def do_GET(self):
        if self.path.startswith('/api/'):
            self.proxy_request('GET')
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path.startswith('/api/'):
            self.proxy_request('POST')
        else:
            self.send_error(405)
    
    def proxy_request(self, method):
        try:
            # Construct the full HA URL
            api_path = self.path  # e.g., /api/states/todo.shopping_list
            full_url = f'{HA_URL}{api_path}'
            
            print(f'[PROXY] {method} {api_path} -> {full_url}')
            
            # Read request body for POST
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            
            # Make request to HA with Supervisor token
            headers = {
                'Authorization': f'Bearer {SUPERVISOR_TOKEN}',
                'Content-Type': 'application/json'
            }
            
            req = Request(full_url, data=body, headers=headers, method=method)
            
            with urlopen(req, timeout=10) as response:
                response_data = response.read()
                
                self.send_response(response.status)
                self.send_header('Content-Type', response.headers.get('Content-Type', 'application/json'))
                self.end_headers()
                self.wfile.write(response_data)
                
                print(f'[PROXY] Response: {response.status}')
                
        except HTTPError as e:
            print(f'[PROXY] HTTP Error: {e.code} {e.reason}')
            error_body = e.read()
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(error_body)
            
        except URLError as e:
            print(f'[PROXY] URL Error: {e.reason}')
            self.send_error(502, f'Bad Gateway: {str(e.reason)}')
            
        except Exception as e:
            print(f'[PROXY] Error: {str(e)}')
            self.send_error(500, str(e))
    
    def log_message(self, format, *args):
        # Suppress default logging (we print our own)
        return

if __name__ == '__main__':
    os.chdir('/var/www/html')
    print(f'Starting proxy server on port 8099...')
    print(f'Supervisor token: {"present" if SUPERVISOR_TOKEN else "missing"}')
    server = HTTPServer(('0.0.0.0', 8099), ProxyHandler)
    server.serve_forever()