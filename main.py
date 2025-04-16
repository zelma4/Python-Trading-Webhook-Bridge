import json
from fastapi import FastAPI, Request
import asyncio, httpx
from signal_manager import SignalManager

# === LOAD CONFIG ON START ===
with open("config.json") as f:
    config = json.load(f)

BUY_MSG = config["buy_message"]
SELL_MSG = config["sell_message"]
EXIT_MSG = config["exit_message"]
WEBHOOK_URL = config["webhook_url"]

# === APP SETUP ===
app = FastAPI()
manager = SignalManager()

async def send_to_bot(message: str):
    async with httpx.AsyncClient() as client:
        await client.post(WEBHOOK_URL, data={"message": message})
        print(f"[BOT]: {message}")

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    alert = data.get("alert")

    if alert not in ["buy", "sell"]:
        return {"error": "Invalid alert type"}

    signal = 'B' if alert == "buy" else 'S'
    manager.add(signal)

    exit_type = manager.check_exit_pattern()

    if exit_type == 'EXIT_BUY':
        await send_to_bot(EXIT_MSG)
        await asyncio.sleep(2)
        await send_to_bot(SELL_MSG)
    elif exit_type == 'EXIT_SELL':
        await send_to_bot(EXIT_MSG)
        await asyncio.sleep(2)
        await send_to_bot(BUY_MSG)
    else:
        await send_to_bot(BUY_MSG if signal == 'B' else SELL_MSG)
        await asyncio.sleep(2)
        await send_to_bot(SELL_MSG if signal == 'B' else BUY_MSG)

    return {"status": "ok"}