import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from user_agent import generate_user_agent

gd = str(generate_user_agent())
# Function to check username availability on Instagram
def check_instagram_username(username):
    headers = {
        'Host': 'www.instagram.com',
        'content-length': '85',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101"',
        'x-ig-app-id': '936619743392459',
        # Add more headers as needed
        'user-agent': f'{gd}',
        'cookie': 'csrftoken=jzhjt4G11O37lW1aDFyFmy1K0yIEN9Qv','cookie':'mid=YtsQ1gABAAEszHB5wT9VqccwQIUL','cookie':'ig_did=227CCCC2-3675-4A04-8DA5-BA3195B46425','cookie':'ig_nrcb=1'
    }

    data = f'email=example%40gmail.com&username={username}&first_name=&opt_into_one_tap=false'

    res = requests.post('https://www.instagram.com/accounts/web_create_ajax/attempt/', headers=headers, data=data).text

    if "status" in res and "fail" in res:
        return "Username is bad"
    elif '"errors": {"username":' in res or '"code": "username_is_taken"' in res:
        return "Username is taken"
    else:
        return "Username is available"

# Telegram command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the Instagram Username Checker Bot! Send me a username to check.')

def check_username(update: Update, context: CallbackContext) -> None:
    username = context.args[0] if context.args else None

    if username:
        result = check_instagram_username(username)
        update.message.reply_text(result)
    else:
        update.message.reply_text('Please provide a username to check.')

# Set up the Telegram bot
updater = Updater(token='7088225677:AAGs7KCjxxdPeFNQM2SRXhHVHXzeOyCNssg', use_context=True)
dispatcher = updater.dispatcher

# Add command handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("check", check_username))

# Start the bot
updater.start_polling()
updater.idle()