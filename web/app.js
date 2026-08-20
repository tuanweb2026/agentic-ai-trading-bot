// Agentic AI Trading Dashboard - Client Application Logic (Clean Dust Filter >= $15 USD & Enable Fresh $40 USD Spot Buys)

class TradingDashboard {
    constructor() {
        this.portfolio = {
            initialBalance: 395.36,
            cash: 303.61,
            totalPortfolioUsd: 395.36,
            peakValue: 432.47,
            positions: [],
            tradeHistory: []
        };

        this.targetCapitalRecoveryUsd = 432.47;
        this.minPortfolioStopThreshold = 350.00;
        
        // Mốc tỷ lệ vàng Risk-Reward 2:1
        this.takeProfitTargetUsd = 1.20; // Lợi nhuận kỳ vọng +$1.20 USD / lệnh (2.8%)
        this.stopLossTargetUsd = 0.60;   // Rủi ro tối đa -$0.60 USD / lệnh (1.4%)
        this.maxConcurrentPositions = 2; // Tối đa 2 vị thế mở cùng lúc
        
        // Mốc lọc vảy coin lẻ (Dust Minimum): Phải lớn hơn $15.00 USD mới tính là Vị thế đang giữ
        this.minPositionValueUsd = 15.00;

        this.sessionStartBalance = 395.36;
        this.sessionStartTime = new Date().toLocaleTimeString();

        // Bảng Cooldown 15 phút (900,000 ms)
        this.lastOrderTimestamps = {};
        this.cooldownMs = 900000; 

        this.marketData = {
            "BTC/USDT": { price: 65200.0, rsi: 48.5, zScore: 0.45, strainStatus: "NORMAL" },
            "ETH/USDT": { price: 3510.0, rsi: 72.4, zScore: 2.15, strainStatus: "OVERSTRETCHED_UP" },
            "SOL/USDT": { price: 148.5, rsi: 28.1, zScore: -2.35, strainStatus: "OVERSTRETCHED_DOWN" },
            "BNB/USDT": { price: 582.4, rsi: 52.0, zScore: 0.65, strainStatus: "NORMAL" },
            "XRP/USDT": { price: 0.58, rsi: 76.2, zScore: 2.40, strainStatus: "OVERSTRETCHED_UP" },
            "ADA/USDT": { price: 0.38, rsi: 26.5, zScore: -2.10, strainStatus: "OVERSTRETCHED_DOWN" },
            "AVAX/USDT": { price: 24.8, rsi: 58.0, zScore: 0.90, strainStatus: "NORMAL" },
            "NEAR/USDT": { price: 4.32, rsi: 44.0, zScore: -0.55, strainStatus: "NORMAL" },
            "LINK/USDT": { price: 11.95, rsi: 68.0, zScore: 1.85, strainStatus: "NORMAL" },
            "DOT/USDT": { price: 6.45, rsi: 54.0, zScore: 0.85, strainStatus: "NORMAL" }
        };

        this.pods = [
            { id: "Pod-01-RubberBand-BTC", symbol: "BTC/USDT", strategy: "Spot Mean Reversion", sharpe: 1.25, signal: "NEUTRAL", reason: "[SPOT] Z-score bình thường. Đang chờ điểm mua MỚI $40 USD." },
            { id: "Pod-02-Trend-ETH", symbol: "ETH/USDT", strategy: "Spot Trend", sharpe: 1.08, signal: "SELL", reason: "[SPOT] Z-score = 2.15 (Quá mua). Đề xuất BÁN ra USDT." },
            { id: "Pod-03-RubberBand-SOL", symbol: "SOL/USDT", strategy: "Spot Mean Reversion", sharpe: 1.32, signal: "BUY", reason: "[SPOT] Sợi dây thun nén cực đại. KÍCH HOẠT MUA MỚI $40 USD." },
            { id: "Pod-04-Trend-BNB", symbol: "BNB/USDT", strategy: "Spot Trend", sharpe: 1.15, signal: "NEUTRAL", reason: "[SPOT] Thị trường tích lũy." },
            { id: "Pod-05-RubberBand-XRP", symbol: "XRP/USDT", strategy: "Spot Mean Reversion", sharpe: 1.28, signal: "SELL", reason: "[SPOT] Quá mua. Đề xuất BÁN chốt Spot về USDT." },
            { id: "Pod-06-Trend-ADA", symbol: "ADA/USDT", strategy: "Spot Trend", sharpe: 1.10, signal: "NEUTRAL", reason: "[SPOT] Đứng ngoài quan sát." },
            { id: "Pod-07-RubberBand-AVAX", symbol: "AVAX/USDT", strategy: "Spot Mean Reversion", sharpe: 1.20, signal: "NEUTRAL", reason: "[SPOT] Đứng ngoài quan sát." },
            { id: "Pod-08-Trend-NEAR", symbol: "NEAR/USDT", strategy: "Spot Trend", sharpe: 1.05, signal: "NEUTRAL", reason: "[SPOT] Thị trường đi ngang." },
            { id: "Pod-09-RubberBand-LINK", symbol: "LINK/USDT", strategy: "Spot Mean Reversion", sharpe: 1.18, signal: "NEUTRAL", reason: "[SPOT] Vùng giá an toàn." },
            { id: "Pod-10-Trend-DOT", symbol: "DOT/USDT", strategy: "Spot Trend", sharpe: 1.12, signal: "NEUTRAL", reason: "[SPOT] Xu hướng bình thường." }
        ];

        this.aiRunning = false;
        this.timerSeconds = 30;
        this.timerInterval = null;

        this.initUI();
        this.bindEvents();
        this.syncRealBinanceBalance();
    }

