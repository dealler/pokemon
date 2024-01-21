import unittest
from unittest.mock import patch
import requests
from unittest.mock import MagicMock

from pokemon import Pokemon, validate_name


class TestPokemon(unittest.TestCase):

    def setUp(self):
        # Example response data to mock the API response
        self.mock_pokemon_data = {
            "stats": {
                "defense": 100,
                "attack": 150
            },
            "moves": ["thunderbolt", "tackle"],
            "name": "pikachu"
        }

    @patch('requests.get')
    def test_pokemon_initialization(self, mock_get):
        """Test the initialization of a Pokemon."""
        # Mock the API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.mock_pokemon_data

        # Initialize a Pokemon
        pikachu = Pokemon("pikachu", mock_get.return_value)

        self.assertEqual(pikachu.name, "pikachu")
        self.assertEqual(pikachu.health, 3000)
        self.assertIn("thunderbolt", pikachu.result['moves'])

    @patch('requests.get')
    def test_damage_by_each_move(self, mock_get):
        """Test damage calculation for each move."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"power": 50, "pp": 15}

        pikachu = Pokemon("pikachu", MagicMock())
        damage = pikachu.damage_by_each_move("thunderbolt")

        self.assertEqual(damage, 50)

    @patch('requests.get')
    def test_damage_taken(self, mock_get):
        """Test damage taken by the Pokemon."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.mock_pokemon_data

        pikachu = Pokemon("pikachu", MagicMock())
        initial_health = pikachu.health
        pikachu.damage_taken(200)

        self.assertTrue(pikachu.health < initial_health)

    def test_attack(self):
        """Test attack functionality."""
        # Assuming the attack method only uses the Pokemon's own data and doesn't make an API call
        pikachu = Pokemon("pikachu", MagicMock())
        bulbasaur = Pokemon("bulbasaur", MagicMock())

        initial_health_bulbasaur = bulbasaur.health
        pikachu.attack(None, bulbasaur)  # Assuming a mock battle_id

        self.assertTrue(bulbasaur.health < initial_health_bulbasaur)

    @patch('requests.get')
    def test_invalid_move_damage(self, mock_get):
        """Test handling of an invalid move."""
        mock_get.return_value.status_code = 404

        pikachu = Pokemon("pikachu", MagicMock())

        with self.assertRaises(NameError):
            pikachu.damage_by_each_move("invalid_move")


if __name__ == '__main__':
    unittest.main()
