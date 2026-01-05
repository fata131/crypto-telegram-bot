import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# CoinGecko does NOT need API key for our usage
COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"
