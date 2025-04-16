from fastapi import FastAPI, Request
import asyncio, json
from hedge_manager import HedgeManager
import httpx

app = FastAPI()
manager = HedgeManager()

with open("config.json") as f:
    config = json.load(f)

async def send_to_bot(message):
    async with httpx.AsyncClient() as client:
        # Replace with actual bot URL
        await client.post("https://your-bot-url", json={"message": message})

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    alert_type = data.get("alert")

    if alert_type in ["buy", "sell"]:
        manager.track_signal(alert_type)
        await send_to_bot(config[f"{alert_type}_message"])
        await asyncio.sleep(2)
        await send_to_bot(config["sell_message" if alert_type == "buy" else "buy_message"])

    elif alert_type == "exit":
        await send_to_bot(config["exit_message"])
        await asyncio.sleep(2)
        await send_to_bot(config["buy_message"])
        await asyncio.sleep(2)
        await send_to_bot(config["sell_message"])

    return {"status": "ok"}