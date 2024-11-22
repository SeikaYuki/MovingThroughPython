
class Player:
    """
    This class represents the player, including their inventory and ability to interact with the game world.

    :param name: The name of the player.
    :param backpack: List of items the player is carrying.
    """

    def __init__(self, name, backpack=[]):
        self.name = name
        self.backpack = backpack
        self.max_weight = 10  # Max weight the player can carry

    def add_to_inventory(self, item):
        """
        Adds an item to the player's inventory if it does not exceed the weight limit.

        :param item: The item to be added.
        """
        total_weight = sum(i.weight for i in self.backpack)
        if total_weight + item.weight <= self.max_weight:
            # pick up coins
            print("type(item).__name__: ", type(item).__name__)
            if type(item).__name__ == "Coin":
                print("Counting coins:")
                for i in self.backpack:
                    if type(i).__name__ == "Coin":
                        i.price += item.price
                        i.weight += item.weight
                        print(f"{i.price} coins ({item.weight} kg)")
                        item.price = 0
                        item.weight = 0
                        break
                print(f"{item.price} coins has been added to your inventory.")

            # other items
            elif item.attr=="default":
                self.backpack.append(item)
                print(f"{item.name} has been added to your inventory.")
            else:
                print(f"Unpickable item.")
        else:
            print("Your backpack is too full!")

    def drop_from_inventory(self,item):
        """
        Drop an item from the player's inventory if it's unneeded.
        :param item: Item to be dropped
        """

        if self.backpack:
            hasItem = False
            for i in self.backpack:
                if i.name == item:
                    hasItem = True
                    self.backpack.remove(i)
                    print(f"{item} has been dropped.")
                    break
                if not hasItem:
                    print(f"{item} not found in your inventory.")
        else:
            print(f"Your inventory is empty!")



    def show_inventory(self):
        """
        Displays all items in the player's inventory.
        """
        if self.backpack:
            print("You are carrying:")
            for item in self.backpack:
                if not item.name=="coins":
                    print(f"- {item.name} ({item.weight}kg)")
                else:
                    print(f"- {item.price} {item.name} ({item.weight}kg)")
        else:
            print("Your backpack is empty.")

    def has_item(self, item_name):
        """
        Checks if the player has a specific item in their inventory.

        :param item_name: The name of the item to check.
        :return: True if the item is in the inventory, else False.
        """
        return any(item.name.lower() == item_name.lower() for item in self.backpack)
