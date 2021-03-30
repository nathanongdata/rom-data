import requests


def mob_harvest(key_id):
    # key_id = 10267 (Test)
    url = 'https://www.romcodex.com/api/monster/' + str(key_id)

    result = requests.get(url)
    result_json = result.json()

    # Mob Attributes
    mob_id = key_id  # ID
    name = result_json['NameZh__EN']  # Name
    element = result_json['Nature']  # Element
    race = result_json['Race']  # Race
    size = result_json['Shape']  # Size
    mob_type = result_json['Type']  # MVP?
    location_key = list(result_json['Location'])[0]  # Need location key
    location = result_json['Location'][str(location_key)]['NameZh__EN']  # Location
    base_exp = result_json['BaseExp']  # Base EXP
    job_exp = result_json['JobExp']  # Job EXP
    strength = result_json['Str']  # STR
    agility = result_json['Agi']  # AGI
    vitality = result_json['Vit']  # VIT ## NULL? == 0?
    intellect = result_json['Int']  # INT ## NULL? (same)
    dexterity = result_json['Dex']  # DEX
    luck = result_json['Luk']  # LUK ## STRING?
    atk = result_json['Atk']  # ATK
    m_atk = result_json['MAtk']  # Magic ATK
    defense = result_json['Def']  # Defense
    m_defense = result_json['MDef']  # Magic Defense
    hit = result_json['Hit']  # Hit
    flee = result_json['Flee']  # Flee
    move_spd = result_json['MoveSpd']  # Movement Speed

    mob_attributes = [mob_id, name, element, race, size, mob_type, location, base_exp, job_exp,
                      strength, agility, vitality, intellect, dexterity, luck,
                      atk, m_atk, defense, m_defense, hit, flee, move_spd]

    # Convert None/null type to 0
    for i in range(0, len(mob_attributes)):
        if mob_attributes[i] is None:
            mob_attributes[i] = 0

    # Convert potential strings in integer attributes to int
    for i in range(7, len(mob_attributes)):
        mob_attributes[i] = int(mob_attributes[i])

    # Grab Loot IDs
    loot_ids = []
    for i in range(0, len(result_json['LootData'])):
        loot_ids.append(result_json['LootData'][i]['id'])

    # Grab in-game names
    loot_names = []
    for i in range(0, len(result_json['LootData'])):
        # ID 100 = Zeny (currency) which must be indexed differently than other IDs
        if loot_ids[i] == 100:
            loot_names.append(result_json['LootData'][i]['item_data']['NameZh'])
        else:
            loot_names.append(result_json['LootData'][i]['item_data']['NameZh__EN'])

    # Grab quantity of item - always either 1 or XXX int (zeny)
    loot_qtys = []
    for i in range(0, len(result_json['LootData'])):
        loot_qtys.append(result_json['LootData'][i]['num'])

    # Merge zeny and quantities
    for i in range(0, len(result_json['LootData'])):
        if loot_names[i] == 'Zeny':
            loot_names[i] = str(loot_qtys[i]) + ' Zeny'

    # Combine the data (mob stats and mob loot)
    mob_data_all = mob_attributes + loot_names
    return mob_data_all
