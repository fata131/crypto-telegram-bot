from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu(is_premium: bool):
    buttons = [
        [InlineKeyboardButton("💰 Live Crypto Prices", callback_data="prices")],
        [InlineKeyboardButton("🚀 Top Gainers", callback_data="gainers")],
        [InlineKeyboardButton("⛽ Gas Fees", callback_data="gas")]
    ]

    if is_premium:
        buttons.append(
            [InlineKeyboardButton("🔔 Price Alerts (VIP)", callback_data="alerts")]
        )
    else:
        buttons.append(
            [InlineKeyboardButton("⭐ Upgrade to Premium", callback_data="upgrade")]
        )

    return InlineKeyboardMarkup(buttons)


def upgrade_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("₦1,000 — 7 Days", callback_data="pay_7")],
        [InlineKeyboardButton("₦3,000 — 30 Days", callback_data="pay_30")],
        [InlineKeyboardButton("⬅ Back", callback_data="back")]
    ])