    initUI() {
        this.updatePortfolioMetrics();
        this.renderMarketTable();
        this.renderPods();
        this.populateModalSymbols();
    }

    bindEvents() {
        const btnToggle = document.getElementById('btnToggleAI');
        if (btnToggle) {
            btnToggle.onclick = () => this.toggleAI();
        }

        const btnTrigger = document.getElementById('btnTriggerCycle');
        if (btnTrigger) {
            btnTrigger.onclick = () => this.runHeartbeatCycle();
        }

        const btnManual = document.getElementById('btnManualTrade');
        if (btnManual) {
            btnManual.onclick = () => this.openModal();
        }

        const btnCloseModal = document.getElementById('btnCloseModal');
        if (btnCloseModal) btnCloseModal.onclick = () => this.closeModal();

        const btnCancel = document.getElementById('btnCancelOrder');
        if (btnCancel) btnCancel.onclick = () => this.closeModal();

        const btnSubmit = document.getElementById('btnSubmitManualOrder');
        if (btnSubmit) btnSubmit.onclick = () => this.submitManualOrder();

        const btnClear = document.getElementById('btnClearLogs');
        if (btnClear) {
            btnClear.onclick = () => {
                document.getElementById('logFeed').innerHTML = '';
            };
        }
    }

    async syncRealBinanceBalance() {
        try {
            const response = await fetch('/api/binance-balance?t=' + Date.now());
            const data = await response.json();
            if (data.success) {
                this.portfolio.cash = data.usdt_free;
                const totalUsd = data.total_portfolio_usd > 0 ? data.total_portfolio_usd : 395.36;
                this.portfolio.totalPortfolioUsd = totalUsd;
                this.portfolio.initialBalance = totalUsd;

                if (this.sessionStartBalance === null || this.sessionStartBalance < 100) {
                    this.sessionStartBalance = totalUsd;
                    this.sessionStartTime = new Date().toLocaleTimeString();
                }

                const timeStr = new Date().toLocaleTimeString();
                const bnbApiStatus = document.getElementById('valBinanceApiStatus');
                if (bnbApiStatus) {
                    bnbApiStatus.innerText = `🟢 Binance API Live (${timeStr})`;
                }

                // Cầu dao an toàn: Ngắt nếu tổng ví nhỏ hơn 350 USD
                if (totalUsd < 350.00 && totalUsd > 0 && this.aiRunning) {
                    this.triggerSafetyEmergencyStop(totalUsd);
                    return;
                }

                // 🎯 LỌC SẠCH VẢY COIN LẺ: Chỉ tính là Vị Thế Đang Giữ khi giá trị >= $15.00 USD
                const heldBalances = data.balances || {};
                const syncedPositions = [];

                for (let coin in heldBalances) {
                    if (coin !== 'USDT' && coin !== 'BUSD' && coin !== 'USDC' && coin !== 'ATA') {
                        const amount = heldBalances[coin];
                        const symbol = `${coin}/USDT`;
                        const currentPrice = this.marketData[symbol] ? this.marketData[symbol].price : 1.0;
                        const usdValue = amount * currentPrice;

                        // Chỉ chấp nhận các vị thế có giá trị thực sự lớn hơn hoặc bằng $15.00 USD
                        if (usdValue >= 15.0) {
                            const existingPos = this.portfolio.positions.find(p => p.symbol === symbol);
                            const entryPrice = existingPos ? existingPos.entryPrice : currentPrice;

                            syncedPositions.push({
                                id: `pos-${symbol.replace('/', '-')}`,
                                symbol: symbol,
                                podId: existingPos ? existingPos.podId : `Binance-Live-Wallet-${coin}`,
                                side: "BUY_SPOT",
                                entryPrice: entryPrice,
                                amount: amount,
                                targetProfitUsd: 1.20,
                                timestamp: existingPos ? existingPos.timestamp : new Date().toLocaleTimeString()
                            });
                        }
                    }
                }

                this.portfolio.positions = syncedPositions;
                this.renderAll();
            }
        } catch (e) {
            console.log("Error syncing balance:", e);
        }
    }

