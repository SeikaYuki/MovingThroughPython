from game_classes.item import Item


class Key(Item):
    """
    The key is used to unlock the attic loft.
    :param name: key
    :param price: 800 coins
    :param weight: 0.1 kg
    :param attr: default, goods
    """
    def __init__(self, name="key", price=800, weight=0.1, attr="default"):
        self.name = name
        self.price = price
        self.weight = weight
        self.attr = attr




