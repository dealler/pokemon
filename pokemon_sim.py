import poke_db
from pokemon import Pokemon, validate_name


def battle_areana():
    """
    This function is battlefield for two pokemons they battle it out
    by mentioning attacks and opponents and whose health gets below
    their stats hp they loose

    After executing the function you will be prompted to type the pokemon
    names and then you should enter your attack name each time until ones health
    is below their hp then battle state will be changed to stop and
    while loop stops

    """

    battle_id = poke_db.get_new_battle_id()

    name, res = validate_name("first")
    if name is None:
        return
    contender_1 = Pokemon(name, res)

    name, res = validate_name("second")
    if name is None:
        return
    contender_2 = Pokemon(name, res)

    battle_state = "start"

    while battle_state == 'start':

        print("{0} turn.".format(contender_1.name))
        contender_1.attack(battle_id, contender_2)

        print("{0} turn.".format(contender_2.name))
        contender_2.attack(battle_id, contender_1)

        if contender_1.health <= contender_1.hp:
            print("{0} is dead. {1} is winner".format(contender_1.name, contender_2.name))
            battle_state = "stop"
            poke_db.update_winner(contender_2.name, contender_1.name, battle_id)

        elif contender_2.health <= contender_2.hp:
            print("{0} is dead. {1} is winner".format(contender_2.name, contender_1.name))
            battle_state = "stop"
            poke_db.update_winner(contender_1.name, contender_2.name, battle_id)


if __name__ == "__main__":
    poke_db.setup_database()
    while True:
        print("starting new Battle")
        battle_areana()
