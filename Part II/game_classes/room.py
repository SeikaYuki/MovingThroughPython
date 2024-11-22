class Room:
    """
    This class represents a room in the game. Each room has a name, description, and connections to other rooms.

    :param name: Name of the room.
    :param description: A brief description of the room.
    :param paths: Dictionary of directions to other rooms.
    :param items: List of items present in the room.
    :param is_locked: Boolean indicating if the room is locked.
    :param required_item: The name of the item required to unlock the room.
    """

    def __init__(self, name, description, paths, items=None, is_locked=False, required_item=None):
        self.name = name
        self.description = description
        self.paths = paths  # Directions to other rooms
        self.items = items if items else []
        self.is_locked = is_locked
        self.required_item = required_item

    def get_discription(self):
        return self.description

    def add_item(self,item):
        if item.price>0:
            self.items.append(item)
            print(f"\033[92mThe {item.name} is added to the room.\033[0m")
        else:
            print(f"\033[91mThe {item.name} HAVE NOT be added to the room.\033[0m")

    def list_item(self):
        #return self.name
        return [item.name for item in self.items]  # Return a list of item names in the room

    def get_item(self, item_name):
        """
        Retrieves an item by name from the room.

        :param item_name: The name of the item to retrieve.
        :return: The item if found, otherwise None.
        """
        for item in self.items:
            if item.name.lower() == item_name.lower():
                return item
        return None

    def remove_item(self, item):
        """
        Removes an item from the room once it has been picked up by the player.

        :param item: The item to be removed from the room.
        """
        if item in self.items and item.attr=="default":
            self.items.remove(item)
            print(f"{item.name} has been removed from the room.")
        elif item.attr=="devil":
            pass
        else:
            print("Item not found in the room.")

    # def hasCoins(self):
    #     if self.items:
    #         for i in self.items:
    #             if type(i).__name__ == "Coin":
    #                 return True if i.price > 0 else False  # check if has coin & price>0
    #     return False


