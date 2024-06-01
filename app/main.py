"""
Main endpoints
"""

import redis
from telebot import TeleBot
from telebot.types import Message

from app.client import OrderHandler
from app.globals import BOT_SETTINGS, CLIENT_SETTINGS
from app.orders import summarize

# Initialize bot
bot = TeleBot(**BOT_SETTINGS.model_dump())
redis_client = redis.Redis(**CLIENT_SETTINGS.model_dump())
order_manager = OrderHandler(client=redis_client)


@bot.message_handler(commands=['start'])
def start_order(message: Message) -> None:
    """Start collecting orders"""
    order_manager.start_collection(conversation_id=message.chat.id)
    # TODO move standard replies to constants
    bot.reply_to(message, "It's time to place your lunch orders! Send your order(s). Type /done when finished.")


@bot.message_handler(commands=["orders"])
def aggregate(message: Message) -> None:
    """Summarize all orders"""
    all_orders = order_manager.get_all_orders(conversation_id=message.chat.id)
    order_summary = summarize(all_orders)
    bot.reply_to(message, f"Today's Orders:\n {order_summary}")


@bot.message_handler(commands=["done"])
def done(message: Message) -> None:
    """Finish collecting orders"""
    aggregate(message=message)
    order_manager.clear_orders(conversation_id=message.chat.id)


@bot.message_handler(commands=["cancel"])
def cancel(message: Message):
    """Cancel the order collection """
    bot.send_message(chat_id=message.chat.id, text="Order collection canceled. Type /start to start over")


@bot.message_handler(func=lambda message: (not message.text.startswith('/')))
def collect_order(message: Message) -> None:
    """Collect messages as orders until /done is received"""

    if not order_manager.is_collecting(conversation_id=message.chat.id):
        return

    username = message.from_user.username or message.from_user.id
    order = message.text
    order_manager.add_order(conversation_id=message.chat.id,
                            username=username,
                            order=order)

    reply = (f"Added {order} to {username} order.\n\n"
             f"Current order for {username}:\n "f"{order_manager.get_user_orders(conversation_id=message.chat.id, username=username)}")
    bot.reply_to(message, reply)


if __name__ == "__main__":
    bot.polling()
