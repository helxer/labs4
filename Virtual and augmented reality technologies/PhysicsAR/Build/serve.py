#!/usr/bin/env python3
"""WebGL static server with correct Content-Encoding and a single Content-Type."""
import http.server
import socketserver
import os
import urllib.parse

GZ_TYPES = {
    '.wasm.gz': 'application/wasm',
    '.js.gz': 'application/javascript',
    '.data.gz': 'application/octet-stream',
}

class WebGLHandler(http.server.SimpleHTTPRequestHandler):
    def guess_type(self, path):
        for ext, ct in GZ_TYPES.items():
            if path.endswith(ext):
                return ct
        return super().guess_type(path)

    def end_headers(self):
        path = urllib.parse.urlsplit(self.path).path
        if path.endswith('.gz'):
            self.send_header('Content-Encoding', 'gzip')
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

os.chdir(os.path.join(os.path.dirname(__file__), 'WebGL'))
PORT = 8000
with socketserver.TCPServer(('', PORT), WebGLHandler) as httpd:
    print(f'Serving http://localhost:{PORT}/ from {os.getcwd()}')
    httpd.serve_forever()