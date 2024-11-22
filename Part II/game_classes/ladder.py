from game_classes.item import Item


class Ladder(Item):
    """
    The Ladder item is used to leave this room from the attic loft.
    :param name: ladder
    :param price: 500 coins
    :param weight: 4kg
    :param attr: default, goods
    """
    def __init__(self, name="ladder", price=500, weight=4, attr="default"):
        self.name = name
        self.price = price
        self.weight = weight
        self.attr = attr




