import json
import urllib.request
import base64
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction

SOLANA_KEYPAIR_PATH = "/home/hasbisdqi/.solana/id.json"
RPC_URL = "https://api.mainnet-beta.solana.com"
SOL_MINT = "So11111111111111111111111111111111111111112"
USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

def send_raw_tx_rpc(signed_tx_base64):
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "sendTransaction",
        "params": [
            signed_tx_base64,
            {
                "skipPreflight": False,
                "preflightCommitment": "confirmed",
                "encoding": "base64",
                "maxRetries": 3
            }
        ]
    }).encode()
    req = urllib.request.Request(RPC_URL, data=payload, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())

def execute_swap_sol_to_usdc(amount_sol=0.009):
    try:
        with open(SOLANA_KEYPAIR_PATH) as f:
            secret = json.load(f)
        keypair = Keypair.from_bytes(bytes(secret))
        wallet_pubkey = str(keypair.pubkey())
        
        amount_lamports = int(amount_sol * 1e9)
        
        print(f"1. Meminta Quote Raydium untuk swap {amount_sol} SOL ke USDC...")
        quote_url = f"https://transaction-v1.raydium.io/compute/swap-base-in?inputMint={SOL_MINT}&outputMint={USDC_MINT}&amount={amount_lamports}&slippageBps=150&txVersion=V0"
        req = urllib.request.Request(quote_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            quote_res = json.loads(r.read().decode())
            
        if not quote_res.get("success"):
            return False, f"Gagal quote Raydium: {quote_res.get('msg')}"
            
        out_usdc = int(quote_res["data"]["outputAmount"]) / 1e6
        print(f"   Estimasi USDC diterima: ${out_usdc:.4f} USDC")
        
        print(f"2. Membuat On-Chain Transaction Payload...")
        tx_url = "https://transaction-v1.raydium.io/transaction/swap-base-in"
        payload = json.dumps({
            "computeUnitPriceMicroLamports": "50000",
            "swapResponse": quote_res,
            "txVersion": "V0",
            "wallet": wallet_pubkey,
            "wrapSol": True,
            "unwrapSol": False
        }).encode()
        
        req_tx = urllib.request.Request(tx_url, data=payload, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req_tx, timeout=15) as r:
            tx_res = json.loads(r.read().decode())
            
        if not tx_res.get("success"):
            return False, f"Gagal build transaksi: {tx_res.get('msg')}"
            
        transactions = tx_res.get("data", [])
        print(f"   Ditemukan {len(transactions)} instruksi transaksi.")
        
        signatures = []
        for idx, tx_item in enumerate(transactions):
            raw_tx_bytes = base64.b64decode(tx_item["transaction"])
            tx = VersionedTransaction.from_bytes(raw_tx_bytes)
            
            # Sign transaksi dengan private key
            signed_tx = VersionedTransaction(tx.message, [keypair])
            signed_tx_b64 = base64.b64encode(bytes(signed_tx)).decode("utf-8")
            
            print(f"3. Menandatangani & Broadcast ke Solana Mainnet #{idx+1}...")
            rpc_res = send_raw_tx_rpc(signed_tx_b64)
            
            if "error" in rpc_res:
                return False, f"RPC Broadcast Error: {json.dumps(rpc_res['error'])}"
                
            sig = rpc_res.get("result")
            print(f"   ✓ Transaksi Berhasil Terkirim! Signature: {sig}")
            signatures.append(sig)
            
        return True, f"Sukses swap {amount_sol} SOL -> ${out_usdc:.4f} USDC! Signature: {', '.join(signatures)}"
        
    except Exception as e:
        return False, f"Error eksekusi on-chain: {e}"

if __name__ == "__main__":
    success, msg = execute_swap_sol_to_usdc(0.009)
    print("\nHASIL AKHIR:", msg)
