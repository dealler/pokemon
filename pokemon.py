import http
import requests
from urllib.parse import urljoin
from tabulate import tabulate
import random
import poke_db
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

URL = 'https://pokeapi.co/api/v2/'
# test in local dev
# validated_names_cache = {}


def validate_name(order):
    """
    This function will check if the given pokemon name is valid or not
    from the pokemon list and returns the pokemon name if it is valid.
    It checks up to 3 times before giving up and returning None.
    """
    for attempt in range(3):
        name = input("enter {0} pokemon name:".format(order))
        # test in local dev
        # if name in validated_names_cache:
        #     return name, validated_names_cache[name]
        cached_res = redis_client.get(name)
        if cached_res:
            return name, json.loads(cached_res)
        pokemon = 'pokemon/' + str(name)
        poke_url = urljoin(URL, pokemon)
        res = requests.get(url=poke_url)

        if res.status_code == http.HTTPStatus.OK:
            # test in local dev
            # validated_names_cache[name] = res
            redis_client.set(name, json.dumps(res.json()))
            return name, res
        else:
            print("Pokemon not found. Please check the spelling and try again.")

    print("Failed to find a valid Pokemon name after 3 attempts.")
    return None, None


class Pokemon:
    """
    This class will initialise a Pokémon and will add features to it
    By using two instances of this class we can battle each other

    __str__ attribute returns table of stats
    """
    _cache = {}

    def __init__(self, name, res):
        self.health = 3000
        self.name = name
        self.result = self.get_pokemon_details(res)
        self.hp = self.result['stats']['defense'] * 10

    def __repr__(self):
        return "<Pokemon:{0}>".format(self.name)

    def __str__(self):
        stats = [[i, self.result['stats'][i]] for i in self.result['stats']]
        tab = tabulate(stats, headers=['Type', 'Value'], tablefmt='orgtbl')
        return tab

    def attack(self, battle_id, defender_name):
        """This function will give damage to other pokemon that is mentioned """

        attack_name = random.choice(self.result['moves'])
        attack_stats = self.result['stats']['attack']
        damage = self.damage_by_each_move(attack_name) * (attack_stats / 2)
        print("damage given by {0} to {1} for {2}".format(self.name, defender_name.name, damage))

        try:
            def_damage = defender_name.damage_taken(damage)

        except:
            raise KeyError("check defender name")

        poke_db.add_attack(battle_id, self.name, defender_name.name, attack_name, damage, defender_name.health)

    def damage_taken(self, damage):
        """This function will decrease the helath of the pokemon based
            on the damage given by an other pokemon.
            The damage taken will also based on the defense stat of this
            pokemon other than attack power of opponent

        """
        stat_defense = self.result['stats']['defense']

        # real damage will be reduced according to defence stat of pokemon
        real_damage = damage / (stat_defense / 10)
        self.health -= real_damage
        print("{0}'s health = {1}".format(self.name, self.health))

    def damage_by_each_move(self, move_name):
        """
            This function will fetch the damage that will be delt by the given
            attack name from the
        """

        poke_details = self.result
        if move_name in poke_details['moves']:
            print(self.move_damages(move_name))
            damage = self.move_damages(move_name)['damage']
            return int(damage) if damage is not None else 0
        else:
            raise NameError("{0} doesnt have this attack".format(self.name))

    def get_pokemon_details(self, res):
        """This function will get all the details of given pokemon """

        poke_response = res.json()
        result = {
            'abilities': [],
            'base_experience': poke_response['base_experience'],
            'height': poke_response['height'],
            'weight': poke_response['weight'],
            'forms': [],
            'moves': [],
            'types': [],
            'stats': {}

        }

        for i in poke_response['abilities']:
            result['abilities'].append(i['ability']['name'])

        for j in poke_response['moves']:
            result['moves'].append(j['move']['name'])

        for k in poke_response['types']:
            result['types'].append(k['type']['name'])

        for l in poke_response['stats']:
            result['stats'][str(l['stat']['name'])] = l['base_stat']

        for m in poke_response['forms']:
            result['forms'].append(m['name'])

        return result

    def move_damages(self, move_name):
        """
        This Function will give details of the attack moves
        """
        cache_key = f"{self.name}_{move_name}"
        # test in local dev
        # if cache_key in Pokemon._cache:
        #     return Pokemon._cache[cache_key]
        cached_output = redis_client.get(cache_key)
        if cached_output:
            return json.loads(cached_output)

        moves = 'move/' + str(move_name)
        moves_url = urljoin(URL, moves)
        try:
            moves_response = requests.get(url=moves_url).json()
        except:
            raise (ValueError("Move entered is not in the database"))
            return None

        output = {
            'name': move_name,
            'damage': moves_response['power'],
            "pp": moves_response['pp']

        }
        # test in local dev
        # Pokemon._cache[cache_key] = output
        redis_client.set(cache_key, json.dumps(output))
        return output

