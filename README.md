# Autonomous Crypto & Multi-Asset Intelligence Dashboard

Clean, dark-themed responsive dashboard for tracking Solana on-chain portfolio, 15-minute epoch audit logs, Dual-Bucket scalping/swing strategies, and multi-asset intelligence watchlist.

## Features
- **Clean Anti-AI Slop UI**: Crafted with Sora & IBM Plex Mono typography, bespoke color hierarchy, motion feedback micro-interactions, and custom scrollbars.
- **Dual Live Charts (Chart.js)**: 15-minute epoch portfolio value trend (IDR) & live SOL/IDR price feeds.
- **Dual-Bucket Strategy Visualizer**:
  - **Bucket A (50%)**: AI Predictive Adaptive Daily Scalper (dynamic targets > 0.45% & daily target rest locking).
  - **Bucket B (50%)**: Trend Swing Runner (trailing stop targets +5-50%).
- **Paginated Audit Journal**: Realtime log tracking with configurable rows (5/10/25) and client-side pagination.
- **Multi-Asset Intelligence**: Live watchlist for Top Crypto Assets (SOL, BTC, ETH) and Indonesian Bluechip Stocks (BBRI, BBCA, TLKM, ASII).
- **On-Chain Raydium Swap Router**: Integrated automated DEX swap execution engine (SOL ↔ USDC).

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
