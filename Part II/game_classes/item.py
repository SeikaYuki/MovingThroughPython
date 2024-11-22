class Item:
    """
    This class represents an item in the game. Items can be picked up and stored in the player's inventory.

    :param name: Name of the item.
    :param price: The price of purchasing this.
    :param weight: The weight of the item.
    :param attr: The type of the item, including "default""devil""delayer""goods"
    """

    def __init__(self, name, price, weight, attr="default"): #description,
        self.name = name
        self.price = price
        self.weight = weight
        self.attr = attr #"default""devil""delayer""goods"
