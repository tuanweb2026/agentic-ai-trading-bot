import http.server
import socketserver
import os
import json
import sys

# Thêm thư mục gốc vào PYTHONPATH
sys.path.insert(0, os.path.dirname(__file__))

from core.live_binance import LiveBinanceExchange
from config.settings import settings

PORT = 8000
WEB_DIR = os.path.join(os.path.dirname(__file__), "web")

class MultiThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def end_headers(self):
        # Cấu hình cấm trình duyệt lưu Cache để luôn cập nhật file mới nhất
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_GET(self):
        if self.path.startswith('/api/binance-balance'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            try:
                live_exchange = LiveBinanceExchange()
                balance_data = live_exchange.fetch_real_balance()
                self.wfile.write(json.dumps(balance_data).encode('utf-8'))
            except Exception as e:
                err_res = {
                    "success": False,
                    "reason": str(e),
                    "usdt_free": 378.86,
                    "total_portfolio_usd": 378.86
                }
                self.wfile.write(json.dumps(err_res).encode('utf-8'))
            return
        else:
            super().do_GET()

    def do_POST(self):
        if self.path.startswith('/api/execute-live-order'):
            content_length = int(self.headers.get('Content-Length', 0))
            body_bytes = self.rfile.read(content_length)
            try:
                payload = json.loads(body_bytes.decode('utf-8'))
                action = payload.get('action') # 'BUY' or 'SELL'
                symbol = payload.get('symbol') # e.g. 'BTC/USDT'
                amount_usd = float(payload.get('amount_usd', 43.20))
                quantity = float(payload.get('quantity', 0.0))

                live_exchange = LiveBinanceExchange()
                
                # 🛑 BẢO VỆ CẦU DAO CẤP BACKEND: KIỂM TRA MỐC VỐN TỔNG < $350.00 USD
                if action == 'BUY':
                    balance_info = live_exchange.fetch_real_balance()
                    total_portfolio = balance_info.get('total_portfolio_usd', 0.0)
                    min_stop_threshold = settings.MIN_PORTFOLIO_STOP_LOSS_USD
                    
                    if total_portfolio < min_stop_threshold and total_portfolio > 0:
                        err_msg = f"🛑 CẦU DAO BẢO VỆ THỦ KHO: Tổng ví (${total_portfolio:.2f}) < $350.00 USD. Đã từ chối đặt mua MỚI để bảo toàn vốn!"
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({"status": "ERROR", "reason": err_msg}).encode('utf-8'))
                        return

                    result = live_exchange.create_spot_buy_order(symbol, amount_usd)
                else:
                    result = live_exchange.create_spot_sell_order(symbol, quantity)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ERROR", "reason": str(e)}).encode('utf-8'))
            return
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    os.chdir(WEB_DIR)
    with MultiThreadedTCPServer(("", PORT), Handler) as httpd:
        print(f"\n=======================================================")
        print(f"🚀 MULTI-THREADED AGENTIC AI TRADING WEB SERVER LIVE AT:")
        print(f"👉 http://localhost:{PORT}")
        print(f"⚡ HIGH PERFORMANCE MULTI-THREADING (NEVER FREEZE)")
        print(f"🛑 SAFETY STOP THRESHOLD: MIN $350.00 USD PORTFOLIO STOP LOSS")
        print(f"=======================================================\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down web dashboard server...")

if __name__ == "__main__":
    run_server()
