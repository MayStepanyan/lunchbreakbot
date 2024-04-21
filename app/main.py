from telebot.types import Message

from app.globals import SETTINGS
from app.orders import Order, OrderCollectorBot

# Define states for the conversation flow
START, COLLECTING_ORDERS = range(2)

# Initialize bot
bot = OrderCollectorBot(SETTINGS.token)


@bot.message_handler(commands=['start'])
def start_order(message: Message) -> None:
    """Start collecting orders"""
    bot.current_orders.clear()  # Clear existing orders
    bot.reply_to(message, "It's time to place your lunch orders! Send your order(s). Type /done when finished.")
    bot.collecting = True


@bot.message_handler(commands=['done'])
def finish(message: Message) -> None:
    """Finish collecting orders"""
    aggregate_orders(message)
    bot.collecting = False


@bot.message_handler(commands=['cancel'])
def cancel(message: Message):
    """Cancel the order collection """
    bot.send_message(chat_id=message.chat.id, text="Order collection canceled. Type /start to start over")


@bot.message_handler(func=lambda message: (not message.text.startswith('/')))
def collect_order(message: Message) -> None:
    """Collect orders until /done is received"""
    if not bot.collecting:
        return

    username = message.from_user.username
    items = message.text.split("\n")
    if username not in bot.current_orders:
        bot.current_orders[username] = Order(username=username,
                                             name=message.from_user.first_name,
                                             order=items)
    else:
        bot.current_orders[username].order.extend(items)
    reply = (f"Added {','.join(items)} to {username} order.\n\n"
             f"Current order for {username}:\n {bot.current_orders[username].order_str}")
    bot.reply_to(message, reply)


@bot.message_handler(commands=["orders"])
def aggregate_orders(message: Message) -> None:
    """Summarize all orders"""
    order_summary = bot.summarize_orders()
    bot.reply_to(message, f"Today's Orders:\n {order_summary}")


if __name__ == "__main__":
    bot.polling()
