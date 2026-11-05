from http.server import BaseHTTPRequestHandler
import json
import subprocess
import urllib.parse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == "/" or parsed_path.path == "":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "Cheetah Cloud API is running smoothly!"}).encode('utf-8'))
            return

        query_params = urllib.parse.parse_qs(parsed_path.query)
        url_list = query_params.get('url', [])
        
        if not url_list:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "URL parameter is missing"}).encode('utf-8'))
            return
            
        target_url = url_list[0]
        
        try:
            cmd = ['yt-dlp', '--get-url', '--no-warnings', target_url]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            
            direct_url = target_url
            if result.returncode == 0:
                links = result.stdout.strip().split('\n')
                for link in links:
                    if link.startswith('http'):
                        direct_url = link
                        break
                        
            response_data = {"success": True, "direct_url": direct_url}
        except Exception as e:
            response_data = {"success": False, "direct_url": target_url, "error": str(e)}
            
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
        return
