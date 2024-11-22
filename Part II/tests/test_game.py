import unittest
from unittest.mock import MagicMock

# # from game_classes.item import Item
from game_classes.devil import Devil
from game_classes.game import Game
from game_classes.key import Key
from game_classes.sword import Sword


class TestGame(unittest.TestCase):

    def setUp(self):
        """
        create a entity for testing the game class
        """
        self.player = MagicMock()
        self.player.has_item.return_value = False
        self.game = Game(self.player)  # create a game entity

    def test_create_rooms(self):
        """
       test the function of create_rooms
        """
        rooms = self.game.create_rooms()

        # check if all rooms created
        self.assertIn("R000", rooms)
        self.assertIn("R400", rooms)

        # check if R400 locked
        self.assertTrue(rooms["R400"].is_locked)
        self.assertEqual(rooms["R400"].required_item, "key")

    def test_move_player(self):
        """
        test the function of moving
        """
        self.game.current_room = self.game.rooms["R100"]  # current room is R100
        self.player.has_item.return_value = True  # suppose a key existing玩家持有钥匙

        # try to move to R200 from R100
        self.game.move("go up")
        self.assertEqual(self.game.current_room.name, "R200")  # should move to R200

        # try to get in R400
        self.game.move("go up")  # R300 -> R400
        self.assertEqual(self.game.current_room.name, "R400")
        self.assertTrue(self.game.current_room.is_locked)
        self.assertEqual(self.game.current_room.required_item, "key")

        # without a key, R400 cannot be get in
        self.player.has_item.return_value = False  # the player has no key
        self.game.move("go down")  # 进入 R400
        self.assertEqual(self.game.current_room.name, "R300")  # still in R300

    def test_pick_up_item(self):
        """
        test the function of pick up things
        """
        room = self.game.rooms["R100"]
        room.items = [Key()]  # a key in the room

        self.player.has_item.return_value = False  # empty inventory
        self.game.pick_up_item("pick up key")

        # test if the key picked up successfully
        self.player.add_to_inventory.assert_called_with(Key("golden_key"))
        self.assertNotIn(Key(), room.items)  # the key in the room should be removed

    def test_drop_item(self):
        """
        test the drop function
        """
        self.player.drop_from_inventory = MagicMock()

        self.player.add_to_inventory(Key())  # the player has got a key
        self.game.drop_item("drop key")

        # 检查玩家是否成功丢弃钥匙
        self.player.drop_from_inventory.assert_called_with("key")

    def test_locked_room_without_key(self):
        """
        test whether a player can get into a locked room without a key
        """
        self.game.current_room = self.game.rooms["R300"]
        self.player.has_item.return_value = False  # the player has no key

        self.game.move("go up")  # try getting into R400

        # make sure that the player hasn't get into the locked R400
        self.assertEqual(self.game.current_room.name, "R300")

    def test_locked_room_with_key(self):
        """
        test of getting in to the locked room with a key
        """
        self.game.current_room = self.game.rooms["R300"]
        self.player.has_item.return_value = True  # the player has the key

        self.game.move("go up")  # try to get into R400

        # make sure the player get in to the locked R400
        self.assertEqual(self.game.current_room.name, "R400")

    def test_inventory(self):
        """
        test of inventory
        """
        self.game.current_room.items = [Sword()]
        self.player.has_item.return_value = False

        # the player pick up the sword
        self.game.pick_up_item("pick up sword")
        self.assertTrue(self.player.add_to_inventory.called)

        # check if the sword in the inventory
        self.player.add_to_inventory.assert_called_with(Sword("sword"))

    def test_game_end_with_ladder(self):
        """
        Test of game over when the player has a ladder
        """
        self.player.has_item.return_value = True  # the player has a ladder
        self.game.current_room = self.game.rooms["R400"]  # the player is in R400

        # test of game suspended
        self.game.move("go down")  # 进入 R300
        self.assertEqual(self.game.current_room.name, "R400")
        self.assertTrue(self.game.current_room.is_locked)
        self.assertEqual(self.game.current_room.required_item, "key")

    def test_invalid_move(self):
        """
        Test of invalid command
        """
        self.game.move("go left")  # invalid direction
        self.assertEqual(self.game.current_room.name, "R100")  # the player is still in R100

        self.game.move("go up")  # R100 -> R200
        self.assertEqual(self.game.current_room.name, "R200")  # now should be in R200


if __name__ == "__main__":
    unittest.main()
