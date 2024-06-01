"""
A client to connect with db and handle orders
"""

from typing import List

import redis


class OrderHandler:
    """
    Connect with Redis DB and handle orders per conversation and per user
    """

    def __init__(self, client: redis.Redis):
        """
        Initialize a redis client with a Redis client.
        """
        self.redis_client = client

    def start_collection(self, conversation_id: id) -> None:
        """
        Start order collection for a conversation.

        Parameters
        ----------
        conversation_id : int
            The unique identifier for the conversation.

        Returns
        -------
        None
        """
        self.redis_client.set(f"conversation:{conversation_id}:is_collecting", "True")

    def cancel_collection(self, conversation_id: int) -> None:
        """
        Cancel order collection for a conversation.

        Parameters
        ----------
        conversation_id : int
            The unique identifier for the conversation.

        Returns
        -------
        None
        """
        self.redis_client.set(f"conversation:{conversation_id}:is_collecting", "False")

    def is_collecting(self, conversation_id: int) -> bool:
        """
        Check if order collection is in progress for a conversation.

        Parameters
        ----------
        conversation_id : int
            The unique identifier for the conversation.

        Returns
        -------
        bool
            True if order collection is in progress, False otherwise.
        """
        result = self.redis_client.get(f"conversation:{conversation_id}:is_collecting")
        return result == b"True"

    def add_order(self, conversation_id: int, username: str, order: str) -> None:
        """
        Add an order to the user's order list within a conversation.

        Parameters
        ----------
        conversation_id : str
            The unique identifier for the conversation.
        username : str
            The unique identifier for the user.
        order : str
            The order to be added.

        Returns
        -------
        None
        """
        if self.is_collecting(conversation_id):
            self.redis_client.rpush(f"conversation:{conversation_id}:user:{username}:orders", order)

    def get_orders_by_key(self, orders_key: str) -> List[str]:
        """
        Retrieve all records for given order_key

        Parameters
        ----------
        orders_key : str
            The unique identifier for the orders.

        Returns
        -------
        List[str]
            A list of orders for the conversation or the specific user within the conversation.
        """
        orders = self.redis_client.lrange(orders_key, 0, -1)
        return [order.decode('utf-8') for order in orders]

    def get_user_orders(self, conversation_id: int, username: str) -> List[str]:
        """
        Retrieve orders for a specific user within the conversation.

        Parameters
        ----------
        conversation_id : str
            The unique identifier for the conversation.
        username : str
            The unique identifier for the user.

        Returns
        -------
        List[str]
            A list of orders for the conversation or the specific user within the conversation.
        """
        order_key = f"conversation:{conversation_id}:user:{username}:orders"
        return self.get_orders_by_key(orders_key=order_key)

    def get_all_orders(self, conversation_id: int) -> List[str]:
        """
        Retrieve all orders for a conversation for all users

        Parameters
        ----------
        conversation_id : str
            The unique identifier for the conversation.

        Returns
        -------
        List[str]
            A list of orders for the conversation or the specific user within the conversation.
        """
        user_keys = self.redis_client.keys(f"conversation:{conversation_id}:user:*:orders")
        all_orders = []
        for order_key in user_keys:
            all_orders.extend(self.get_orders_by_key(orders_key=order_key))
        return all_orders

    def clear_user_orders(self, conversation_id: int, username: str) -> None:
        """
        CLear all orders for a given user. Helpful when user changed their mind and doesn't want to order anymore.

        Parameters
        ----------
        conversation_id : int
            The conversation id to construct the order key
        username : str
            User id to cosntruct the key
        """
        orders_key = f"conversation:{conversation_id}:user:{username}:orders"
        self.redis_client.delete(orders_key)

    def clear_orders(self, conversation_id: int) -> None:
        """
        Clear all orders for a conversation

        Parameters
        ----------
        conversation_id : id
            The unique identifier for the conversation.
        """
        user_keys = self.redis_client.keys(f"conversation:{conversation_id}:user:*:orders")
        for key in user_keys:
            self.redis_client.delete(key)


# Example usage
if __name__ == "__main__":
    # TODO move this part to tests
    manager = OrderHandler()
    conversation_id = "conv12345"
    user_id1 = "user1"
    user_id2 = "user2"

    # Start order collection for the conversation
    manager.start_collection(conversation_id)

    # Add orders for different users in the same conversation
    manager.add_order(conversation_id, user_id1, "order1_user1")
    manager.add_order(conversation_id, user_id1, "order2_user1")
    manager.add_order(conversation_id, user_id2, "order1_user2")

    # Retrieve orders for the entire conversation
    print("All orders:",
          manager.get_all_orders(conversation_id))  # Output: ["order1_user1", "order2_user1", "order1_user2"]

    # Retrieve orders for a specific user within the conversation
    print("Orders for user1:",
          manager.get_user_orders(conversation_id, user_id1))  # Output: ["order1_user1", "order2_user1"]
    print("Orders for user2:", manager.get_user_orders(conversation_id, user_id2))  # Output: ["order1_user2"]

    # Clear all orders for a specific user
    manager.clear_user_orders(conversation_id, user_id1)
    print("Orders for user1 after clearing:", manager.get_user_orders(conversation_id, user_id1))  # Output: []
    print("All orders after clearing user1:", manager.get_all_orders(conversation_id))  # Output: ['order1_user2']

    # Clear all orders for the entire conversation
    manager.clear_orders(conversation_id)
    print("All orders after clearing:", manager.get_all_orders(conversation_id))  # Output: []

    # Cancel order collection for the conversation
    manager.cancel_collection(conversation_id)