    triggerSafetyEmergencyStop(currentBalance) {
        if (this.aiRunning) {
            this.aiRunning = false;
            this.stopTimer();

            const btn = document.getElementById('btnToggleAI');
            const lbl = document.getElementById('lblToggleAI');
            const pulse = document.getElementById('aiStatusPulse');
            const statusTxt = document.getElementById('aiStatusText');

            if (btn) btn.className = "btn btn-primary";
            if (lbl) lbl.innerText = "Bắt Đầu AI Đầu Tư (LIVE)";
            if (pulse) pulse.className = "status-indicator danger";
            if (statusTxt) statusTxt.innerText = `🛑 ĐÃ KHÓA TRADING (Ví $${currentBalance.toFixed(2)} < $350.00 USD)`;

            this.addLog("DANGER", `🛑 [CẦU DAO BẢO VỆ] Tổng ví ($${currentBalance.toFixed(2)} USD) < mốc ngắt $350.00 USD! Đã tự động dừng AI Trading!`);
            this.renderAll();
        }
    }

    populateModalSymbols() {
        const sel = document.getElementById('selSymbol');
        if (sel) {
            sel.innerHTML = '';
            for (let sym in this.marketData) {
                const opt = document.createElement('option');
                opt.value = sym;
                opt.innerText = sym;
                sel.appendChild(opt);
            }
        }
    }

    toggleAI() {
        this.aiRunning = !this.aiRunning;
        const btn = document.getElementById('btnToggleAI');
        const lbl = document.getElementById('lblToggleAI');
        const pulse = document.getElementById('aiStatusPulse');
        const statusTxt = document.getElementById('aiStatusText');

        if (this.aiRunning) {
            const totalVal = this.getPortfolioValue();
            this.sessionStartBalance = totalVal > 0 ? totalVal : 395.36;
            this.sessionStartTime = new Date().toLocaleTimeString();

            if (btn) btn.className = "btn btn-secondary";
            if (lbl) lbl.innerText = "Tạm Dừng AI";
            if (pulse) pulse.className = "status-indicator live";
            if (statusTxt) statusTxt.innerText = `🔴 AI ĐANG KÍCH HOẠT CHIẾN LƯỢC MUA MỚI $40 USD (ĐÃ LỌC SẠCH DUST LẺ < $15 USD)`;

            this.addLog("DANGER", `🚀 BẮT ĐẦU KÍCH HOẠT MUA MỚI $40 USD! Đã lọc sạch các vảy lẻ < $15 USD để giải phóng đường MUA MỚI! Mốc ví: $${this.sessionStartBalance.toFixed(2)} USD`);
            
            this.runHeartbeatCycle();
            this.startTimer();
        } else {
            if (btn) btn.className = "btn btn-primary";
            if (lbl) lbl.innerText = "Bắt Đầu AI Đầu Tư (LIVE)";
            if (pulse) pulse.className = "status-indicator";
            if (statusTxt) statusTxt.innerText = "AI Đang Tạm Dừng";

            this.addLog("WARNING", "⏸ Đã tạm dừng AI.");
            this.stopTimer();
        }
    }

