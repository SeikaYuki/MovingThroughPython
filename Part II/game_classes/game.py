import random
from unittest import TestCase

#from game_classes.game import Game
from game_classes.room import Room
from game_classes.player import Player

from game_classes.item import Item
from game_classes.devil import Devil
from game_classes.sword import Sword

from game_classes.key import Key
from game_classes.ladder import Ladder

def redSignal(signal):
    print("\033[91m"+str(signal)+"\033[0m")
def greenSignal(signal):
    print("\033[92m"+str(signal)+"\033[0m")
def cyanSignal(signal):
    print("\033[36m"+str(signal)+"\033[0m")

class Game:
    """
    This class manages the game state, including player actions, room transitions, and game logic.

    :param player: Instance of the Player class.
    :param current_room: The current room the player is in.
    :param rooms: Dictionary of rooms in the game.
    """

    def __init__(self, player,TestCase=False): #,timer
        self.player = player
        self.rooms = self.place_items_in_rooms(self.create_rooms(),TestCase=TestCase)
        self.current_room = self.rooms["R000"] #start

        #self.timer = timer


    def create_rooms(self):
        """Create the rooms in the house and define the paths"""
        # 创建房间实例
        R000 = Room("R000", "Start Room & Exchange Spot", {"up": "R100"})
        R100 = Room("R100", "Stairs", {"R101": "R101", "R102": "R102", "R103": "R103", "down": "R000", "up": "R200"})
        R101 = Room("R101", "Room 1", {"R100": "R100", "R102": "R102", "R103": "R103"})
        R102 = Room("R102", "Room 2", {"R100": "R100", "R101": "R101", "R103": "R103"})
        R103 = Room("R103", "Room 3", {"R100": "R100", "R101": "R101", "R102": "R102"})

        R200 = Room("R200", "Stairs", {"R201": "R201", "R202": "R202", "R203": "R203", "up": "R300", "down": "R100"})
        R201 = Room("R201", "Room 1", {"R200": "R200", "R202": "R202", "R203": "R203"})
        R202 = Room("R202", "Room 2", {"R200": "R200", "R201": "R201", "R203": "R203"})
        R203 = Room("R203", "Room 3", {"R200": "R200", "R201": "R201", "R202": "R202"})

        R300 = Room("R300", "Stairs to the attic loft",
                    {"R301": "R301", "R302": "R302", "R303": "R303", "up": "R400", "down": "R200"})
        R301 = Room("R301", "Room 1", {"R300": "R300", "R302": "R302", "R303": "R303"})
        R302 = Room("R302", "Room 2", {"R300": "R300", "R301": "R301", "R303": "R303"})
        R303 = Room("R303", "Room 3", {"R300": "R300", "R301": "R301", "R302": "R302", "up": "R400"})

        R400 = Room("R400", "End Room. You need to unlock and climb down here.", {"down": "R300"}, is_locked=True,
                    required_item="key")

        # 存储所有房间在rooms字典中
        rooms = {
            "R000": R000,
            "R100": R100, "R101": R101, "R102": R102, "R103": R103,
            "R200": R200, "R201": R201, "R202": R202, "R203": R203,
            "R300": R300, "R301": R301, "R302": R302, "R303": R303,
            "R400": R400
        }

        return rooms
    def place_items_in_rooms(self,rooms, TestCase=False):
        """Distribute the items randomly to the rooms"""
        # Create items for rooms
        key = Key("golden_key")
        ladder = Ladder("ladder")
        devil = Devil("devil")
        sword = Sword("sword")

        # Create the house
        for r in rooms:
            room = rooms[r]
            items = room.items
            # print(room.name, end=" ")
            if items:
                for i in items:
                    print(room.name, i.name)
        print()

        items = [Key(), Ladder(), Devil(), Sword()]
        item_rooms = random.sample(list(rooms.values())[1:], 3)  # Select 3 random rooms（except R000）
        # for ir in item_rooms:
        #     print(ir.name)
        # print()

        sword_room = None  # sword_floor = None
        devil_room = None  # devil_floor = None

        # Make sure the sword is placed lower than the devil
        while True:
            # Initialization
            for room in item_rooms:
                room.items = []

            # Random distribution
            for item in items:
                room = random.choice(item_rooms)
                room.items.append(item)

                if isinstance(item, Sword):
                    sword_room = room  # sword_floor = int(room.name[1])
                elif isinstance(item, Devil):
                    devil_room = room  # devil_floor = int(room.name[1])

            # Check if the condition is satisfied
            # if sword_floor < devil_floor:
            if sword_room and devil_room and int(sword_room.name[1]) < int(devil_room.name[1]):
                break  # jump out of the loop

        # the devil room requires sword to get in
        if devil_room:
            devil_room.is_locked = True
            devil_room.required_item = "sword"

        # Testing
        if TestCase:
            for r in rooms.values():
                if r.list_item():
                    print(r.name, r.list_item())
            print()

        return rooms

    def start(self):
        """Starts the game loop, accepting player commands."""

        signal = """You are in the Haunted House.Try to escape this 3-floor building from the attic loft with a [ladder].
The attic loft [R400] is [locked]. Remember to protect yourself with any tools available.  \n"""
        redSignal(signal)

        print("Input\033[92m [go up] \033[0mto get into the main building.")

        while True:
            # Check winner
            if self.current_room.name == "R400":
                if self.player.has_item("ladder"):
                    redSignal("You have escaped the haunted house.")
                    break
                else:
                    redSignal("Ladder unavailable. Go and find it!")

            # check action
            Choices = ["quit", "inventory", "go", "pick up", "drop", "tips"]
            Items = self.current_room.list_item()  # Check items in the room

            greenSignal(f"\nYou are in the {self.current_room.name}. ") # {self.current_room.description}
            if Items:
                print("Items: ", [i for i in self.current_room.list_item()])
            else:
                print("An empty room.")
            print("Choices: ", Choices)
            print("Directions: ", list(self.current_room.paths.keys()))
            print("Examples: pick up item; go up; go R103")
            command = input("What do you want to do? ").strip() #.lower()
            self.process_command(command)

    def process_command(self, command):
        """
        Process the player's command.
        :param command: The command entered by the player.
        """
        if command == "quit":
            cyanSignal("Game suspended.")
            cyanSignal("Thanks for your participation.")
            exit()
        elif command == "inventory":
            self.player.show_inventory()
        elif command == "tips":
            self.checkTips()
        elif command.startswith("go"):
            self.move(command)
        elif command.startswith("pick up"):
            self.pick_up_item(command)
        elif command.startswith("drop"):
            self.drop_item(command)
        else:
            redSignal("Invalid command.")
    def checkTips(self):
        """
        See the description of the current room
        """
        discription = self.current_room.get_discription()
        greenSignal("Here is: " + discription)
    def move(self, command):
        """
        Moves the player to another room based on the direction provided.

        :param command: The movement direction.
        """
        try:
            direction = command.split(" ")[1]
            # print("direction:",direction)
            # print("current_room.paths:",self.current_room.paths)
            # print("isInPaths:",direction in self.current_room.paths)

            if direction in self.current_room.paths:
                next_room = self.rooms[self.current_room.paths[direction]] #.name
                # print(next_room.name)
                if next_room.is_locked and not self.player.has_item(next_room.required_item):
                    redSignal(f"The {next_room.name} is unavailable. You need a {next_room.required_item} to enter.")
                else:
                    self.current_room = next_room
            else:
                redSignal("You can't go that way.")
        except:
            redSignal("Invalid command.")
            return
    def pick_up_item(self, command):
        """
        Picks up an item from the current room and adds it to the player's inventory.

        :param command: The pick-up command, which includes the item name.
        """
        try:
            item_name = command.split(" ")[2]
            item = self.current_room.get_item(item_name)
            if item:
                self.player.add_to_inventory(item)
                self.current_room.remove_item(item)
            else:
                print("Item not found.")
        except:
            redSignal("Invalid command.")
            return
    def drop_item(self,command):
            """
            Drop an item from the inventory.

            :param command: The drop command, which includes the item name.
            """
            try:
                item_name = command.split(" ")[1]
                self.player.drop_from_inventory(item_name)
            except:
                redSignal("Dropping failed.")
                return



def main():

    player = Player("Player 2")
    game = Game(player,TestCase=True) # TestCase=True | Show item in rooms when testing
    game.start()


if __name__ == "__main__":
    main()



