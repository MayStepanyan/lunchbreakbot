"""
Module for creating and handling orders
"""
from collections import Counter
from typing import Dict, List

import telebot
from pydantic import BaseModel, Field


class Order(BaseModel):
    """A single order"""
    username: str | None = Field(description="Unique username of the client")
    name: str | None = Field(description="Name of the client")
    order: List[str] = Field(description="List of ordered items")

    @property
    def order_str(self):
        """Order as a newline-separated string"""
        return "\n".join(self.order)


class OrderCollectorBot(telebot.TeleBot):
    """A bot for collecting orders from a chat"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO replace this with a proper memory/state storage
        self.collecting = False
        self.current_orders: Dict[str, Order] = {}

    def summarize_orders(self):
        """Summarize current orders collected by the bot"""
        return self._summarize_orders(orders=self.current_orders)

    @staticmethod
    def _summarize_orders(orders: Dict[str, Order]) -> str:
        """
        Return a text summary of given orders

        Summary includes ordered items per each person and the total number per item

        Parameters
        ----------
        orders: list[Order]
            a list of orders

        Returns
        -------
        summary: str
            a text summary of given orders
        """
        all_orders = [item for order in orders.values() for item in order.order]
        element_counts = Counter(all_orders)
        counter_string = "\n".join([f"{element}: {count}" for element, count in element_counts.items()])
        order_summary = "\n".join([f"{order.username}: {order.order}" for username, order in orders.items()])
        return f"{order_summary}\n\nTotal {len(all_orders)} items:\n{counter_string}"
