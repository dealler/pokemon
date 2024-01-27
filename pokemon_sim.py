import poke_db
from pokemon import Pokemon, validate_name

BATTLE_START = "start"
BATTLE_STOP = "stop"


def setup_battle():
    """
    Set up the battle by selecting two Pokémons.
    """
    pokemon1 = select_pokemon("first")
    if not pokemon1:
        return None, None

    pokemon2 = select_pokemon("second")
    if not pokemon2:
        return None, None

    return pokemon1, pokemon2


def select_pokemon(order):
    """
    Prompts the user to select a Pokémon.
    """
    name, res = validate_name(order)
    if name is None:
        return None
    return Pokemon(name, res)


def battle(pokemon1, pokemon2):
    """
    Conduct the battle between two Pokémons.
    """
    battle_id = poke_db.get_new_battle_id()
    battle_state = BATTLE_START

    while battle_state == BATTLE_START:
        for attacker, defender in [(pokemon1, pokemon2), (pokemon2, pokemon1)]:
            print(f"{attacker.name}'s turn.")
            attacker.attack(battle_id, defender)

            if defender.health <= defender.hp:
                print(f"{defender.name} is defeated. {attacker.name} wins!")
                poke_db.update_winner(battle_id, attacker.name, defender.name)
                return


def battle_arena():
    """
    This function is the battlefield for two Pokémon. They battle it out
    by attacking each other. The battle continues until one Pokémon's health
    falls below its hp.
    """
    pokemon1, pokemon2 = setup_battle()
    if pokemon1 and pokemon2:
        battle(pokemon1, pokemon2)


if __name__ == "__main__":
    poke_db.setup_database()
    while True:
        print("Starting a new Battle")
        battle_arena()
