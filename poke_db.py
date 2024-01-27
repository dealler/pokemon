import sqlite3
import logging

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

DATABASE_NAME = 'pokemon_battles.db'


def create_connection():
    """Create and return a database connection."""
    try:
        return sqlite3.connect(DATABASE_NAME)
    except sqlite3.Error as e:
        logging.error(f"Database connection error: {e}")
        raise


def setup_database():
    """Set up the database by creating necessary tables."""
    try:
        with create_connection() as conn:
            c = conn.cursor()

            c.execute('''CREATE TABLE IF NOT EXISTS battles
                         (id INTEGER PRIMARY KEY, winner TEXT, loser TEXT)''')
            c.execute('''CREATE TABLE IF NOT EXISTS battle_events
                         (battle_id INTEGER, attacker TEXT, defender TEXT, 
                          action TEXT, damage_points REAL, defender_hp REAL,
                          FOREIGN KEY (battle_id) REFERENCES battles (id))''')
    except sqlite3.Error as e:
        logging.error(f"Error setting up the database: {e}")


def get_new_battle_id():
    """Insert a new battle record and return its ID."""
    try:
        with create_connection() as conn:
            c = conn.cursor()
            c.execute("INSERT INTO battles (winner, loser) VALUES (?, ?)", ('TBD', 'TBD'))
            return c.lastrowid
    except sqlite3.Error as e:
        logging.error(f"Error getting new battle ID: {e}")


def add_attack(battle_id, attacker_name, defender_name, attack_name, damage, defender_health):
    """Record an attack in a battle."""
    if battle_id is None or not attacker_name or not defender_name or not attack_name or damage is None or defender_health is None:
        logging.error("Invalid parameters for add_attack")
        return

    try:
        with create_connection() as conn:
            c = conn.cursor()
            c.execute("INSERT INTO battle_events (battle_id, attacker, defender, action, damage_points, defender_hp) "
                      "VALUES (?, ?, ?, ?, ?, ?)",
                      (battle_id, attacker_name, defender_name, attack_name, damage, defender_health))
    except sqlite3.Error as e:
        logging.error(f"Error adding attack: {e}")


def update_winner(battle_id, winner_name, loser_name):
    """Update the winner and loser of a battle."""
    if not all([battle_id, winner_name, loser_name]):
        logging.error("Invalid parameters for update_winner")
        return

    try:
        with create_connection() as conn:
            c = conn.cursor()
            c.execute("UPDATE battles SET winner = ?, loser = ? WHERE id = ?",
                      (winner_name, loser_name, battle_id))
    except sqlite3.Error as e:
        logging.error(f"Error updating winner: {e}")
