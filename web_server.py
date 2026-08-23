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
from core.log_manager import log_manager

PORT = 8000
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")

exchange = LiveBinanceExchange()

# 🚀 ĐỐI SOÁT TỰ ĐỘNG LỊCH SỬ BINANCE & KHÔI PHỤC LOG KHI KHỞI ĐỘNG SERVER
try:
    synced = pnl_tracker.sync_from_binance_orders(exchange)
    log_manager.add_log("SUCCESS", f"🚀 HỆ THỐNG KHỞI ĐỘNG LẠI: Đã khôi phục Live Feed & đối soát {synced} lệnh mới từ Binance API!")
except Exception as e:
    print("Startup sync error:", e)

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
        elif parsed.path == '/api/system-logs':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            logs = log_manager.get_recent_logs(35)
            self.wfile.write(json.dumps({"success": True, "logs": logs}).encode('utf-8'))
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
                pnl_usd = payload.get('pnl_usd', 0.0)
                
                result = {"status": "ERROR", "reason": "Hành động không hợp lệ"}
                
                if action == 'BUY':
                    result = exchange.create_spot_buy_order(symbol, amount_usd)
                    if result.get("status") == "SUCCESS":
                        log_manager.add_log("SUCCESS", f"✅ [MUA SPOT THẬT] Đã MUA SPOT THẬT {symbol} (${amount_usd:.2f} USDT) | Order ID: {result.get('order_id')}")
                elif action == 'SELL':
                    result = exchange.create_spot_sell_order(symbol, quantity, pnl_usd=pnl_usd, amount_usd=amount_usd)
                    if result.get("status") == "SUCCESS":
                        pnl_str = f"+${pnl_usd:.2f}" if pnl_usd >= 0 else f"-${abs(pnl_usd):.2f}"
                        log_manager.add_log("SUCCESS", f"🎯 [BÁN CHỐT SPOT THẬT] Đã bán chốt Spot {symbol} | PnL: {pnl_str} | Order ID: {result.get('order_id')}")

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
