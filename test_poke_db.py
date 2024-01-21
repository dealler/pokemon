import unittest
import sqlite3
import poke_db


class TestPokeDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the database before running tests."""
        poke_db.setup_database()

    def test_get_new_battle_id(self):
        """Test if a new battle ID is created correctly."""
        battle_id = poke_db.get_new_battle_id()
        self.assertIsInstance(battle_id, int)

    def test_add_attack(self):
        """Test adding an attack to the database."""
        battle_id = poke_db.get_new_battle_id()
        poke_db.add_attack(battle_id, 'Pikachu', 'Bulbasaur', 'Thunderbolt', 40, 250)
        # Verify if the attack was added correctly
        conn = sqlite3.connect('pokemon_battles.db')
        c = conn.cursor()
        c.execute("SELECT * FROM battle_events WHERE battle_id = ?", (battle_id,))
        attack = c.fetchone()
        conn.close()
        self.assertIsNotNone(attack)
        self.assertEqual(attack[1], 'Pikachu')
        self.assertEqual(attack[2], 'Bulbasaur')

    def test_update_winner(self):
        """Test updating the winner and loser of a battle."""
        battle_id = poke_db.get_new_battle_id()
        poke_db.update_winner(battle_id, 'Bulbasaur', 'Pikachu')
        # Verify if the winner and loser were updated correctly
        conn = sqlite3.connect('pokemon_battles.db')
        c = conn.cursor()
        c.execute("SELECT winner, loser FROM battles WHERE id = ?", (battle_id,))
        battle = c.fetchone()
        conn.close()
        self.assertIsNotNone(battle)
        self.assertEqual(battle[0], 'Bulbasaur')
        self.assertEqual(battle[1], 'Pikachu')


if __name__ == '__main__':
    unittest.main()
