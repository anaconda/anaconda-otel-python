"""
Simple HTTP forward proxy for testing ATEL_PROXY_URL.

Usage:
    python test_proxy.py

Starts a proxy on http://localhost:8888. Then configure:
    export ATEL_PROXY_URL=http://localhost:8888

Every request that flows through the proxy is logged to stdout.
Press Ctrl+C to stop.
"""

import http.server
import socketserver
import urllib.request
import sys


class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        self._proxy()

    def do_GET(self):
        self._proxy()

    def do_PUT(self):
        self._proxy()

    def _proxy(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length else None

        print(f"\n{'='*60}")
        print(f"PROXY REQUEST: {self.command} {self.path}")
        print(f"Headers:")
        for k, v in self.headers.items():
            print(f"  {k}: {v}")
        if body:
            print(f"Body: {len(body)} bytes")
        print(f"{'='*60}")

        # Try to forward the request
        try:
            req = urllib.request.Request(
                self.path,
                data=body,
                headers={k: v for k, v in self.headers.items() if k.lower() not in ("host", "proxy-connection")},
                method=self.command,
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                resp_body = resp.read()
                self.send_response(resp.status)
                for k, v in resp.getheaders():
                    if k.lower() not in ("transfer-encoding",):
                        self.send_header(k, v)
                self.end_headers()
                self.wfile.write(resp_body)
                print(f"PROXY RESPONSE: {resp.status} ({len(resp_body)} bytes)")
        except Exception as e:
            # If the upstream is unreachable, still confirm the proxy received it
            print(f"PROXY FORWARD FAILED (expected if no real collector): {e}")
            self.send_response(502)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            msg = f"Proxy received request but upstream failed: {e}"
            self.wfile.write(msg.encode())

    def log_message(self, format, *args):
        # Suppress default access log (we do our own logging)
        pass


PORT = 8888

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
        httpd.allow_reuse_address = True
        print(f"Test proxy running on http://localhost:{PORT}")
        print(f"Set: export ATEL_PROXY_URL=http://localhost:{PORT}")
        print("Ctrl+C to stop\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nProxy stopped.")
            sys.exit(0)
