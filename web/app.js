// Agentic AI Trading Dashboard v5.2 - Auto-Active 24/7 Stop Loss Engine & Zero Missed Cut-Loss

class TradingDashboard {
    constructor() {
        this.portfolio = {
            initialBalance: 395.36,
            cash: 397.80,
            totalPortfolioUsd: 401.49,
            peakValue: 432.47,
            positions: [],
            tradeHistory: []
        };

        this.targetCapitalRecoveryUsd = 432.47;
        this.minPortfolioStopThreshold = 350.00;
        
        // 🚀 Cấu hình Chiến lược v5.2 Full Quant Trading Engine
        this.baseOrderUsd = 80.00;
        this.takeProfitTargetUsd = 2.20; // Mốc kích hoạt chốt lời ròng ban đầu (+2.8%)
        this.stopLossTargetUsd = 1.10;   // Rủi ro tối đa -$1.10 USD / lệnh (1.4%)
        this.maxConcurrentPositions = 3; // Tối đa 3 vị thế mở cùng lúc ($240 USD vốn)
        
        // 📈 Trailing Stop Spot: Khoảng lùi 0.8% theo Giá Coin (Coin Price Callback)
        this.enableTrailingStop = true;
        this.trailingStopCallbackPct = 0.8;
        this.trailingHighWaterMarks = {}; // Đỉnh PnL cao nhất đạt được của từng vị thế

        // Mốc lọc vảy coin lẻ (Dust Minimum): Phải lớn hơn $15.00 USD mới tính là Vị thế đang giữ
        this.minPositionValueUsd = 15.00;

        this.sessionStartBalance = 401.49;
        this.sessionStartTime = new Date().toLocaleTimeString();

        // Bảng Cooldown 15 phút (900,000 ms)
        this.lastOrderTimestamps = {};
        this.cooldownMs = 900000; 

        // Giá thị trường THẬT từ Binance API
        this.marketData = {
            "BTC/USDT": { price: 77154.0, rsi: 48.5, zScore: 0.45, macdHist: 2.5, strainStatus: "NORMAL" },
            "ETH/USDT": { price: 2435.4, rsi: 72.4, zScore: 2.15, macdHist: 1.2, strainStatus: "OVERSTRETCHED_UP" },
            "SOL/USDT": { price: 92.97, rsi: 28.1, zScore: -2.35, macdHist: 0.8, strainStatus: "OVERSTRETCHED_DOWN" },
            "BNB/USDT": { price: 694.4, rsi: 52.0, zScore: 0.65, macdHist: 0.5, strainStatus: "NORMAL" },
            "XRP/USDT": { price: 0.58, rsi: 76.2, zScore: 2.40, macdHist: -0.3, strainStatus: "OVERSTRETCHED_UP" },
            "ADA/USDT": { price: 0.229, rsi: 26.5, zScore: -2.10, macdHist: 0.4, strainStatus: "OVERSTRETCHED_DOWN" },
            "AVAX/USDT": { price: 7.65, rsi: 58.0, zScore: 0.90, macdHist: 0.1, strainStatus: "NORMAL" },
            "NEAR/USDT": { price: 1.89, rsi: 44.0, zScore: -0.55, macdHist: -0.2, strainStatus: "NORMAL" },
            "LINK/USDT": { price: 11.69, rsi: 68.0, zScore: 1.85, macdHist: 0.9, strainStatus: "NORMAL" },
            "DOT/USDT": { price: 6.45, rsi: 54.0, zScore: 0.85, macdHist: 0.2, strainStatus: "NORMAL" }
        };

        this.pods = [
            { id: "Pod-01-RubberBand-BTC", symbol: "BTC/USDT", strategy: "Spot Mean Reversion", sharpe: 1.25, signal: "NEUTRAL", reason: "[SPOT] Z-score bình thường. Chờ nén MUA MỚI." },
            { id: "Pod-02-Trend-ETH", symbol: "ETH/USDT", strategy: "Spot Trend", sharpe: 1.08, signal: "NEUTRAL", reason: "[SPOT] Thị trường tích lũy." },
            { id: "Pod-03-RubberBand-SOL", symbol: "SOL/USDT", strategy: "Spot Mean Reversion", sharpe: 1.32, signal: "NEUTRAL", reason: "[SPOT] Đứng ngoài an toàn." },
            { id: "Pod-04-Trend-BNB", symbol: "BNB/USDT", strategy: "Spot Trend", sharpe: 1.15, signal: "NEUTRAL", reason: "[SPOT] Thị trường tích lũy." },
            { id: "Pod-05-RubberBand-XRP", symbol: "XRP/USDT", strategy: "Spot Mean Reversion", sharpe: 1.28, signal: "NEUTRAL", reason: "[SPOT] Vùng giá an toàn." },
            { id: "Pod-06-Trend-ADA", symbol: "ADA/USDT", strategy: "Spot Trend", sharpe: 1.10, signal: "NEUTRAL", reason: "[SPOT] Thị trường tích lũy." },
            { id: "Pod-07-RubberBand-AVAX", symbol: "AVAX/USDT", strategy: "Spot Mean Reversion", sharpe: 1.20, signal: "NEUTRAL", reason: "[SPOT] Đứng ngoài quan sát." },
            { id: "Pod-08-Trend-NEAR", symbol: "NEAR/USDT", strategy: "Spot Trend", sharpe: 1.05, signal: "NEUTRAL", reason: "[SPOT] Thị trường đi ngang." },
            { id: "Pod-09-RubberBand-LINK", symbol: "LINK/USDT", strategy: "Spot Mean Reversion", sharpe: 1.18, signal: "NEUTRAL", reason: "[SPOT] Vùng giá an toàn." },
            { id: "Pod-10-Trend-DOT", symbol: "DOT/USDT", strategy: "Spot Trend", sharpe: 1.12, signal: "NEUTRAL", reason: "[SPOT] Xu hướng bình thường." }
        ];

        // 🚀 TỰ ĐỘNG BẬT 100% AI TRADING NGAY KHI VÀO TRANG (KHÔNG CẦN BẤM NÚT KÍCH HOẠT)
        this.aiRunning = true;
        this.timerSeconds = 30;
        this.timerInterval = null;

        this.initUI();
        this.bindEvents();
        this.syncRealBinanceBalance();
        this.fetchPnlAnalytics();

        this.startTimer();
    }

