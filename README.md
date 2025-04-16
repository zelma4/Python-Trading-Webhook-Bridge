🔧 Webhook Bridge for TradingView to Bot

This is a cloud-hosted Python bridge that listens to TradingView webhooks and sends bot messages with custom logic, including:

✅ Hedge position with 2s delay
✅ Auto exit based on buy/sell pattern detection
✅ Fully editable messages via config.json
✅ Simple setup and easy reuse for other pairs or accounts

🚀 How It Works
	1.	TradingView sends a webhook alert like {"alert": "buy"} or {"alert": "sell"}
	2.	The server receives the alert
	3.	It sends the entry message immediately (buy/sell)
	4.	Waits 2 seconds
	5.	Sends the hedge message (sell/buy)

If a special exit pattern is detected (e.g., B → B → S), the server sends:
	•	EXIT message
	•	Then after 2s → opens a hedge again (re-entry)

🧠 Pattern-Based Exit Logic

Buy-side triggers Exit:
	•	B → S → B
	•	B → B → S
	•	B → B → B → S
	•	B → B → B → B → S
	•	B → B → B → B → B

Sell-side triggers Exit:
	•	S → B → S
	•	S → S → B
	•	S → S → S → B
	•	S → S → S → S → B
	•	S → S → S → S → S

🔧 Configuration

All bot messages are editable in the config.json file:

{
  "webhook_url": "https://wtalerts.com/bot/trading_view",
  "buy_message": "ENTER-LONG_BINANCE_BTCUSDC_BOT-NAME-2 with tsl_1M_xxxxxxxx",
  "sell_message": "ENTER-SHORT_BINANCE_BTCUSDC_BOT-NAME-2 with tsl_1M_xxxxxxxx",
  "exit_message": "EXIT-ALL_BINANCE_BTCUSDC_BOT-NAME-2 with tsl_1M_xxxxxxxx"
}

💡 To use with a different coin or account, just copy the project folder, change config.json, and restart the server.

⚙️ Run Locally
	1.	Install dependencies:

pip install fastapi httpx uvicorn

	2.	Start the server:

uvicorn main:app --reload --port 8000

	3.	Test via Postman or TradingView:

{ "alert": "buy" }

☁️ Deployment (Railway/Render)
	1.	Push this project to a GitHub repo
	2.	Go to https://railway.app or https://render.com
	3.	Connect your repo
	4.	Use command:

uvicorn main:app --host 0.0.0.0 --port $PORT

	5.	Get the final webhook URL like:

https://your-app.up.railway.app/webhook

✅ You’re Done!

Just use this URL in your TradingView alerts and it will handle hedge, exit, and re-entry for you automatically!