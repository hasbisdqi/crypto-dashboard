import urllib.request
import json
import xml.etree.ElementTree as ET

def fetch_multi_assets():
    url_price = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,ripple,cardano&vs_currencies=usd,idr&include_24hr_change=true'
    req = urllib.request.Request(url_price, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        price_data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode())
    except Exception as e:
        print("Price error:", e)
        return

    print("=== HARGA LIVE & PERGERAKAN 24 JAM ===")
    for coin, data in price_data.items():
        usd = data.get('usd', 0)
        idr = data.get('idr', 0)
        chg = data.get('usd_24h_change', 0)
        print(f"{coin.upper():8} : ${usd:>10,.2f} | Rp {idr:>14,.0f} | 24h: {chg:>+6.2f}%")

    print("\n=== HEADLINES & SENTIMEN BERITA TERBARU ===")
    feeds = [
        'https://cointelegraph.com/rss',
        'https://coindesk.com/arc/outboundfeeds/rss/'
    ]
    pos_kw = ['surge', 'rally', 'etf', 'gain', 'bullish', 'breakout', 'all-time high', 'ath', 'inflow', 'adoption', 'record']
    neg_kw = ['crash', 'hack', 'lawsuit', 'dump', 'bearish', 'sec', 'ban', 'exploit', 'fud', 'drop', 'fell']

    headlines = []
    score = 0
    for f in feeds:
        try:
            r = urllib.request.Request(f, headers={'User-Agent': 'Mozilla/5.0'})
            tree = ET.fromstring(urllib.request.urlopen(r, timeout=8).read())
            for it in tree.findall('.//item')[:4]:
                t = it.find('title').text or ''
                headlines.append(t)
                lt = t.lower()
                for w in pos_kw:
                    if w in lt: score += 1
                for w in neg_kw:
                    if w in lt: score -= 1
        except Exception:
            pass

    for i, h in enumerate(headlines[:5], 1):
        print(f"{i}. {h}")

    status = "NEUTRAL"
    if score >= 3: status = "STRONG_BULLISH"
    elif score >= 1: status = "BULLISH"
    elif score <= -3: status = "STRONG_BEARISH"
    elif score <= -1: status = "BEARISH"

    print(f"\nSkor Sentimen Makro: {score} ({status})")

if __name__ == "__main__":
    fetch_multi_assets()
