from game_classes.item import Item


class Devil(Item):
    """
    The devil will force the player to restart and go back to the entrance without the force of a sword.
    :param name: devil
    :param price: 300 coins
    :param weight: 0 kg
    :param attr: devil
    """
    def __init__(self, name="devil", price=300, weight=0, attr="devil"):
        self.name = name
        self.price = price
        self.weight = weight
        self.attr = attr




