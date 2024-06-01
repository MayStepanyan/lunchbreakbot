"""
Module for creating and handling orders
"""
from collections import Counter


def summarize(orders: list[str]) -> str:
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
    all_orders = orders
    element_counts = Counter(all_orders)
    counter_string = "\n".join([f"{element}: {count}" for element, count in element_counts.items()])
    return f"Total {len(all_orders)} items:\n{counter_string}"
