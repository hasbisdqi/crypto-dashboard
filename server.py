#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
import urllib.request

PORT = int(os.environ.get("PORT", 8088))
DATA_FILE = os.environ.get("DATA_FILE_PATH", os.path.expanduser("~/crypto_trading_bot.json"))

RECOMMENDED_INSTRUMENTS = [
    {
        "symbol": "SOL",
        "name": "Solana",
        "type": "Crypto (L1)",
        "asset_class": "Crypto",
        "coingecko_id": "solana",
        "horizon": "Jangka Pendek / Momentum",
        "thesis": "High throughput, biaya transaksi ultra-rendah, ekosistem DeFi & volume DEX bertumbuh pesat.",
        "risk_level": "Tinggi",
        "catalyst": "Inflow ekosistem & adopsi institusional",
        "badge": "Active Dual-Bucket"
    },
    {
        "symbol": "BTC",
        "name": "Bitcoin",
        "type": "Crypto (Store of Value)",
        "asset_class": "Crypto",
        "coingecko_id": "bitcoin",
        "horizon": "Jangka Panjang",
        "thesis": "Digital gold, pasokan terbatas 21 juta, ditopang ETF institusional global.",
        "risk_level": "Sedang-Tinggi",
        "catalyst": "Global ETF Inflows & Halving cycle",
        "badge": "Benchmark"
    },
    {
        "symbol": "ETH",
        "name": "Ethereum",
        "type": "Crypto (Smart Contract)",
        "asset_class": "Crypto",
        "coingecko_id": "ethereum",
        "horizon": "Menengah - Panjang",
        "thesis": "Jaringan Layer 1 paling terdesentralisasi dengan basis modal institusi terbesar.",
        "risk_level": "Sedang-Tinggi",
        "catalyst": "L2 Rollups scaling & Staking yields",
        "badge": "Core Asset"
    },
    {
        "symbol": "BBRI",
        "name": "Bank Rakyat Indonesia",
        "type": "Saham IDX (Perbankan)",
        "asset_class": "Stock",
        "price_approx": 3750,
        "lot_price": 375000,
        "div_yield": "~10.4%",
        "horizon": "Jangka Panjang / Dividen",
        "thesis": "Dominasi kredit mikro & UMKM Indonesia, rekor dividend payout ratio konsisten tinggi.",
        "risk_level": "Rendah-Sedang",
        "catalyst": "Pertumbuhan kredit nasional & dividen interim",
        "badge": "Top Dividend"
    },
    {
        "symbol": "BBCA",
        "name": "Bank Central Asia",
        "type": "Saham IDX (Perbankan Swasta)",
        "asset_class": "Stock",
        "price_approx": 9850,
        "lot_price": 985000,
        "div_yield": "~4.15%",
        "horizon": "Jangka Panjang / Core Growth",
        "thesis": "Fundamental paling kokoh di IHSG, dana murah (CASA) tebal, NPL sangat rendah, defensif terhadap krisis.",
        "risk_level": "Rendah",
        "catalyst": "Pertumbuhan laba bersih & aliran modal asing",
        "badge": "Bluechip Utama"
    },
    {
        "symbol": "TLKM",
        "name": "Telkom Indonesia",
        "type": "Saham IDX (Telekomunikasi/Infrastruktur)",
        "asset_class": "Stock",
        "price_approx": 2850,
        "lot_price": 285000,
        "div_yield": "~7.8%",
        "horizon": "Menengah - Panjang",
        "thesis": "Transformasi bisnis B2B, konsolidasi data center, dan dividen yield konsisten menarik.",
        "risk_level": "Rendah-Sedang",
        "catalyst": "Restrukturisasi FiberCo (TIF) & pertumbuhan data center",
        "badge": "Value & Yield"
    },
    {
        "symbol": "ASII",
        "name": "Astra International",
        "type": "Saham IDX (Konglomerasi)",
        "asset_class": "Stock",
        "price_approx": 5050,
        "lot_price": 505000,
        "div_yield": "~6.5%",
        "horizon": "Jangka Panjang / Siklikal",
        "thesis": "Konglomerasi terdiversifikasi (otomotif, alat berat, agribisnis, fintech), valuasi menarik & dividen rutin.",
        "risk_level": "Sedang",
        "catalyst": "Pemulihan daya beli & penetrasi kendaraan hybrid/EV",
        "badge": "Diversified"
    }
]

def fetch_crypto_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=solana,bitcoin,ethereum&vs_currencies=usd,idr&include_24hr_change=true"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read().decode())
    except Exception:
        return {}

class DashboardHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/data":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            data = {}
            if os.path.exists(DATA_FILE):
                try:
                    with open(DATA_FILE, "r") as f:
                        data = json.load(f)
                except Exception:
                    data = {}
            
            crypto_quotes = fetch_crypto_prices()
            data["recommended_instruments"] = RECOMMENDED_INSTRUMENTS
            data["crypto_quotes"] = crypto_quotes
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        html = """<!DOCTYPE html>
<html lang="id" class="h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Autonomous Dual-Bucket Sentinel & Multi-Asset Intelligence</title>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Sora"', 'system-ui', 'sans-serif'],
            mono: ['"IBM Plex Mono"', 'ui-monospace', 'monospace'],
          },
          colors: {
            surface: {
              DEFAULT: '#090d16',
              raised: '#0f1626',
              overlay: '#17223b',
              border: '#1f2e4d',
              muted: '#94a3b8'
            },
            sol: '#14F195',
            usdc: '#2775CA'
          }
        }
      }
    }
  </script>
  <style>
    ::selection { background: #14F195; color: #090d16; }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #090d16; }
    ::-webkit-scrollbar-thumb { background: #1f2e4d; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #2775CA; }
    .tabular-numbers { font-variant-numeric: tabular-nums; }

    :focus-visible {
      outline: 2px solid #14F195;
      outline-offset: 2px;
    }

    @keyframes dataPulse {
      0% { background-color: rgba(20, 241, 149, 0.25); }
      100% { background-color: transparent; }
    }
    .flash-update {
      animation: dataPulse 800ms cubic-bezier(0.16, 1, 0.3, 1);
    }
    @media (prefers-reduced-motion: reduce) {
      * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
    }
  </style>
</head>
<body class="bg-surface text-slate-100 min-h-full font-sans antialiased flex flex-col">
  <!-- Connection Status Banner -->
  <div id="conn-banner" class="hidden bg-rose-950/90 border-b border-rose-500/30 px-4 py-2 text-xs text-rose-200 flex items-center justify-between z-40">
    <div class="flex items-center gap-2">
      <span class="w-2 h-2 rounded-full bg-rose-400 animate-ping"></span>
      <span id="conn-banner-msg">Gagal menghubungkan ke backend RPC. Mencoba sinkronisasi ulang...</span>
    </div>
    <button onclick="refreshData(true)" class="px-2 py-0.5 rounded bg-rose-900 border border-rose-700 text-white font-medium hover:bg-rose-800 transition" aria-label="Coba hubungkan kembali">
      Coba Lagi
    </button>
  </div>

  <!-- Top Navigation Bar -->
  <header class="border-b border-surface-border bg-surface-raised/80 backdrop-blur-md sticky top-0 z-30" role="banner">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded-lg bg-surface-overlay border border-surface-border flex items-center justify-center text-emerald-400 font-bold font-mono text-sm shadow-sm" aria-label="Alokasi 50/50 Dual Bucket">
          50/50
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-sm font-semibold tracking-tight text-white">Dual-Bucket Sentinel Node</h1>
            <span class="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-mono font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">50% SCALPER + 50% SWING</span>
          </div>
          <p id="wallet-addr" class="text-[11px] font-mono text-slate-300 truncate max-w-xs sm:max-w-md">Menghubungkan...</p>
        </div>
      </div>

      <div class="flex items-center gap-4 text-right">
        <div class="hidden sm:block">
          <div class="text-[10px] uppercase font-semibold tracking-wider text-slate-400">Cadence Cron 15m</div>
          <div id="last-updated" class="text-xs font-mono text-slate-200 tabular-numbers" aria-live="polite">--:--:--</div>
        </div>
        <button id="btn-manual-refresh" onclick="refreshData(true)" class="p-2 text-slate-300 hover:text-white rounded-lg bg-surface-overlay border border-surface-border transition hover:border-slate-500 focus:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400" aria-label="Segarkan Data Real-time (Shortcut: R)" title="Segarkan Data (Tekan 'R')">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
        </button>
      </div>
    </div>
  </header>

  <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8" role="main">
    <!-- Primary Financial Ledger Metric Strip -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" role="region" aria-label="Ringkasan Portofolio On-Chain">
      <!-- Total Value (IDR) -->
      <div class="bg-surface-raised border border-surface-border rounded-xl p-5 relative overflow-hidden flex flex-col justify-between shadow-sm">
        <div class="flex justify-between items-start">
          <span class="text-xs font-medium uppercase tracking-wider text-slate-300">Total Saldo Dompet</span>
          <span id="pnl-status" class="text-[10px] font-mono font-medium px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">ON-CHAIN</span>
        </div>
        <div class="my-3">
          <div id="total-val-idr" class="text-3xl font-bold tracking-tight text-white font-sans tabular-numbers" aria-live="polite">Rp 0</div>
          <div id="total-val-usd" class="text-xs font-mono text-slate-300 mt-1 tabular-numbers">≈ $0.00 USD</div>
        </div>
        <div class="text-[11px] text-slate-300 border-t border-surface-border/60 pt-2 flex justify-between">
          <span>Dompet Aktif</span>
          <span class="text-slate-200">Solana Network</span>
        </div>
      </div>

      <!-- Real SOL Balance -->
      <div class="bg-surface-raised border border-surface-border rounded-xl p-5 flex flex-col justify-between shadow-sm">
        <div class="flex justify-between items-start">
          <span class="text-xs font-medium uppercase tracking-wider text-slate-300">Posisi Aset SOL</span>
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" aria-hidden="true"></span>
        </div>
        <div class="my-3">
          <div id="sol-bal" class="text-2xl font-bold text-slate-100 font-mono tabular-numbers" aria-live="polite">0.000000 SOL</div>
          <div id="sol-val-idr" class="text-xs font-sans text-emerald-400 mt-1 font-medium tabular-numbers">≈ Rp 0</div>
        </div>
        <div class="text-[11px] text-slate-300 border-t border-surface-border/60 pt-2 flex justify-between font-mono">
          <span>SPOT</span>
          <span id="sol-val-usd" class="text-slate-200">$0.00</span>
        </div>
      </div>

      <!-- Real USDC Liquidity -->
      <div class="bg-surface-raised border border-surface-border rounded-xl p-5 flex flex-col justify-between shadow-sm">
        <div class="flex justify-between items-start">
          <span class="text-xs font-medium uppercase tracking-wider text-slate-300">Kas USDC (Ready)</span>
          <span class="text-[10px] font-mono text-cyan-400" title="Solana Program Library Token">SPL</span>
        </div>
        <div class="my-3">
          <div id="usdc-val-idr" class="text-2xl font-bold text-slate-100 font-sans tabular-numbers" aria-live="polite">Rp 0</div>
          <div id="usdc-bal" class="text-xs font-mono text-cyan-400 mt-1 tabular-numbers">$0.0000 USDC</div>
        </div>
        <div class="text-[11px] text-slate-300 border-t border-surface-border/60 pt-2 flex justify-between">
          <span>Cadangan Swap</span>
          <span class="text-slate-200 font-mono">Stablecoin</span>
        </div>
      </div>

      <!-- Current Oracle & Pattern -->
      <div class="bg-surface-raised border border-surface-border rounded-xl p-5 flex flex-col justify-between shadow-sm">
        <div class="flex justify-between items-start">
          <span class="text-xs font-medium uppercase tracking-wider text-slate-300">Pola Pasar (15m)</span>
          <span id="pattern-badge" class="text-[10px] font-mono uppercase px-1.5 py-0.5 rounded bg-surface-overlay text-amber-300 border border-surface-border">SCANNING</span>
        </div>
        <div class="my-3">
          <div id="sol-price-idr" class="text-xl font-bold text-white font-mono tabular-numbers" aria-live="polite">Rp 0</div>
          <div id="sol-price-usd" class="text-xs font-mono text-slate-300 mt-1 tabular-numbers">$0.00 / SOL</div>
        </div>
        <div class="text-[11px] text-slate-300 border-t border-surface-border/60 pt-2 flex justify-between">
          <span>Sentimen AI</span>
          <span id="sentiment-score-text" class="text-emerald-400 font-medium">NEUTRAL (0)</span>
        </div>
      </div>
    </div>

    <!-- Dual-Bucket Strategy Split Showcase -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4" role="region" aria-label="Visualisasi Strategi Dual-Bucket">
      <!-- Bucket A (Daily Scalper) -->
      <div class="bg-surface-raised border border-emerald-500/30 rounded-xl p-5 relative overflow-hidden space-y-3 shadow-sm">
        <div class="flex justify-between items-center">
          <div class="flex items-center gap-2">
            <span class="p-1 rounded bg-emerald-500/10 text-emerald-400 text-xs font-bold font-mono border border-emerald-500/20">50%</span>
            <h2 class="text-sm font-bold text-white tracking-tight">Bucket A: Daily Scalper Machine</h2>
          </div>
          <span class="px-2 py-0.5 rounded text-[10px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">TARGET +1.0%/HARI + REST</span>
        </div>
        <div class="grid grid-cols-2 gap-2 text-xs py-2 border-y border-surface-border/60">
          <div>
            <span class="text-slate-400 text-[11px]">Alokasi Aset (50%):</span>
            <div id="bucket-a-val" class="font-mono text-white font-semibold mt-0.5">Rp 0 (0.000000 SOL)</div>
          </div>
          <div>
            <span class="text-slate-400 text-[11px]">Status Operasi:</span>
            <div id="bucket-a-status" class="font-mono text-emerald-400 font-semibold mt-0.5">SCALP_MONITOR</div>
          </div>
        </div>
        <p class="text-xs text-slate-300 leading-relaxed">
          Mekanisme putar modal cepat harian. Menangkap titik support/rebound dan mengunci profit begitu target +1% tercapai, lalu otomatis istirahat (REST) sampai hari berikutnya.
        </p>
      </div>

      <!-- Bucket B (Swing Runner) -->
      <div class="bg-surface-raised border border-cyan-500/30 rounded-xl p-5 relative overflow-hidden space-y-3 shadow-sm">
        <div class="flex justify-between items-center">
          <div class="flex items-center gap-2">
            <span class="p-1 rounded bg-cyan-500/10 text-cyan-400 text-xs font-bold font-mono border border-cyan-500/20">50%</span>
            <h2 class="text-sm font-bold text-white tracking-tight">Bucket B: Trend Swing Runner</h2>
          </div>
          <span class="px-2 py-0.5 rounded text-[10px] font-mono bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">TRAILING +10-50%</span>
        </div>
        <div class="grid grid-cols-2 gap-2 text-xs py-2 border-y border-surface-border/60">
          <div>
            <span class="text-slate-400 text-[11px]">Alokasi Aset (50%):</span>
            <div id="bucket-b-val" class="font-mono text-white font-semibold mt-0.5">Rp 0 (0.000000 SOL)</div>
          </div>
          <div>
            <span class="text-slate-400 text-[11px]">Status Operasi:</span>
            <div id="bucket-b-status" class="font-mono text-cyan-400 font-semibold mt-0.5">SWING_HOLD</div>
          </div>
        </div>
        <p class="text-xs text-slate-300 leading-relaxed">
          Mekanisme swing hold untuk menangkap bull run besar tanpa terganggu noise harian. Menggunakan trailing stop untuk melindungi capital gain besar.
        </p>
      </div>
    </div>

    <!-- Dual Historical Data Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6" role="region" aria-label="Grafik Historis Portofolio">
      <div class="bg-surface-raised border border-surface-border rounded-xl p-5 space-y-4 shadow-sm">
        <div class="flex items-center justify-between">
          <h2 class="text-sm font-semibold text-white tracking-tight">Tren Total Portofolio (IDR)</h2>
          <span class="text-[11px] font-mono text-slate-300">Resolusi Interval 15m</span>
        </div>
        <div class="h-60 w-full relative">
          <canvas id="assetChart" aria-label="Grafik Garis Tren Total Portofolio dalam IDR" role="img"></canvas>
        </div>
      </div>

      <div class="bg-surface-raised border border-surface-border rounded-xl p-5 space-y-4 shadow-sm">
        <div class="flex items-center justify-between">
          <h2 class="text-sm font-semibold text-white tracking-tight">Pergerakan Kurs SOL / IDR</h2>
          <span class="text-[11px] font-mono text-slate-300">Live Price Feed</span>
        </div>
        <div class="h-60 w-full relative">
          <canvas id="priceChart" aria-label="Grafik Garis Harga Pasar SOL IDR Real-time" role="img"></canvas>
        </div>
      </div>
    </div>

    <!-- Recommended Instruments & Stocks Intelligence Strip -->
    <div class="bg-surface-raised border border-surface-border rounded-xl shadow-lg overflow-hidden space-y-4 p-6" role="region" aria-label="Daftar Pantau Multi-Aset">
      <div class="flex flex-col sm:flex-row justify-between sm:items-center gap-2 pb-4 border-b border-surface-border">
        <div>
          <div class="flex items-center gap-2">
            <h2 class="text-sm font-semibold text-white tracking-tight">Instrumen & Saham Rekomendasi (Intelligence Watchlist)</h2>
            <span class="px-2 py-0.5 rounded text-[10px] font-mono bg-blue-500/10 text-blue-400 border border-blue-500/20">RESEARCH BACKED</span>
          </div>
          <p class="text-xs text-slate-300 mt-0.5">Kombinasi aset kripto terpilih & saham fundamental kuat (IHSG) untuk diversifikasi</p>
        </div>
        <div class="flex items-center gap-2 text-xs font-mono">
          <span class="px-2 py-1 rounded bg-surface-overlay text-emerald-400 border border-surface-border">Crypto High-Beta</span>
          <span class="px-2 py-1 rounded bg-surface-overlay text-cyan-400 border border-surface-border">Stock Bluechips</span>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" id="instruments-grid">
        <!-- Injected via JavaScript -->
      </div>
    </div>

    <!-- 15-Minute Autonomous Sync Journal (Audit Log) with Pagination -->
    <div class="bg-surface-raised border border-surface-border rounded-xl shadow-lg overflow-hidden" role="region" aria-label="Jurnal Audit Epoch 15 Menit">
      <div class="px-6 py-4 border-b border-surface-border flex flex-col sm:flex-row justify-between sm:items-center gap-2">
        <div>
          <h2 class="text-sm font-semibold text-white tracking-tight">Jurnal Pemantauan & Keputusan Cron (15-Min Epochs)</h2>
          <p class="text-xs text-slate-300 mt-0.5">Audit rekaman evaluasi sinyal teknikal, pola pasar, dan status on-chain</p>
        </div>
        <div class="flex items-center gap-3">
          <div class="flex items-center gap-1.5 text-xs text-slate-300">
            <label for="page-size-select">Baris:</label>
            <select id="page-size-select" onchange="changePageSize(this.value)" class="bg-surface-overlay border border-surface-border rounded px-2 py-1 text-slate-200 text-xs font-mono focus:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400" aria-label="Pilih jumlah baris log per halaman">
              <option value="5">5</option>
              <option value="10" selected>10</option>
              <option value="25">25</option>
            </select>
          </div>
          <span id="check-counter" class="text-xs font-mono bg-surface-overlay text-slate-300 px-2.5 py-1 rounded border border-surface-border self-start sm:self-auto">0 Epochs Logged</span>
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs border-collapse" aria-label="Tabel Catatan Audit Log Trading">
          <thead>
            <tr class="border-b border-surface-border bg-surface/50 text-[11px] font-semibold text-slate-300 uppercase tracking-wider">
              <th scope="col" class="py-3 px-4">Waktu (WIB)</th>
              <th scope="col" class="py-3 px-4">Aksi / Status</th>
              <th scope="col" class="py-3 px-4">Pola (15m)</th>
              <th scope="col" class="py-3 px-4 text-right">Saldo SOL</th>
              <th scope="col" class="py-3 px-4 text-right">Nilai SOL (IDR)</th>
              <th scope="col" class="py-3 px-4 text-right">Kas USDC (IDR)</th>
              <th scope="col" class="py-3 px-4 text-right">Total Aset (IDR)</th>
              <th scope="col" class="py-3 px-4">Sentimen</th>
              <th scope="col" class="py-3 px-4">Alasan & Pertimbangan</th>
            </tr>
          </thead>
          <tbody id="check-log-body" class="divide-y divide-surface-border font-mono text-slate-300">
            <tr>
              <td colspan="9" class="py-8 text-center text-slate-400 font-sans">Menghubungkan ke Solana RPC node...</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination Footer -->
      <div id="pagination-controls" class="px-6 py-3 border-t border-surface-border bg-surface-raised/50 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs">
        <div id="pagination-info" class="text-slate-300 font-mono" aria-live="polite">
          Menampilkan 0 - 0 dari 0 data
        </div>
        <div class="flex items-center gap-1.5" id="pagination-buttons">
          <button id="btn-prev" onclick="prevPage()" class="px-3 py-1.5 rounded bg-surface-overlay border border-surface-border text-slate-200 hover:text-white hover:border-slate-500 disabled:opacity-40 disabled:cursor-not-allowed font-mono transition focus-visible:ring-2 focus-visible:ring-emerald-400" aria-label="Halaman sebelumnya (Shortcut: [)">
            &larr; Prev
          </button>
          <div id="page-numbers" class="flex items-center gap-1"></div>
          <button id="btn-next" onclick="nextPage()" class="px-3 py-1.5 rounded bg-surface-overlay border border-surface-border text-slate-200 hover:text-white hover:border-slate-500 disabled:opacity-40 disabled:cursor-not-allowed font-mono transition focus-visible:ring-2 focus-visible:ring-emerald-400" aria-label="Halaman berikutnya (Shortcut: ])">
            Next &rarr;
          </button>
        </div>
      </div>
    </div>
  </main>

  <footer class="border-t border-surface-border py-4 mt-auto">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row justify-between items-center gap-2 text-xs text-slate-400">
      <div>Dual-Bucket Market Sentinel • Hermes Autonomous Agent</div>
      <div class="flex items-center gap-4 font-mono text-[11px]">
        <span>RPC: mainnet-beta</span>
        <span>MINT: EPjFWdd...yTDt1v (USDC)</span>
      </div>
    </div>
  </footer>

  <script>
    function formatIDR(num) {
      return 'Rp ' + Math.round(num || 0).toLocaleString('id-ID');
    }

    let assetChart = null;
    let priceChart = null;

    let currentPage = 1;
    let pageSize = 10;
    let allLogs = [];
    let currentSolIdr = 1850000;
    let currentUsdIdr = 16600;

    function initCharts() {
      const chartDefaults = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { intersect: false, mode: 'index' },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#0f1626',
            titleColor: '#94a3b8',
            titleFont: { family: '"IBM Plex Mono"', size: 11 },
            bodyColor: '#f8fafc',
            bodyFont: { family: '"IBM Plex Mono"', size: 12, weight: '600' },
            borderColor: '#1f2e4d',
            borderWidth: 1,
            padding: 10,
            displayColors: false,
            callbacks: {
              label: function(c) { return ' ' + formatIDR(c.parsed.y); }
            }
          }
        },
        scales: {
          x: {
            grid: { color: '#131b2e' },
            ticks: { color: '#627d98', font: { family: '"IBM Plex Mono"', size: 10 } }
          },
          y: {
            grid: { color: '#131b2e' },
            ticks: {
              color: '#627d98',
              font: { family: '"IBM Plex Mono"', size: 10 },
              callback: function(v) { return formatIDR(v); }
            }
          }
        }
      };

      const ctxAsset = document.getElementById('assetChart').getContext('2d');
      assetChart = new Chart(ctxAsset, {
        type: 'line',
        data: {
          labels: [],
          datasets: [{
            data: [],
            borderColor: '#14F195',
            backgroundColor: 'rgba(20, 241, 149, 0.08)',
            borderWidth: 2,
            fill: true,
            tension: 0.3,
            pointRadius: 3,
            pointBackgroundColor: '#14F195'
          }]
        },
        options: chartDefaults
      });

      const ctxPrice = document.getElementById('priceChart').getContext('2d');
      priceChart = new Chart(ctxPrice, {
        type: 'line',
        data: {
          labels: [],
          datasets: [{
            data: [],
            borderColor: '#38bdf8',
            backgroundColor: 'rgba(56, 189, 248, 0.08)',
            borderWidth: 2,
            fill: true,
            tension: 0.3,
            pointRadius: 3,
            pointBackgroundColor: '#38bdf8'
          }]
        },
        options: chartDefaults
      });
    }

    function renderInstruments(instruments, cryptoQuotes) {
      const container = document.getElementById('instruments-grid');
      if (!instruments || !container) return;

      container.innerHTML = instruments.map(item => {
        const isStock = item.asset_class === 'Stock';
        const typeBadgeClass = isStock ? 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20' : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
        
        let priceDisplay = '-';
        let changeDisplay = '';
        if (isStock) {
          priceDisplay = `Rp ${item.price_approx.toLocaleString('id-ID')} / lembar`;
          changeDisplay = `<span class="text-xs font-mono text-slate-400">Min 1 Lot: Rp ${item.lot_price.toLocaleString('id-ID')}</span>`;
        } else if (cryptoQuotes && item.coingecko_id && cryptoQuotes[item.coingecko_id]) {
          const q = cryptoQuotes[item.coingecko_id];
          const chg = q.usd_24h_change || 0;
          priceDisplay = `Rp ${Math.round(q.idr || 0).toLocaleString('id-ID')} ($${(q.usd || 0).toLocaleString('en-US')})`;
          changeDisplay = `<span class="text-xs font-mono ${chg >= 0 ? 'text-emerald-400' : 'text-rose-400'}">${chg >= 0 ? '+' : ''}${chg.toFixed(2)}% (24h)</span>`;
        }

        return `
          <div class="bg-surface-overlay/50 border border-surface-border rounded-xl p-4 flex flex-col justify-between hover:border-slate-600 transition">
            <div>
              <div class="flex justify-between items-start">
                <div class="flex items-center gap-2">
                  <span class="text-base font-bold font-mono text-white">${item.symbol}</span>
                  <span class="px-1.5 py-0.5 rounded text-[10px] font-mono border ${typeBadgeClass}">${item.badge}</span>
                </div>
                <span class="text-[10px] font-mono text-slate-400">${item.risk_level} Risk</span>
              </div>
              <div class="text-xs font-medium text-slate-300 mt-0.5">${item.name} • <span class="text-slate-400">${item.type}</span></div>
              
              <div class="my-3 py-2 border-y border-surface-border/50">
                <div class="text-sm font-semibold text-white font-mono">${priceDisplay}</div>
                <div class="flex justify-between items-center mt-1">
                  ${changeDisplay}
                  ${item.div_yield ? `<span class="text-xs font-mono text-amber-400 font-semibold">Yield ${item.div_yield}</span>` : ''}
                </div>
              </div>

              <p class="text-xs text-slate-300 leading-relaxed">${item.thesis}</p>
            </div>

            <div class="mt-4 pt-2 border-t border-surface-border/40 text-[11px] text-slate-400 flex justify-between items-center">
              <span>Katalis:</span>
              <span class="text-slate-200 text-right truncate max-w-[180px]">${item.catalyst}</span>
            </div>
          </div>
        `;
      }).join('');
    }

    function renderPaginatedLogs() {
      const tbody = document.getElementById('check-log-body');
      const totalItems = allLogs.length;
      
      if (totalItems === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="py-8 text-center text-slate-500 font-sans">Belum ada epoch catatan pemantauan.</td></tr>';
        document.getElementById('pagination-info').innerText = 'Menampilkan 0 dari 0 data';
        document.getElementById('btn-prev').disabled = true;
        document.getElementById('btn-next').disabled = true;
        document.getElementById('page-numbers').innerHTML = '';
        return;
      }

      const totalPages = Math.ceil(totalItems / pageSize) || 1;
      if (currentPage > totalPages) currentPage = totalPages;
      if (currentPage < 1) currentPage = 1;

      const startIndex = (currentPage - 1) * pageSize;
      const endIndex = Math.min(startIndex + pageSize, totalItems);
      const pageLogs = allLogs.slice(startIndex, endIndex);

      tbody.innerHTML = pageLogs.map(l => {
        let actClass = 'bg-surface-overlay text-slate-300 border-surface-border';
        if (l.action.includes('PROFIT') || l.action.includes('BUY')) actClass = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
        else if (l.action.includes('LOSS') || l.action.includes('SELL')) actClass = 'bg-rose-500/10 text-rose-400 border-rose-500/20';
        else if (l.action.includes('ACTIVE') || l.action.includes('SCALP')) actClass = 'bg-emerald-500/10 text-emerald-300 border-emerald-500/20';
        else if (l.action.includes('MONITOR') || l.action.includes('HOLD')) actClass = 'bg-blue-500/10 text-blue-400 border-blue-500/20';

        let patClass = 'text-slate-300 bg-surface-overlay';
        const pat = l.pattern || '-';
        if (pat.includes('SUPPORT') || pat.includes('DIP')) patClass = 'text-emerald-400 bg-emerald-500/10 border border-emerald-500/20';
        else if (pat.includes('PEAK') || pat.includes('RESISTANCE')) patClass = 'text-amber-400 bg-amber-500/10 border border-amber-500/20';
        else if (pat.includes('UP')) patClass = 'text-cyan-400 bg-cyan-500/10 border border-cyan-500/20';
        else if (pat.includes('DOWN')) patClass = 'text-rose-400 bg-rose-500/10 border border-rose-500/20';

        const logSolIdr = (l.sol_balance || 0) * (l.sol_idr || currentSolIdr);
        const logUsdcIdr = (l.usdc_balance || 0) * currentUsdIdr;
        const logTotalIdr = l.total_val_idr || (logSolIdr + logUsdcIdr);

        return `
          <tr class="hover:bg-surface-overlay/40 transition-colors">
            <td class="py-3 px-4 text-slate-400 whitespace-nowrap">${l.timestamp}</td>
            <td class="py-3 px-4"><span class="px-2 py-0.5 text-[10px] font-semibold rounded border ${actClass}">${l.action}</span></td>
            <td class="py-3 px-4"><span class="px-2 py-0.5 text-[10px] font-mono font-semibold rounded ${patClass}">${pat}</span></td>
            <td class="py-3 px-4 text-right text-slate-200">${(l.sol_balance || 0).toFixed(6)}</td>
            <td class="py-3 px-4 text-right text-slate-300">${formatIDR(logSolIdr)}</td>
            <td class="py-3 px-4 text-right text-slate-400">${formatIDR(logUsdcIdr)}</td>
            <td class="py-3 px-4 text-right text-emerald-400 font-semibold">${formatIDR(logTotalIdr)}</td>
            <td class="py-3 px-4 text-xs font-sans text-cyan-300 font-medium">${l.sentiment}</td>
            <td class="py-3 px-4 text-xs font-sans text-slate-400 max-w-xs truncate" title="${l.reason}">${l.reason}</td>
          </tr>
        `;
      }).join('');

      document.getElementById('pagination-info').innerText = `Menampilkan ${startIndex + 1} - ${endIndex} dari ${totalItems} data (Halaman ${currentPage}/${totalPages})`;
      document.getElementById('btn-prev').disabled = (currentPage === 1);
      document.getElementById('btn-next').disabled = (currentPage === totalPages);

      const pageNumbersEl = document.getElementById('page-numbers');
      let pageBtnsHtml = '';
      for (let p = 1; p <= totalPages; p++) {
        if (totalPages > 7 && Math.abs(p - currentPage) > 2 && p !== 1 && p !== totalPages) {
          if (p === 2 || p === totalPages - 1) pageBtnsHtml += `<span class="px-1 text-slate-500">...</span>`;
          continue;
        }
        const isActive = (p === currentPage);
        const btnClass = isActive ? 'bg-emerald-500 text-black font-bold border-emerald-400' : 'bg-surface-overlay text-white border-surface-border hover:border-slate-500';
        pageBtnsHtml += `<button onclick="goToPage(${p})" class="px-2.5 py-1 rounded border text-xs font-mono ${btnClass} transition">${p}</button>`;
      }
      pageNumbersEl.innerHTML = pageBtnsHtml;
    }

    function goToPage(p) {
      currentPage = p;
      renderPaginatedLogs();
    }

    function prevPage() {
      if (currentPage > 1) {
        currentPage--;
        renderPaginatedLogs();
      }
    }

    function nextPage() {
      const totalPages = Math.ceil(allLogs.length / pageSize) || 1;
      if (currentPage < totalPages) {
        currentPage++;
        renderPaginatedLogs();
      }
    }

    function changePageSize(val) {
      pageSize = parseInt(val) || 10;
      currentPage = 1;
      renderPaginatedLogs();
    }

    async function refreshData(manual = false) {
      const bannerEl = document.getElementById('conn-banner');
      const bannerMsgEl = document.getElementById('conn-banner-msg');
      try {
        const res = await fetch('/api/data');
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}: Gagal memuat data.`);
        }
        const data = await res.json();
        if (data.error) {
          throw new Error(data.error);
        }

        if (bannerEl) bannerEl.classList.add('hidden');

        document.getElementById('wallet-addr').innerText = data.wallet_address || 'Connected';

        const solBal = data.sol_balance || 0;
        const usdcBal = data.usdc_balance || 0;
        const solUsd = data.sol_usd_price || 0;
        const solIdr = data.sol_idr_price || 0;
        const usdIdr = data.usd_idr_rate || 16600;

        currentSolIdr = solIdr;
        currentUsdIdr = usdIdr;

        const solValIdr = solBal * solIdr;
        const usdcValIdr = usdcBal * usdIdr;
        const totalIdr = solValIdr + usdcValIdr;
        const totalUsd = (solBal * solUsd) + usdcBal;

        document.getElementById('total-val-idr').innerText = formatIDR(totalIdr);
        document.getElementById('total-val-usd').innerText = '≈ $' + totalUsd.toFixed(2) + ' USD';

        const totalEl = document.getElementById('total-val-idr');
        totalEl.classList.remove('flash-update');
        void totalEl.offsetWidth;
        totalEl.classList.add('flash-update');

        document.getElementById('sol-bal').innerText = solBal.toFixed(6) + ' SOL';
        document.getElementById('sol-val-idr').innerText = '≈ ' + formatIDR(solValIdr);
        document.getElementById('sol-val-usd').innerText = '$' + (solBal * solUsd).toFixed(2);

        document.getElementById('usdc-val-idr').innerText = formatIDR(usdcValIdr);
        document.getElementById('usdc-bal').innerText = '$' + usdcBal.toFixed(4) + ' USDC';

        document.getElementById('sol-price-idr').innerText = formatIDR(solIdr);
        document.getElementById('sol-price-usd').innerText = '$' + solUsd.toFixed(2) + ' / SOL';

        const sent = data.sentiment || 'NEUTRAL';
        const score = data.sentiment_score || 0;
        const pat = data.market_pattern || 'SCANNING';

        document.getElementById('pattern-badge').innerText = pat;
        document.getElementById('sentiment-score-text').innerText = `${sent} (${score >= 0 ? '+' : ''}${score})`;

        document.getElementById('last-updated').innerText = new Date().toLocaleTimeString('id-ID');

        const halfIdr = totalIdr / 2;
        const halfSol = solBal / 2;
        document.getElementById('bucket-a-val').innerText = `${formatIDR(halfIdr)} (${halfSol.toFixed(6)} SOL)`;
        document.getElementById('bucket-b-val').innerText = `${formatIDR(halfIdr)} (${halfSol.toFixed(6)} SOL)`;

        if (data.buckets) {
          document.getElementById('bucket-a-status').innerText = data.buckets.scalper_50?.state || 'SCALP_ACTIVE';
          document.getElementById('bucket-b-status').innerText = data.buckets.swing_50?.state || 'SWING_HOLD';
        }

        if (data.recommended_instruments) {
          renderInstruments(data.recommended_instruments, data.crypto_quotes);
        }

        const rawLogs = data.check_logs || [];
        allLogs = rawLogs.slice().reverse();
        document.getElementById('check-counter').innerText = allLogs.length + ' Epochs Logged';

        renderPaginatedLogs();

        if (rawLogs.length > 0 && assetChart && priceChart) {
          const chartLabels = rawLogs.map(l => {
            const parts = (l.timestamp || '').split(' ');
            return parts.length > 1 ? parts[1].substring(0, 5) : l.timestamp;
          });
          const assetPoints = rawLogs.map(l => {
            const sIdr = (l.sol_balance || 0) * (l.sol_idr || solIdr);
            const uIdr = (l.usdc_balance || 0) * usdIdr;
            return l.total_val_idr || (sIdr + uIdr);
          });
          const pricePoints = rawLogs.map(l => l.sol_idr || solIdr);

          assetChart.data.labels = chartLabels;
          assetChart.data.datasets[0].data = assetPoints;
          assetChart.update();

          priceChart.data.labels = chartLabels;
          priceChart.data.datasets[0].data = pricePoints;
          priceChart.update();
        }
      } catch (err) {
        console.error("Ledger sync error:", err);
        if (bannerEl) {
          bannerEl.classList.remove('hidden');
          if (bannerMsgEl) {
            bannerMsgEl.innerText = `Terputus dari backend: ${err.message || 'Koneksi gagal'}. Mencoba sinkronisasi otomatis...`;
          }
        }
      }
    }

    // Keyboard Shortcuts for Power Users (Alex Persona)
    document.addEventListener('keydown', function(e) {
      if (['INPUT', 'SELECT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;
      if (e.key === 'r' || e.key === 'R') {
        e.preventDefault();
        refreshData(true);
      } else if (e.key === '[' || e.key === 'ArrowLeft') {
        e.preventDefault();
        prevPage();
      } else if (e.key === ']' || e.key === 'ArrowRight') {
        e.preventDefault();
        nextPage();
      }
    });

    initCharts();
    refreshData();
    setInterval(refreshData, 10000);
  </script>
</body>
</html>
"""
        self.wfile.write(html.encode("utf-8"))

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), DashboardHandler) as httpd:
        print(f"Dual-Bucket Sentinel Node running on port {PORT}...")
        httpd.serve_forever()

if __name__ == "__main__":
    run()
