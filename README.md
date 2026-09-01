# Autonomous Crypto & Multi-Asset Intelligence Dashboard

Clean, dark-themed responsive dashboard for tracking Solana on-chain portfolio, 15-minute epoch audit logs, Dual-Bucket scalping/swing strategies, and multi-asset intelligence watchlist.

## Features
- **Clean Anti-AI Slop UI**: Crafted with Sora & IBM Plex Mono typography, bespoke color hierarchy, and custom scrollbars.
- **Dual Live Charts (Chart.js)**: 15-minute epoch portfolio value trend (IDR) & live SOL/IDR price feeds.
- **Dual-Bucket Strategy Visualizer**: 50% Adaptive Daily Scalper + 50% Trend Swing Runner.
- **Paginated Audit Journal**: Realtime log tracking with configurable rows (5/10/25) and client-side pagination.
- **Multi-Asset Intelligence**: Live watchlist for Top Crypto Assets (SOL, BTC, ETH) and Indonesian Bluechip Stocks (BBRI, BBCA, TLKM, ASII).

## Setup & Run

1. **Environment Variables (Optional)**:
   ```bash
   export PORT=8088
   export DATA_FILE_PATH="./crypto_trading_bot.json"
   ```

2. **Run Server**:
   ```bash
   python3 server.py
   ```
   Open `http://localhost:8088` in your browser.
