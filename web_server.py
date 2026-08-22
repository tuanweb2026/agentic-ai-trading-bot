import http.server
import socketserver
import json
import urllib.parse
import os
import sys

# Thêm thư mục hiện tại vào PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.live_binance import LiveBinanceExchange
from core.pnl_tracker import pnl_tracker

PORT = 8000
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")

exchange = LiveBinanceExchange()

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/api/binance-balance':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            data = exchange.fetch_real_balance()
            self.wfile.write(json.dumps(data).encode('utf-8'))
            return
        elif parsed.path == '/api/pnl-analytics':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            data = pnl_tracker.get_analytics()
            self.wfile.write(json.dumps({"success": True, "data": data}).encode('utf-8'))
            return
            
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/api/execute-live-order':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                payload = json.loads(post_data.decode('utf-8'))
                action = payload.get('action') # 'BUY' hoặc 'SELL'
                symbol = payload.get('symbol')
                amount_usd = payload.get('amount_usd', 80.0)
                quantity = payload.get('quantity', 0.0)
                
                result = {"status": "ERROR", "reason": "Hành động không hợp lệ"}
                
                if action == 'BUY':
                    result = exchange.create_spot_buy_order(symbol, amount_usd)
                elif action == 'SELL':
                    result = exchange.create_spot_sell_order(symbol, quantity)
                    # 🚀 NẾU LỆNH BÁN KHỚP THÀNH CÔNG -> TỰ ĐỘNG GHI NHẬN VÀO PNL ANALYTICS MÁY CHỦ
                    if result.get("status") == "SUCCESS" and result.get("order_id"):
                        pnl_usd = payload.get("pnl_usd", 0.0)
                        pnl_tracker.record_trade(
                            symbol=symbol,
                            side="SELL",
                            amount_usd=amount_usd,
                            pnl_usd=pnl_usd,
                            order_id=str(result["order_id"])
                        )

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ERROR", "reason": str(e)}).encode('utf-8'))
                return
        elif parsed.path == '/api/record-trade':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode('utf-8'))
                res = pnl_tracker.record_trade(
                    symbol=payload.get("symbol"),
                    side=payload.get("side", "SELL"),
                    amount_usd=payload.get("amount_usd", 80.0),
                    pnl_usd=payload.get("pnl_usd", 0.0),
                    order_id=str(payload.get("order_id", ""))
                )
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(res).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ERROR", "reason": str(e)}).encode('utf-8'))
                return

        self.send_response(404)
        self.end_headers()

class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

if __name__ == '__main__':
    with ThreadingHTTPServer(("", PORT), CustomHandler) as httpd:
        print(f"🚀 Multi-threaded Web Server running at http://localhost:{PORT}")
        httpd.serve_forever()
