#!/usr/bin/python


from tabulate import tabulate
import argparse

buy_items = {
    'prototype_fractal_capacitor': 1350,
    'gift_of_ascension': 500,
    '20_slot_fractal_exotic_equipment_box': 250,
    '20_slot_fractal_rare_equipment_box': 200,
    '20_slot_fractal_uncommon_equipment_box': 150,
    'versatile_simple_infusion': 75,
    'dessas_experimental_journal': 35,
    'obsidian_shard': 15}

def generate_fractal_rewards(tier_width=5, max_tier=10, tier_0_award=5):
    fr = {}
    for tier in xrange(max_tier):
        for level_mod in xrange(tier_width):
          fractal_level = (tier_width * tier) + level_mod + 1
          #print fractal_level, ( tier_0_award + tier ) * 4
          fr[fractal_level] = ( tier_0_award + tier ) * 4

    return fr

def count_remaining_runs(fractal_rewards, current_inventory, item_name, item_price, starting_fractal_level, target_inventory, lvl_cap, starting_relics):
    current_inventory = int(current_inventory)
    togo = target_inventory - current_inventory
    cur_lvl = starting_fractal_level

    print 'Target Item:  {0}'.format(item_name)
    print 'Target Inventory:  {0}'.format(target_inventory)
    print 'Current Inventory:  {0}'.format(current_inventory)
    print 'Needed Inventory:  {0}'.format(togo)
    print 'Relics per item:  {0}'.format(item_price)

    runs = 0
    result = []
    reward = starting_relics

    while togo > 0:
        runs += 1
        reward += fractal_rewards[cur_lvl]

        result.append([runs, cur_lvl, reward, reward / item_price, togo, reward % item_price])
        togo -= reward / item_price
        reward = reward % item_price
        if cur_lvl < lvl_cap:
            cur_lvl += 1

    print "Runs remaining: ", runs
    print "Final fractal level", cur_lvl
    return result

#get item cost from table
target_inventory = 250
starting_relics = 0
starting_fractal_level = 1
fractal_level_limit = 50

parser = argparse.ArgumentParser(description='Calculate how many fractal runs its going to take in order to buy a quantity of items from BUY-4374.')
parser.add_argument('--item-name', help='The item you want to buy with fractal relics.', required=True)
parser.add_argument('--current-inventory', default=0, type=int, help='The quantify of your desired item that you already possess.')
parser.add_argument('--target-inventory', default=1, type=int, help='The total quantity of items you want to possess.')
parser.add_argument('--starting-fractal-level', default=1, type=int, help='The highest level fractal you can run now.')
parser.add_argument('--fractal-level-limit', default=50, type=int, help='The highest level fractal you are willing to run.')
parser.add_argument('--starting_relics', default=0, type=int, help='The number of fractal relics you currently possess.')

args = parser.parse_args()
try:
    item_price = buy_items[args.item_name]
except:
    print 'Please select your item from one of the following:\n'
    print '\n'.join(sorted(buy_items.keys()))
    exit(-1)

fractal_rewards = generate_fractal_rewards()

result = count_remaining_runs(
    fractal_rewards,
    args.current_inventory,
    args.item_name,
    item_price,
    args.starting_fractal_level,
    args.target_inventory,
    args.fractal_level_limit,
    args.starting_relics)

print
print tabulate(result, ['Run', 'Level', 'Relics', 'Target Items', 'Remaining Items', 'Unused Relics'])
