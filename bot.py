import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    ContextTypes,
    CommandHandler
)

from config import BOT_TOKEN, OWNER_ID, COINGECKO_BASE_URL
from database import add_user, is_premium
from keyboards import main_menu, upgrade_menu


# ---------------------- START COMMAND ----------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    add_user(user_id)  # automatically adds new users

    premium = is_premium(user_id, OWNER_ID)

    text = (
        "🚀 *CryptoPulse Live*\n\n"
        "Real-time crypto prices and stats.\n"
        "Select an option below 👇"
    )

    await update.message.reply_text(
        text,
        reply_markup=main_menu(premium),
        parse_mode="Markdown"
    )


# ---------------------- BUTTON HANDLER ----------------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    premium = is_premium(user_id, OWNER_ID)

    # ----- Live Prices -----
    if query.data == "prices":
        try:
            response = requests.get(
                f"{COINGECKO_BASE_URL}/simple/price",
                params={"ids": "bitcoin,ethereum", "vs_currencies": "usd"}
            ).json()

            text = (
                f"💰 *Live Prices*\n\n"
                f"BTC: ${response['bitcoin']['usd']}\n"
                f"ETH: ${response['ethereum']['usd']}"
            )
        except:
            text = "❌ Failed to fetch prices. Try again."

        await query.edit_message_text(
            text,
            reply_markup=main_menu(premium),
            parse_mode="Markdown"
        )

    # ----- Top Gainers -----
    elif query.data == "gainers":
        await query.edit_message_text(
            "🚀 *Top Gainers*\nFeature coming soon (powered by CoinGecko)",
            reply_markup=main_menu(premium),
            parse_mode="Markdown"
        )

    # ----- Gas Fees -----
    elif query.data == "gas":
        await query.edit_message_text(
            "⛽ *Gas Fees*\nFeature coming soon",
            reply_markup=main_menu(premium),
            parse_mode="Markdown"
        )

    # ----- Upgrade menu -----
    elif query.data == "upgrade":
        await query.edit_message_text(
            "⭐ *Upgrade to Premium*\nChoose a plan:",
            reply_markup=upgrade_menu(),
            parse_mode="Markdown"
        )

    # ----- Back button -----
    elif query.data == "back":
        await query.edit_message_text(
            "🚀 *CryptoPulse Live*\nSelect an option below 👇",
            reply_markup=main_menu(premium),
            parse_mode="Markdown"
        )


# ---------------------- MAIN FUNCTION ----------------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Command /start
    app.add_handler(CommandHandler("start", start))

    # All button clicks
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🚀 Bot is running...")
    app.run_polling()


# ---------------------- RUN BOT ----------------------
if __name__ == "__main__":
    main()