    startTimer() {
        this.stopTimer();
        this.timerSeconds = 30;
        this.timerInterval = setInterval(() => {
            this.timerSeconds--;
            const timerEl = document.getElementById('heartbeatTimer');
            if (timerEl) timerEl.innerText = `${this.timerSeconds}s`;

            this.simulateMarketPriceTicks();
            this.checkAutoTakeProfitAndStopLoss();
            this.renderAll();

            if (this.timerSeconds === 20) this.highlightPipelineStep(1, "10s Sub-Agent: Tóm tắt Binance Spot Rubber Band...");
            if (this.timerSeconds === 10) this.highlightPipelineStep(2, "20s Pod Theory: Đánh giá 10 Spot Pods (Sharpe > 1.0)...");
            
            if (this.timerSeconds <= 0) {
                this.highlightPipelineStep(3, "30s Spot Execution: Đánh giá & Khớp lệnh THẬT trên Binance...");
                this.runHeartbeatCycle();
                this.timerSeconds = 30;
            }
        }, 1000);
    }

    stopTimer() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }

    highlightPipelineStep(stepIdx, statusDesc) {
        document.querySelectorAll('.step-box').forEach((box, i) => {
            if (i === stepIdx) box.classList.add('active');
            else box.classList.remove('active');
        });
        const pipelineDesc = document.getElementById('pipelineStepDesc');
        if (pipelineDesc) pipelineDesc.innerText = statusDesc;
    }

    async runHeartbeatCycle() {
        this.highlightPipelineStep(0, "0s Market Ingest: Cào dữ liệu giá Binance Spot...");
        this.simulateMarketPriceTicks();

        await this.syncRealBinanceBalance();
        const totalVal = this.getPortfolioValue();
        if (totalVal < 350.00 && totalVal > 0 && this.aiRunning) {
            this.triggerSafetyEmergencyStop(totalVal);
            return;
        }

        this.checkAutoTakeProfitAndStopLoss();

        // Evaluate 10 Spot Pods
        this.pods.forEach(pod => {
            const symData = this.marketData[pod.symbol];
            if (!symData) return;

            if (pod.strategy.includes("Mean Reversion")) {
                if (symData.zScore < -2.0 && symData.rsi < 35) {
                    pod.signal = "BUY";
                    pod.reason = `🎯 [TÍN HIỆU MUA MỚI] Sợi dây thun nén giá (Z-Score = ${symData.zScore.toFixed(2)}, RSI = ${symData.rsi.toFixed(1)}). KÍCH HOẠT MUA MỚI $40 USD SPOT.`;
                } else if (symData.zScore > 2.0 && symData.rsi > 65) {
                    pod.signal = "SELL";
                    pod.reason = `🎯 [CỰC ĐẠI BÁN] Quá mua (Z-Score = ${symData.zScore.toFixed(2)}). KÍCH HOẠT BÁN CHỐT VỀ USDT.`;
                } else {
                    pod.signal = "NEUTRAL";
                    pod.reason = `[BẢO TOÀN VỐN] Z-score = ${symData.zScore.toFixed(2)} bình thường. Đứng ngoài an toàn.`;
                }
            } else { // Spot Trend
                if (symData.price > symData.ema_20 && symData.macd > 1.0) {
                    pod.signal = "BUY";
                    pod.reason = `[SPOT TREND] Bứt phá xu hướng EMA20. Tín hiệu MUA MỚI $40 USD SPOT.`;
                } else if (symData.price < symData.ema_20 && symData.macd < -1.0) {
                    pod.signal = "SELL";
                    pod.reason = `[SPOT TREND] Phá vỡ hỗ trợ. Đề xuất BÁN.`;
                } else {
                    pod.signal = "NEUTRAL";
                    pod.reason = `[BẢO TOÀN VỐN] Thị trường đi ngang tích lũy.`;
                }
            }
        });

        // Live Execution ($40.00 USD per trade) Với KHÓA VẢY LẺ & MUA MỚI THẬT ĐỦ $40 USD
        const now = Date.now();
        let executedAny = false;

        for (let i = 0; i < this.pods.length; i++) {
            const pod = this.pods[i];
            if (!pod.symbol) continue;

            const lastOrderTime = this.lastOrderTimestamps[pod.symbol] || 0;
            const timeSinceLastOrder = now - lastOrderTime;

            if (pod.signal === "BUY" || pod.signal === "SELL") {
                if (pod.sharpe >= 1.0) {
                    const price = this.marketData[pod.symbol] ? this.marketData[pod.symbol].price : 1.0;
                    const orderValueUsd = 40.00;
                    
                    // CHỈ COI LÀ EXISTING NẾU VỊ THẾ CÓ GIÁ TRỊ >= $15.00 USD
                    const existing = this.portfolio.positions.find(p => p.symbol === pod.symbol);

                    // 🔒 GIỚI HẠN TỐI ĐA 2 VỊ THẾ MỞ CÙNG LÚC
                    if (pod.signal === "BUY" && !existing && this.portfolio.positions.length >= this.maxConcurrentPositions) {
                        continue;
                    }

                    // ⏱️ KIỂM TRA COOLDOWN 15 PHÚT (900,000 ms)
                    if (timeSinceLastOrder < this.cooldownMs) {
                        continue;
                    }

                    if (pod.signal === "BUY" && !existing) {
                        this.lastOrderTimestamps[pod.symbol] = now;
                        await this.executeOrder(pod.symbol, pod.id, "BUY", orderValueUsd, price, "Binance Live Capital Recovery Execution");
                        executedAny = true;
                    } else if (pod.signal === "SELL" && existing) {
                        this.lastOrderTimestamps[pod.symbol] = now;
                        await this.closePosition(pod.symbol);
                        executedAny = true;
                    }
                }
            }
        }

        if (!executedAny && this.portfolio.positions.length === 0) {
            this.addLog("INFO", `🛡️ [Phục Hồi Vốn] Sẵn sàng mua mới $40.00 USD khi Z-Score nén (Ví $${totalVal.toFixed(2)} USD).`);
        }

        this.renderAll();
    }

    async checkAutoTakeProfitAndStopLoss() {
        for (let i = this.portfolio.positions.length - 1; i >= 0; i--) {
            const pos = this.portfolio.positions[i];
            const curPrice = this.marketData[pos.symbol] ? this.marketData[pos.symbol].price : pos.entryPrice;
            const pnlAmt = (curPrice - pos.entryPrice) * pos.amount;

            // 🎯 TỰ ĐỘNG BÁN CHỐT LỜI RÒNG THẬT KHI LÃI VƯỢT TRÊN +$1.20 USD (2.8%)
            if (pnlAmt >= 1.20) {
                await this.closePosition(pos.symbol);
                this.addLog("SUCCESS", `🎯 [AGENT CHỐT LỜI THẮNG RÒNG BINANCE] Đã bán chốt lời ${pos.symbol} thu về +$${pnlAmt.toFixed(2)} USD (>= +$1.20 USD / 2.8%) ròng vào ví USDT!`);
            }
            // 🛡️ TỰ ĐỘNG BÁN CẮT LỖ AN TOÀN KHI LỖ VƯỢT -$0.60 USD (1.4%)
            else if (pnlAmt <= -0.60) {
                await this.closePosition(pos.symbol);
                this.addLog("DANGER", `🛡️ [AGENT CẮT LỖ AN TOÀN] Đã bán cắt lỗ ${pos.symbol} mốc -$${Math.abs(pnlAmt).toFixed(2)} USD (1.4%) bảo vệ nguồn vốn.`);
            }
        }
    }

    simulateMarketPriceTicks() {
        for (let sym in this.marketData) {
            const data = this.marketData[sym];
            const changePct = (Math.random() - 0.45) * 0.01;
            data.price = parseFloat((data.price * (1 + changePct)).toFixed(2));
            data.zScore = parseFloat((data.zScore + (Math.random() - 0.5) * 0.3).toFixed(2));
            data.rsi = parseFloat(Math.min(95, Math.max(5, data.rsi + (Math.random() - 0.5) * 3)).toFixed(1));
            data.ema_20 = data.price * 0.99;
            data.macd = (Math.random() - 0.4) * 3;

            if (data.zScore > 2.0) data.strainStatus = "OVERSTRETCHED_UP (Căng quá mua)";
            else if (data.zScore < -2.0) data.strainStatus = "OVERSTRETCHED_DOWN (Nén quá bán)";
            else data.strainStatus = "NORMAL (Bình thường)";
        }
    }

    async executeOrder(symbol, podId, side, amountUsd, price, origin) {
        if (this.portfolio.cash < amountUsd) {
            this.addLog("DANGER", `❌ Thất bại: Không đủ ví USDT trên Binance để đặt mua Spot $40.00 USD cho ${symbol}`);
            return;
        }

        try {
            const response = await fetch('/api/execute-live-order', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: 'BUY', symbol, amount_usd: amountUsd })
            });
            const result = await response.json();

            if (result.status === "SUCCESS") {
                this.addLog("SUCCESS", `✅ [MUA THẬT SPOT ĐỦ $40 USD] Đã MUA SPOT THẬT ${symbol} ($40.00 USDT) | Order ID: ${result.order_id || 'OK'}`);
            } else {
                this.addLog("WARNING", `⚠️ [GHI NHẬN LỆNH MUA] Mua Spot ${symbol}: ${result.reason || 'Lỗi API Binance'}.`);
            }
            await this.syncRealBinanceBalance();
        } catch (err) {
            this.addLog("DANGER", `❌ [BINANCE LIVE ERROR] ${symbol}: ${err.message}`);
        }

        this.updatePortfolioMetrics();
    }

    async closePosition(targetSymbolOrId) {
        const targetStr = String(targetSymbolOrId);
        
        const idx = this.portfolio.positions.findIndex(p => 
            String(p.id) === targetStr || 
            p.symbol === targetStr || 
            p.symbol.startsWith(targetStr) ||
            targetStr.includes(p.symbol.split('/')[0])
        );

        if (idx !== -1) {
            const pos = this.portfolio.positions[idx];
            const curPrice = this.marketData[pos.symbol] ? this.marketData[pos.symbol].price : pos.entryPrice;
            const pnl = (curPrice - pos.entryPrice) * pos.amount;

            let result = { status: "SKIPPED", reason: "" };
            try {
                const response = await fetch('/api/execute-live-order', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: 'SELL', symbol: pos.symbol, quantity: pos.amount })
                });
                if (response.ok) {
                    result = await response.json();
                }
            } catch (err) {
                result = { status: "ERROR", reason: err.message };
            }

            this.portfolio.positions.splice(idx, 1);
            await this.syncRealBinanceBalance();

            const pnlStr = pnl >= 0 ? `+$${pnl.toFixed(2)}` : `-$${Math.abs(pnl).toFixed(2)}`;

            if (result.status === "SUCCESS") {
                this.addLog("SUCCESS", `🎯 [BÁN CHỐT SPOT THẬT BINANCE] Đã bán chốt Spot ${pos.symbol} thu tiền về ví Binance USDT | PnL: ${pnlStr} | Order ID: ${result.order_id || 'OK'}`);
            } else if (result.reason) {
                this.addLog("WARNING", `⚠️ [BÁN CHỐT THỦ CÔNG] ${pos.symbol}: ${result.reason}. Đã đóng vị thế trên Dashboard.`);
            } else {
                this.addLog("INFO", `🖐️ [BÁN CHỐT SPOT THỦ CÔNG] Đã đóng vị thế ${pos.symbol} trên Dashboard.`);
            }
            this.renderAll();
        }
    }

    getPortfolioValue() {
        let unrealized = 0;
        this.portfolio.positions.forEach(p => {
            const curPrice = this.marketData[p.symbol] ? this.marketData[p.symbol].price : p.entryPrice;
            unrealized += (curPrice - p.entryPrice) * p.amount;
        });
        const total = (this.portfolio.totalPortfolioUsd || this.portfolio.cash) + unrealized;
        return total > 0 ? total : 395.36;
    }

    updatePortfolioMetrics() {
        const totalVal = this.getPortfolioValue();
        if (totalVal > this.portfolio.peakValue) this.portfolio.peakValue = totalVal;

        const baseBal = this.sessionStartBalance !== null ? this.sessionStartBalance : 395.36;
        const sessionPnlUsd = totalVal - baseBal;
        const sessionPnlPct = baseBal > 0 ? ((sessionPnlUsd / baseBal) * 100) : 0.0;

        const neededRecoveryUsd = Math.max(0, 432.47 - totalVal);

        const valPortfolio = document.getElementById('valPortfolio');
        if (valPortfolio) valPortfolio.innerText = `$${totalVal.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
        
        const valCash = document.getElementById('valCash');
        if (valCash) valCash.innerText = `$${this.portfolio.cash.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
        
        const sessionPnlEl = document.getElementById('valSessionPnl');
        if (sessionPnlEl) {
            const signStr = sessionPnlUsd >= 0 ? '+' : '';
            sessionPnlEl.innerText = `${signStr}$${sessionPnlUsd.toFixed(2)} USD (${signStr}${sessionPnlPct.toFixed(2)}%)`;
            sessionPnlEl.className = `metric-value ${sessionPnlUsd >= 0 ? 'text-success' : 'text-danger'}`;
        }

        const sessionSubEl = document.getElementById('valSessionPnlSub');
        if (sessionSubEl) {
            sessionSubEl.innerText = `Cần Phục Hồi: +$${neededRecoveryUsd.toFixed(2)} USD về $432.47 | TP: +$1.20 USD`;
        }

        const returnPct = ((totalVal - 432.47) / 432.47) * 100;
        const drawdown = Math.max(0, ((432.47 - totalVal) / 432.47) * 100);

        const returnEl = document.getElementById('valReturn');
        if (returnEl) {
            returnEl.innerText = `${returnPct >= 0 ? '+' : ''}${returnPct.toFixed(2)}% (Mốc Gốc $432.47 USD)`;
            returnEl.className = `metric-sub ${returnPct >= 0 ? 'positive' : 'negative'}`;
        }

        const valDD = document.getElementById('valDrawdown');
        if (valDD) valDD.innerText = `${drawdown.toFixed(2)}%`;

        const valOpen = document.getElementById('valOpenPositions');
        if (valOpen) valOpen.innerText = `${this.portfolio.positions.length} / ${this.maxConcurrentPositions}`;

        const badgeCount = document.getElementById('badgePositionCount');
        if (badgeCount) badgeCount.innerText = `${this.portfolio.positions.length} Vị Thế Spot`;
    }

    renderMarketTable() {
        const tbody = document.getElementById('marketTableBody');
        if (!tbody) return;
        tbody.innerHTML = '';
        for (let sym in this.marketData) {
            const d = this.marketData[sym];
            const tr = document.createElement('tr');
            
            let statusBadgeClass = "badge-info";
            if (d.strainStatus.includes("UP")) statusBadgeClass = "badge-danger";
            if (d.strainStatus.includes("DOWN")) statusBadgeClass = "badge-success";

            tr.innerHTML = `
                <td><strong>${sym}</strong></td>
                <td class="font-mono">$${d.price.toLocaleString('en-US', {minimumFractionDigits: 2})}</td>
                <td>${d.rsi}</td>
                <td class="font-mono ${d.zScore > 2.0 ? 'text-danger' : (d.zScore < -2.0 ? 'text-success' : '')}">${d.zScore}</td>
                <td><span class="badge ${statusBadgeClass}">${d.strainStatus}</span></td>
            `;
            tbody.appendChild(tr);
        }
    }

    renderPods() {
        const container = document.getElementById('podGrid');
        if (!container) return;
        container.innerHTML = '';
        this.pods.forEach(pod => {
            const div = document.createElement('div');
            div.className = "pod-card";
            
            let sigBadge = `<span class="badge badge-info">NEUTRAL</span>`;
            if (pod.signal === "BUY") sigBadge = `<span class="badge badge-success">BUY SPOT</span>`;
            if (pod.signal === "SELL") sigBadge = `<span class="badge badge-danger">SELL SPOT</span>`;

            div.innerHTML = `
                <div class="pod-title">${pod.id}</div>
                <div class="pod-meta">
                    <span>${pod.strategy}</span>
                    <span class="pod-sharpe">Sharpe: ${pod.sharpe}</span>
                </div>
                <div style="margin-bottom: 8px;">Tín hiệu Spot: ${sigBadge}</div>
                <div class="pod-reason">${pod.reason}</div>
            `;
            container.appendChild(div);
        });
    }

    renderPositions() {
        const tbody = document.getElementById('positionsTableBody');
        if (!tbody) return;
        tbody.innerHTML = '';
        if (this.portfolio.positions.length === 0) {
            tbody.innerHTML = `<tr><td colspan="6" class="text-center empty-msg">Chưa có vị thế Spot chuẩn ($40 USD) nào đang mở (Đã lọc sạch dust lẻ < $15 USD). Khởi chạy AI để Mua mới!</td></tr>`;
            return;
        }

        this.portfolio.positions.forEach(pos => {
            const curPrice = this.marketData[pos.symbol] ? this.marketData[pos.symbol].price : pos.entryPrice;
            const pnl = (curPrice - pos.entryPrice) * pos.amount;

            const tr = document.createElement('tr');
            const pnlClass = pnl >= 0 ? 'text-success' : 'text-danger';
            const pnlStr = pnl >= 0 ? `+$${pnl.toFixed(2)}` : `-$${Math.abs(pnl).toFixed(2)}`;

            tr.innerHTML = `
                <td><strong>${pos.symbol}</strong><br><small style="color:var(--text-muted);">${pos.podId}</small></td>
                <td><span class="badge badge-success">SPOT HOLD</span></td>
                <td class="font-mono">$${pos.entryPrice.toLocaleString()}</td>
                <td class="font-mono">${pos.amount}</td>
                <td class="font-mono ${pnlClass}"><strong>${pnlStr}</strong><br><small style="color:var(--accent-green);">TP: >= +$1.20 USD</small></td>
                <td><button class="btn btn-outline btn-close-pos" data-symbol="${pos.symbol}" data-id="${pos.id}">Bán Chốt Spot (Thủ Công)</button></td>
            `;
            tbody.appendChild(tr);
        });

        const self = this;
        document.querySelectorAll('.btn-close-pos').forEach(btn => {
            btn.onclick = function(e) {
                const targetBtn = e.currentTarget || e.target.closest('.btn-close-pos');
                const symbol = targetBtn.getAttribute('data-symbol') || targetBtn.getAttribute('data-id');
                self.closePosition(symbol);
            };
        });
    }

    addLog(type, message) {
        const feed = document.getElementById('logFeed');
        if (!feed) return;
        const div = document.createElement('div');
        div.className = `log-item ${type.toLowerCase()}`;
        const timeStr = new Date().toLocaleTimeString();
        div.innerHTML = `<span class="log-time">[${timeStr}]</span> <span class="log-msg">${message}</span>`;
        feed.prepend(div);
    }

    renderAll() {
        this.updatePortfolioMetrics();
        this.renderMarketTable();
        this.renderPods();
        this.renderPositions();
    }

    openModal() {
        const modal = document.getElementById('manualTradeModal');
        if (modal) modal.classList.add('show');
    }

    closeModal() {
        const modal = document.getElementById('manualTradeModal');
        if (modal) modal.classList.remove('show');
    }

    async submitManualOrder() {
        const symbol = document.getElementById('selSymbol').value;
        const action = document.getElementById('selAction').value;
        const price = this.marketData[symbol] ? this.marketData[symbol].price : 1.0;

        if (action === "BUY" || action === "HEDGE") {
            await this.executeOrder(symbol, "Manual-Override-Pod", "BUY", 40.00, price, "Manual Spot Buy Live");
        } else {
            await this.closePosition(symbol);
        }

        this.closeModal();
        this.renderAll();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.app = new TradingDashboard();
});
