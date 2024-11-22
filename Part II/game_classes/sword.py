from game_classes.item import Item


class Sword(Item):
    """
    The sword is used to fight the devil, preventing the player to restart.
    :param name: sword
    :param price: 300coins
    :param weight: 5 kg
    :param attr: default, goods
    """
    def __init__(self, name="sword", price=300, weight=5, attr="default"):
        self.name = name
        self.price = price
        self.weight = weight
        self.attr = attr




