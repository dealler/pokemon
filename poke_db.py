import sqlite3


def setup_database():
    conn = sqlite3.connect('pokemon_battles.db')
    c = conn.cursor()

    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS battles
                 (id INTEGER PRIMARY KEY, winner TEXT, loser TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS battle_events
                 (battle_id INTEGER, attacker TEXT, defender TEXT, action TEXT, damage_points REAL, defender_hp REAL,
                  FOREIGN KEY (battle_id) REFERENCES battles (id))''')

    conn.commit()
    conn.close()


def get_new_battle_id():
    conn = sqlite3.connect('pokemon_battles.db')
    c = conn.cursor()

    c.execute("INSERT INTO battles (winner, loser) VALUES (?, ?)", ('TBD', 'TBD'))
    lastrowid = c.lastrowid

    conn.commit()
    conn.close()

    return lastrowid


def add_attack(battle_id, attacker_name, defender_name, attack_name, damage, defender_health):
    conn = sqlite3.connect('pokemon_battles.db')
    c = conn.cursor()

    c.execute("INSERT INTO battle_events (battle_id, attacker, defender, action, damage_points, defender_hp) "
              "VALUES (?, ?, ?, ?, ?, ?)",
              (battle_id, attacker_name, defender_name, attack_name, damage, defender_health))

    conn.commit()
    conn.close()


def update_winner(battle_id, winner_name, loser_name):
    conn = sqlite3.connect('pokemon_battles.db')
    c = conn.cursor()

    c.execute("UPDATE battles SET winner = ?, loser = ? WHERE id = ?",
              (winner_name, loser_name, battle_id))

    conn.commit()
    conn.close()