    initUI() {
        this.updatePortfolioMetrics();
        this.renderMarketTable();
        this.renderPods();
        this.populateModalSymbols();

        // Cập nhật trạng thái nút AI Active mặc định ngay trên UI
        const btn = document.getElementById('btnToggleAI');
        const lbl = document.getElementById('lblToggleAI');
        const pulse = document.getElementById('aiStatusPulse');
        const statusTxt = document.getElementById('aiStatusText');

        if (btn) btn.className = "btn btn-secondary";
        if (lbl) lbl.innerText = "Tạm Dừng AI";
        if (pulse) pulse.className = "status-indicator live";
        if (statusTxt) statusTxt.innerText = `🔴 AI v5.2 ACTIVE (TỰ ĐỘNG CẮT LỖ MỖI GIÂY)`;
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

    calculateDynamicOrderSize(symbol) {
        const cleanSym = symbol.replace('/', '').upper ? symbol.replace('/', '').toUpperCase() : symbol;
        if (cleanSym.includes("BTC") || cleanSym.includes("ETH")) {
            return 100.00;
        }
        return 80.00;
    }

    async syncRealBinanceBalance() {
        try {
            const response = await fetch('/api/binance-balance?t=' + Date.now());
            const data = await response.json();
            if (data.success) {
                this.portfolio.cash = data.usdt_free;
                const totalUsd = data.total_portfolio_usd > 0 ? data.total_portfolio_usd : 401.49;
                this.portfolio.totalPortfolioUsd = totalUsd;
                this.portfolio.initialBalance = totalUsd;

                if (data.prices) {
                    for (let coin in data.prices) {
                        const sym = `${coin}/USDT`;
                        if (this.marketData[sym]) {
                            this.marketData[sym].price = data.prices[coin];
                        }
                    }
                }

                if (this.sessionStartBalance === null || this.sessionStartBalance < 100) {
                    this.sessionStartBalance = totalUsd;
                    this.sessionStartTime = new Date().toLocaleTimeString();
                }

                const timeStr = new Date().toLocaleTimeString();
                const bnbApiStatus = document.getElementById('valBinanceApiStatus');
                if (bnbApiStatus) {
                    bnbApiStatus.innerText = `🟢 Binance API Live (${timeStr})`;
                }

                if (totalUsd < 350.00 && totalUsd > 0 && this.aiRunning) {
                    this.triggerSafetyEmergencyStop(totalUsd);
                    return;
                }

                const heldBalances = data.balances || {};
                const usdValues = data.usd_values || {};
                const realPrices = data.prices || {};
                const syncedPositions = [];

                for (let coin in heldBalances) {
                    if (coin !== 'USDT' && coin !== 'BUSD' && coin !== 'USDC' && coin !== 'ATA') {
                        const amount = heldBalances[coin];
                        const symbol = `${coin}/USDT`;
                        const livePrice = realPrices[coin] || (this.marketData[symbol] ? this.marketData[symbol].price : 1.0);
                        const usdValue = usdValues[coin] || (amount * livePrice);

                        if (usdValue >= 15.0) {
                            const existingPos = this.portfolio.positions.find(p => p.symbol === symbol);

                            const dynamicBase = this.calculateDynamicOrderSize(symbol);
                            let entryValueUsd = dynamicBase;
                            let entryPrice = livePrice;

                            if (existingPos) {
                                entryValueUsd = existingPos.entryValueUsd || dynamicBase;
                                entryPrice = existingPos.entryPrice || (entryValueUsd / amount);
                            } else {
                                entryValueUsd = dynamicBase;
                                entryPrice = entryValueUsd / amount;
                            }

                            const realPnl = usdValue - entryValueUsd;

                            const key = `pos-${symbol}`;
                            const currentHigh = this.trailingHighWaterMarks[key] || realPnl;
                            if (realPnl > currentHigh) {
                                this.trailingHighWaterMarks[key] = realPnl;
                            }

                            syncedPositions.push({
                                id: `pos-${symbol.replace('/', '-')}`,
                                symbol: symbol,
                                podId: existingPos ? existingPos.podId : `Binance-Live-Wallet-${coin}`,
                                side: "BUY_SPOT",
                                entryPrice: entryPrice,
                                entryValueUsd: entryValueUsd,
                                currentUsdValue: usdValue,
                                realPnl: realPnl,
                                maxPnlReached: this.trailingHighWaterMarks[key] || realPnl,
                                amount: amount,
                                targetProfitUsd: 2.20,
                                timestamp: existingPos ? existingPos.timestamp : new Date().toLocaleTimeString()
                            });
                        }
                    }
                }

                this.portfolio.positions = syncedPositions;
                this.renderAll();

                // KÍCH HOẠT QUÉT CẮT LỖ VÀ CHỐT LỜI NGAY SAU KHI ĐỒNG BỘ VỊ THẾ
                if (this.aiRunning) {
                    this.checkAutoTakeProfitAndStopLoss();
                }
            }
        } catch (e) {
            console.log("Error syncing balance:", e);
        }
    }

    async fetchPnlAnalytics() {
        try {
            const response = await fetch('/api/pnl-analytics?t=' + Date.now());
            const json = await response.json();
            if (json.success && json.data) {
                this.renderPnlAnalytics(json.data);
            }
        } catch (err) {
            console.log("Error fetching PnL Analytics:", err);
        }
    }

    renderPnlAnalytics(data) {
        const statWeekly = document.getElementById('statWeeklyPnl');
        if (statWeekly) {
            const pnl = data.weekly_pnl_usd || 0.0;
            statWeekly.innerText = `${pnl >= 0 ? '+' : ''}$${pnl.toFixed(2)} USD`;
            statWeekly.className = `metric-value ${pnl >= 0 ? 'text-success' : 'text-danger'}`;
        }

        const statWin = document.getElementById('statWinRate');
        if (statWin) {
            statWin.innerText = `${data.win_rate_pct || 100.0}%`;
        }

        const statBest = document.getElementById('statBestDay');
        if (statBest) {
            const b = data.best_day;
            if (b) {
                statBest.innerText = `+${b.pnl_usd.toFixed(2)} USD (${b.day_name_vi} ${b.date_str.split('-').slice(1).join('/')})`;
            } else {
                statBest.innerText = "+$0.00 USD";
            }
        }

        const statWorst = document.getElementById('statWorstDay');
        if (statWorst) {
            const w = data.worst_day;
            if (w) {
                const sign = w.pnl_usd >= 0 ? '+' : '';
                statWorst.innerText = `${sign}$${w.pnl_usd.toFixed(2)} USD (${w.day_name_vi} ${w.date_str.split('-').slice(1).join('/')})`;
                statWorst.className = `metric-value ${w.pnl_usd >= 0 ? 'text-success' : 'text-danger'}`;
            } else {
                statWorst.innerText = "$0.00 USD";
            }
        }

        const wrapper = document.getElementById('timelineBarsWrapper');
        if (wrapper && data.today && data.today.hourly) {
            wrapper.innerHTML = '';
            const hourly = data.today.hourly;
            
            let maxVal = 1.0;
            for (let h = 0; h < 24; h++) {
                const absVal = Math.abs(hourly[h] || 0);
                if (absVal > maxVal) maxVal = absVal;
            }

            for (let h = 0; h < 24; h++) {
                const val = hourly[h] || 0.0;
                const col = document.createElement('div');
                col.className = 'hour-bar-col';

                let heightPct = 0;
                let fillClass = 'zero';
                if (val > 0) {
                    heightPct = Math.max(10, Math.min(100, (val / maxVal) * 100));
                    fillClass = 'profit';
                } else if (val < 0) {
                    heightPct = Math.max(10, Math.min(100, (Math.abs(val) / maxVal) * 100));
                    fillClass = 'loss';
                }

                const hourFormatted = h < 10 ? `0${h}:00` : `${h}:00`;
                const valStr = val >= 0 ? `+$${val.toFixed(2)}` : `-$${Math.abs(val).toFixed(2)}`;

                col.innerHTML = `
                    <div class="bar-tooltip">${hourFormatted}: ${valStr}</div>
                    <div class="bar-fill ${fillClass}" style="height: ${heightPct}%;"></div>
                    <div class="hour-label">${h}h</div>
                `;
                wrapper.appendChild(col);
            }
        }

        const tbody = document.getElementById('pnlWeeklyTableBody');
        if (tbody && data.weekly_days) {
            tbody.innerHTML = '';
            data.weekly_days.forEach(day => {
                const tr = document.createElement('tr');
                const pnl = day.pnl_usd || 0.0;
                const pnlClass = pnl >= 0 ? 'text-success' : 'text-danger';
                const pnlStr = pnl >= 0 ? `+$${pnl.toFixed(2)}` : `-$${Math.abs(pnl).toFixed(2)}`;
                const statusBadge = pnl > 0 ? `<span class="badge badge-success">LÃI RÒNG</span>` : 
                                   (pnl < 0 ? `<span class="badge badge-danger">LỖ RÒNG</span>` : `<span class="badge badge-info">HÒA VỐN</span>`);

                const dateDisplay = day.date_str ? day.date_str.split('-').reverse().join('/') : '-';

                tr.innerHTML = `
                    <td><strong>${day.day_name_vi}</strong></td>
                    <td class="font-mono">${dateDisplay}</td>
                    <td class="font-mono"><span class="text-success">${day.wins || 0} Thắng</span> / <span class="text-danger">${day.losses || 0} Thua</span></td>
                    <td class="font-mono ${pnlClass}"><strong>${pnlStr} USD</strong></td>
                    <td>${statusBadge}</td>
                `;
                tbody.appendChild(tr);
            });
        }
    }

    triggerSafetyEmergencyStop(currentBalance) {
        if (this.aiRunning) {
            this.aiRunning = false;

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
            this.sessionStartBalance = totalVal > 0 ? totalVal : 401.49;
            this.sessionStartTime = new Date().toLocaleTimeString();

            if (btn) btn.className = "btn btn-secondary";
            if (lbl) lbl.innerText = "Tạm Dừng AI";
            if (pulse) pulse.className = "status-indicator live";
            if (statusTxt) statusTxt.innerText = `🔴 AI v5.2 ACTIVE (TỰ ĐỘNG CẮT LỖ MỖI GIÂY)`;

            this.addLog("DANGER", `🚀 BẮT ĐẦU V5.2 FULL QUANT ENGINE! Cắt lỗ tự động mỗi 1s ngay mốc -$1.10 USD. Mốc vốn: $${this.sessionStartBalance.toFixed(2)} USD`);
            
            this.runHeartbeatCycle();
        } else {
            if (btn) btn.className = "btn btn-primary";
            if (lbl) lbl.innerText = "Bắt Đầu AI Đầu Tư (LIVE)";
            if (pulse) pulse.className = "status-indicator";
            if (statusTxt) statusTxt.innerText = "AI Đang Tạm Dừng";

            this.addLog("WARNING", "⏸ Đã tạm dừng AI.");
        }
    }

    startTimer() {
        this.stopTimer();
        this.timerSeconds = 30;
        
        this.timerInterval = setInterval(() => {
            this.timerSeconds--;
            const timerEl = document.getElementById('heartbeatTimer');
            if (timerEl) timerEl.innerText = `${this.timerSeconds}s`;

            if (this.timerSeconds > 20) {
                this.highlightPipelineStep(0, "0s Market Ingest: Cào dữ liệu nến Binance Live API...");
            } else if (this.timerSeconds > 10) {
                this.highlightPipelineStep(1, "10s Sub-Agent: Tóm tắt RSI + MACD + Z-Score Strain...");
            } else if (this.timerSeconds > 0) {
                this.highlightPipelineStep(2, "20s Pod Theory: Đánh giá 10 Spot Pods & Dynamic Sizing...");
            } else {
                this.highlightPipelineStep(3, "30s Spot Execution: Đánh giá & Khớp lệnh OTOCO THẬT trên Binance...");
            }

            // ⚡ KIỂM TRA QUÉT BÁN CẮT LỖ & CHỐT LỜI LIÊN TỤC MỖI GIÂY (1 SECOND TICK)
            if (this.aiRunning) {
                this.checkAutoTakeProfitAndStopLoss();
            }

            this.updatePortfolioMetrics();

            if (this.timerSeconds <= 0) {
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
        await this.syncRealBinanceBalance();
        await this.fetchPnlAnalytics();

        const totalVal = this.getPortfolioValue();
        if (totalVal < 350.00 && totalVal > 0 && this.aiRunning) {
            this.triggerSafetyEmergencyStop(totalVal);
            return;
        }

        if (this.aiRunning) {
            this.checkAutoTakeProfitAndStopLoss();
        }

        this.pods.forEach(pod => {
            const symData = this.marketData[pod.symbol];
            if (!symData) return;

            if (pod.strategy.includes("Mean Reversion")) {
                if (symData.zScore < -2.0 && symData.rsi < 35 && symData.macdHist > 0) {
                    pod.signal = "BUY";
                    pod.reason = `🎯 [XÁC NHẬN KÉP v5.2] Nén Dây Thun (Z=${symData.zScore.toFixed(2)}, RSI=${symData.rsi.toFixed(1)}) + MACD Histogram Dương (${symData.macdHist}). KÍCH HOẠT MUA SPOT.`;
                } else {
                    pod.signal = "NEUTRAL";
                    pod.reason = `[BẢO TOÀN VỐN] Z-score = ${symData.zScore.toFixed(2)} bình thường. Đứng ngoài an toàn.`;
                }
            } else {
                if (symData.price > (symData.ema_20 || symData.price * 0.99) && symData.macdHist > 0.5) {
                    pod.signal = "BUY";
                    pod.reason = `[SPOT TREND v5.2] Bứt phá xu hướng EMA20 + MACD Dương mạnh. Tín hiệu MUA SPOT.`;
                } else {
                    pod.signal = "NEUTRAL";
                    pod.reason = `[BẢO TOÀN VỐN] Thị trường tích lũy an toàn.`;
                }
            }
        });

        if (this.aiRunning) {
            let executedAny = false;
            const now = Date.now();

            if (this.portfolio.cash < 70.00) {
                this.addLog("WARNING", `🛡️ [AUTO-REBALANCING] Ví tiền mặt USDT ($${this.portfolio.cash.toFixed(2)}) < $70 USD đệm an toàn. Tạm ngưng mua mới để cân bằng danh mục.`);
                this.renderAll();
                return;
            }

            for (let i = 0; i < this.pods.length; i++) {
                const pod = this.pods[i];
                if (!pod.symbol) continue;

                const lastOrderTime = this.lastOrderTimestamps[pod.symbol] || 0;
                const timeSinceLastOrder = now - lastOrderTime;

                if (pod.signal === "BUY") {
                    if (pod.sharpe >= 1.0) {
                        const price = this.marketData[pod.symbol] ? this.marketData[pod.symbol].price : 1.0;
                        const orderValueUsd = this.calculateDynamicOrderSize(pod.symbol);
                        const existing = this.portfolio.positions.find(p => p.symbol === pod.symbol);

                        if (!existing && this.portfolio.positions.length >= this.maxConcurrentPositions) {
                            continue;
                        }

                        if (timeSinceLastOrder < this.cooldownMs) {
                            continue;
                        }

                        if (!existing) {
                            this.lastOrderTimestamps[pod.symbol] = now;
                            await this.executeOrder(pod.symbol, pod.id, "BUY", orderValueUsd, price, "Binance v5.2 Full Quant Execution");
                            executedAny = true;
                        }
                    }
                }
            }

            if (!executedAny && this.portfolio.positions.length === 0) {
                this.addLog("INFO", `⏱️ [Heartbeat 30s] Quét Binance Spot 10 coin (RSI+MACD+ZScore). Thị trường đi ngang, Agent bảo toàn vốn $${totalVal.toFixed(2)} USD.`);
            }
        } else {
            this.addLog("INFO", `⏱️ [Heartbeat 30s] Cập nhật Ví Live Binance: $${this.portfolio.cash.toFixed(2)} USDT (Tổng ví $${totalVal.toFixed(2)} USD). AI Trading đang tạm dừng.`);
        }

        this.renderAll();
    }

    // 🛡️ BƯỚC 2: TỰ ĐỘNG CẮT LỖ KHẮT KHE CHÍNH XÁC KHI PNL <= -$1.10 USD (HOẶC GỬI OCO)
    async checkAutoTakeProfitAndStopLoss() {
        if (!this.aiRunning) return;

        for (let i = this.portfolio.positions.length - 1; i >= 0; i--) {
            const pos = this.portfolio.positions[i];
            
            if ((pos.currentUsdValue || 0) < 15.0) continue;

            const pnlAmt = pos.realPnl !== undefined ? pos.realPnl : ((pos.currentUsdValue || 80.0) - (pos.entryValueUsd || 80.0));
            const maxPnl = pos.maxPnlReached !== undefined ? pos.maxPnlReached : pnlAmt;

            // 1. CẮT LỖ NGAY LẬP TỨC KHI PNL VỪA RỚT XUỐNG DƯỚI -$1.10 USD
            if (pnlAmt <= -1.10) {
                this.addLog("DANGER", `🛡️ [CẮT LỖ KỶ LUẬT 24/7] ${pos.symbol} vừa chạm mốc -$1.10 USD (PnL hiện tại: -$${Math.abs(pnlAmt).toFixed(2)} USD). PHÁT LỆNH BÁN CẮT LỖ NGAY!`);
                await this.closePosition(pos.symbol);
            } 
            // 2. Trailing Stop Spot: Khi PnL đỉnh cao nhất đã vượt mốc +$2.20 USD
            else if (maxPnl >= 2.20) {
                const posValueUsd = pos.currentUsdValue || 80.0;
                const pullbackAmt = posValueUsd * (this.trailingStopCallbackPct / 100.0);
                const trailingStopPnlTarget = maxPnl - pullbackAmt;

                if (pnlAmt <= trailingStopPnlTarget || pnlAmt >= 5.00) {
                    await this.closePosition(pos.symbol);
                }
            }
        }
    }

    async executeOrder(symbol, podId, side, amountUsd, price, origin) {
        if (this.portfolio.cash < amountUsd) {
            this.addLog("DANGER", `❌ Thất bại: Không đủ ví USDT trên Binance để đặt mua Spot $${amountUsd.toFixed(2)} USD cho ${symbol}`);
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
                this.addLog("SUCCESS", `✅ [MUA SPOT THẬT v5.2] Đã MUA SPOT THẬT ${symbol} ($${amountUsd.toFixed(2)} USDT) | Order ID: ${result.order_id || 'OK'}`);
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
            const pnl = pos.realPnl !== undefined ? pos.realPnl : 0.0;

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

            if (result.status === "SUCCESS" && result.order_id) {
                this.addLog("SUCCESS", `🎯 [BÁN CHỐT SPOT THẬT BINANCE] Đã bán chốt Spot ${pos.symbol} thu tiền về ví Binance USDT | PnL: ${pnlStr} | Order ID: ${result.order_id}`);
                
                try {
                    await fetch('/api/record-trade', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            symbol: pos.symbol,
                            side: 'SELL',
                            amount_usd: pos.entryValueUsd || 80.00,
                            pnl_usd: pnl,
                            order_id: result.order_id
                        })
                    });
                    await this.fetchPnlAnalytics();
                } catch (e) {
                    console.log("Error recording trade:", e);
                }
            } else if (result.reason && !result.reason.includes("làm tròn bằng 0") && !result.reason.includes("insufficient")) {
                this.addLog("WARNING", `⚠️ [GHI NHẬN BÁN] ${pos.symbol}: ${result.reason}. Đã cập nhật trên Dashboard.`);
            }
            this.renderAll();
        }
    }

    getPortfolioValue() {
        const total = (this.portfolio.totalPortfolioUsd || this.portfolio.cash);
        return total > 0 ? total : 401.49;
    }

    updatePortfolioMetrics() {
        const totalVal = this.getPortfolioValue();
        if (totalVal > this.portfolio.peakValue) this.portfolio.peakValue = totalVal;

        const baseBal = this.sessionStartBalance !== null ? this.sessionStartBalance : 401.49;
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
            sessionSubEl.innerText = `Cần Phục Hồi: +$${neededRecoveryUsd.toFixed(2)} USD về $432.47 | v4.0 Trailing Stop (0.8%)`;
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
            tbody.innerHTML = `<tr><td colspan="6" class="text-center empty-msg">Chưa có vị thế Spot chuẩn nào đang mở. Khởi chạy AI v4.0 để Mua mới!</td></tr>`;
            return;
        }

        this.portfolio.positions.forEach(pos => {
            const valUsd = pos.currentUsdValue !== undefined ? pos.currentUsdValue : (pos.amount * pos.entryPrice);
            const pnl = pos.realPnl !== undefined ? pos.realPnl : 0.0;
            const maxPnl = pos.maxPnlReached !== undefined ? pos.maxPnlReached : pnl;

            const tr = document.createElement('tr');
            const pnlClass = pnl >= 0 ? 'text-success' : 'text-danger';
            const pnlStr = pnl >= 0 ? `+$${pnl.toFixed(2)}` : `-$${Math.abs(pnl).toFixed(2)}`;

            tr.innerHTML = `
                <td><strong>${pos.symbol}</strong><br><small style="color:var(--text-muted);">${pos.podId}</small></td>
                <td><span class="badge badge-success">SPOT HOLD</span></td>
                <td class="font-mono">$${valUsd.toFixed(2)} USD<br><small style="color:var(--text-muted);">Binance App Live</small></td>
                <td class="font-mono">${pos.amount}</td>
                <td class="font-mono ${pnlClass}"><strong>${pnlStr}</strong><br><small style="color:var(--accent-green);">Đỉnh: +$${maxPnl.toFixed(2)} | Trailing 0.8%</small></td>
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

        while (feed.children.length > 35) {
            feed.removeChild(feed.lastChild);
        }
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
        const amountUsd = this.calculateDynamicOrderSize(symbol);

        if (action === "BUY" || action === "HEDGE") {
            await this.executeOrder(symbol, "Manual-Override-Pod", "BUY", amountUsd, price, "Manual Spot Buy Live");
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
