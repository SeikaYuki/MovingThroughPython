
from game_classes.room import Room
from game_classes.item import Item

import unittest
from unittest.mock import patch, MagicMock


class TestRoom(unittest.TestCase):

    def setUp(self):
        """Create a Room instance with a mock setup for each test."""
        # Mock some items
        self.room = Room(
            name="Living Room",
            description="A cozy living room with a fireplace.",
            paths={"north": "Kitchen", "east": "Bedroom"},
            items=[],  # Initially no items
            is_locked=False,
            required_item=None
        )

    def test_add_item(self):
        """Test that a valid item is correctly added to the room."""
        mock_item = MagicMock()
        mock_item.name = "Key"
        mock_item.price = 10  # Valid item with positive price
        mock_item.attr = "default"

        with patch("builtins.print") as mock_print:
            self.room.add_item(mock_item)
            mock_print.assert_called_with(f"\033[92mThe {mock_item.name} is added to the room.\033[0m")

        # Verify the item is in the room's items list
        self.assertIn(mock_item, self.room.items)

    def test_add_invalid_item(self):
        """Test that an invalid item (with price <= 0) is not added to the room."""
        mock_item = MagicMock()
        mock_item.name = "Broken Key"
        mock_item.price = 0  # Invalid item
        mock_item.attr = "default"

        with patch("builtins.print") as mock_print:
            self.room.add_item(mock_item)
            mock_print.assert_called_with(f"\033[91mThe {mock_item.name} HAVE NOT be added to the room.\033[0m")

        # Verify the item is not in the room's items list
        self.assertNotIn(mock_item, self.room.items)

    def test_list_item(self):
        """Test that the list of items in the room is returned correctly."""
        # Create and add items to the room
        mock_item1 = MagicMock()
        mock_item1.name = "Key"
        mock_item1.price = 10
        mock_item1.attr = "default"

        mock_item2 = MagicMock()
        mock_item2.name = "Map"
        mock_item2.price = 5
        mock_item2.attr = "default"

        self.room.add_item(mock_item1)
        self.room.add_item(mock_item2)

        # List items in the room
        item_names = self.room.list_item()
        self.assertIn("Key", item_names)
        self.assertIn("Map", item_names)

    def test_get_item(self):
        """Test that a specific item can be retrieved by its name."""
        # Create and add an item to the room
        mock_item = MagicMock()
        mock_item.name = "Sword"
        mock_item.price = 20
        mock_item.attr = "default"
        self.room.add_item(mock_item)

        # Retrieve the item by name
        retrieved_item = self.room.get_item("Sword")
        self.assertEqual(retrieved_item, mock_item)

    def test_get_item_not_found(self):
        """Test that if an item is not found, None is returned."""
        # Try to get an item that doesn't exist
        retrieved_item = self.room.get_item("NonExistentItem")
        self.assertIsNone(retrieved_item)

    def test_remove_item(self):
        """Test that an item can be correctly removed from the room."""
        # Create and add an item to the room
        mock_item = MagicMock()
        mock_item.name = "Key"
        mock_item.price = 10
        mock_item.attr = "default"
        self.room.add_item(mock_item)

        with patch("builtins.print") as mock_print:
            # Remove the item
            self.room.remove_item(mock_item)
            mock_print.assert_called_with(f"{mock_item.name} has been removed from the room.")

        # Verify the item is removed from the room's items list
        self.assertNotIn(mock_item, self.room.items)

    def test_remove_item_not_found(self):
        """Test that an attempt to remove an item not in the room is handled correctly."""
        # Create a mock item that's not in the room
        mock_item = MagicMock()
        mock_item.name = "Fake Item"
        mock_item.price = 0
        mock_item.attr = "default"

        with patch("builtins.print") as mock_print:
            self.room.remove_item(mock_item)
            mock_print.assert_called_with("Item not found in the room.")

    def test_remove_item_devils_item(self):
        """Test that an item marked as "devil" cannot be removed."""
        # Create a "devil" item
        mock_item = MagicMock()
        mock_item.name = "Cursed Item"
        mock_item.price = 10
        mock_item.attr = "devil"  # Special attribute, should not be removed

        self.room.add_item(mock_item)

        with patch("builtins.print") as mock_print:
            # Try to remove the "devil" item
            self.room.remove_item(mock_item)
            mock_print.assert_not_called()  # No print message expected, as it doesn't get removed

        # Verify the item is still in the room's items list
        self.assertIn(mock_item, self.room.items)

    def test_room_description(self):
        """Test that the room's description is correctly returned."""
        description = self.room.get_discription()
        self.assertEqual(description, "A cozy living room with a fireplace.")

    def test_locked_room(self):
        """Test that a locked room's access is managed correctly."""
        # Create a locked room
        locked_room = Room(
            name="Secret Room",
            description="A hidden room with treasures.",
            paths={},
            items=[],
            is_locked=True,
            required_item="Golden Key"
        )

        # Test that the room is locked
        self.assertTrue(locked_room.is_locked)
        self.assertEqual(locked_room.required_item, "Golden Key")

    def test_remove_item_non_default(self):
        """Test that a non-default item cannot be removed."""
        # Create an item with an invalid attribute (non-default)
        mock_item = MagicMock()
        mock_item.name = "NonDefault Item"
        mock_item.price = 10
        mock_item.attr = "non_default"  # Not 'default', should not be removed

        self.room.add_item(mock_item)

        with patch("builtins.print") as mock_print:
            # Try to remove this non-default item
            self.room.remove_item(mock_item)
            mock_print.assert_called_with("Item not found in the room.")

        # Verify the item is still in the room
        self.assertIn(mock_item, self.room.items)


if __name__ == "__main__":
    unittest.main()
