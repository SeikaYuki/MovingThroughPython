import unittest
from unittest.mock import patch, MagicMock

from game_classes.player import Player


class TestPlayer(unittest.TestCase):

    def setUp(self):
        """Create a player instance with an empty backpack for each test."""
        self.player = Player(name="TestPlayer")

    def test_add_to_inventory(self):
        """Test that an item is correctly added to the inventory."""
        # Mock Item class
        mock_item = MagicMock()
        mock_item.name = "Sword"
        mock_item.weight = 2
        mock_item.attr = "default"

        # Add item to inventory
        self.player.add_to_inventory(mock_item)

        # Check that the item was added
        self.assertIn(mock_item, self.player.backpack)
        self.assertEqual(len(self.player.backpack), 1)

    def test_add_item_exceeds_weight_limit(self):
        """Test that trying to add an item that exceeds the weight limit is prevented."""
        # Create an item that exceeds the weight limit
        mock_item = MagicMock()
        mock_item.name = "Heavy Armor"
        mock_item.weight = 15  # Exceeds the max weight of 10

        # Try to add the item to the inventory
        with patch("builtins.print") as mock_print:
            self.player.add_to_inventory(mock_item)
            mock_print.assert_called_with("Your backpack is too full!")

    def test_add_multiple_items(self):
        """Test that multiple items can be added within the weight limit."""
        # Add first item (weight 5)
        mock_item1 = MagicMock()
        mock_item1.name = "Sword"
        mock_item1.weight = 5
        mock_item1.attr = "default"
        self.player.add_to_inventory(mock_item1)

        # Add second item (weight 4)
        mock_item2 = MagicMock()
        mock_item2.name = "Shield"
        mock_item2.weight = 4
        mock_item2.attr = "default"
        self.player.add_to_inventory(mock_item2)

        # The total weight is 9, within the limit of 10
        self.assertEqual(len(self.player.backpack), 2)

    def test_add_coins_to_inventory(self):
        """Test that coins are correctly added to the inventory and their count is updated."""
        # Create a mock coin item
        mock_coin = MagicMock()
        mock_coin.name = "coins"
        mock_coin.price = 5
        mock_coin.weight = 0.1

        # Add coin to inventory
        self.player.add_to_inventory(mock_coin)

        # Create another coin and add it to the inventory
        mock_coin2 = MagicMock()
        mock_coin2.name = "coins"
        mock_coin2.price = 10
        mock_coin2.weight = 0.1
        self.player.add_to_inventory(mock_coin2)

        # Check if the total price of coins has increased
        self.assertEqual(mock_coin.price, 15)
        self.assertEqual(len(self.player.backpack), 1)  # Only one 'coins' item in the backpack

    def test_drop_from_inventory(self):
        """Test that an item is correctly dropped from the inventory."""
        # Add an item to the inventory
        mock_item = MagicMock()
        mock_item.name = "Sword"
        mock_item.weight = 2
        mock_item.attr = "default"
        self.player.add_to_inventory(mock_item)

        # Drop the item
        self.player.drop_from_inventory("Sword")

        # Check that the item is no longer in the backpack
        self.assertNotIn(mock_item, self.player.backpack)

    def test_drop_non_existent_item(self):
        """Test that attempting to drop an item that is not in the inventory is handled correctly."""
        # Try to drop an item that doesn't exist
        with patch("builtins.print") as mock_print:
            self.player.drop_from_inventory("NonExistentItem")
            mock_print.assert_called_with("NonExistentItem not found in your inventory.")

    def test_show_inventory(self):
        """Test that the player's inventory is displayed correctly."""
        # Add two items to the player's inventory
        mock_item1 = MagicMock()
        mock_item1.name = "Sword"
        mock_item1.weight = 2
        mock_item1.attr = "default"
        self.player.add_to_inventory(mock_item1)

        mock_item2 = MagicMock()
        mock_item2.name = "Shield"
        mock_item2.weight = 3
        mock_item2.attr = "default"
        self.player.add_to_inventory(mock_item2)

        with patch("builtins.print") as mock_print:
            self.player.show_inventory()
            mock_print.assert_any_call("You are carrying:")
            mock_print.assert_any_call("- Sword (2kg)")
            mock_print.assert_any_call("- Shield (3kg)")

    def test_has_item(self):
        """Test that the has_item method correctly checks if an item is in the inventory."""
        mock_item = MagicMock()
        mock_item.name = "Sword"
        mock_item.weight = 2
        mock_item.attr = "default"
        self.player.add_to_inventory(mock_item)

        # Check if the player has the item
        self.assertTrue(self.player.has_item("Sword"))
        self.assertFalse(self.player.has_item("Shield"))

    def test_add_to_inventory_with_default_attr(self):
        """Test that an item with 'default' attribute is added to the inventory."""
        mock_item = MagicMock()
        mock_item.name = "Sword"
        mock_item.weight = 3
        mock_item.attr = "default"

        with patch("builtins.print") as mock_print:
            self.player.add_to_inventory(mock_item)
            mock_print.assert_called_with("Sword has been added to your inventory.")

        # Verify the item is in the player's inventory
        self.assertIn(mock_item, self.player.backpack)

    def test_add_unpickable_item(self):
        """Test that an unpickable item is not added to the inventory."""
        mock_item = MagicMock()
        mock_item.name = "Mystic Orb"
        mock_item.weight = 5
        mock_item.attr = "unpickable"

        with patch("builtins.print") as mock_print:
            self.player.add_to_inventory(mock_item)
            mock_print.assert_called_with("Unpickable item.")


if __name__ == "__main__":
    unittest.main()
