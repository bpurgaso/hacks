#!/usr/bin/python


from tabulate import tabulate

'''
fractal_rewards = {
        '1-5': {'boss': 15, 'norm': 5},
        '6-10': {'boss': 20, 'norm': 6},
        '11-15': {'boss': 25, 'norm': 7},
        '16-20': {'boss': 30, 'norm': 8},
        '21-25': {'boss': 35, 'norm': 9},
        '26-30': {'boss': 40, 'norm': 10},
        '31-35': {'boss': 45, 'norm': 11},
        '36-40': {'boss': 50, 'norm': 12},
        '41-45': {'boss': 55, 'norm': 14},
        '46-50': {'boss': 60, 'norm': 15}}
'''

def generate_fractal_rewards(tier_width=5, starting_level=1, tiers=10):
    fr = {}
    for i in xrange(starting_level, tier_width*tiers, tier_width):
        tier_info = {}
        lower_bound = i - 1
        cur_tier = lower_bound / tier_width

        tier_info['boss'] = cur_tier * 5 + 10
        tier_info['norm'] = cur_tier + 5

        if cur_tier >= 8:
            tier_info['norm'] += 1

        fr['{0}-{1}'.format(lower_bound+1, lower_bound+tier_width)] = tier_info
        fr['0-0'] = tier_info
    return fr

def get_tier_key(fractal_rewards, lvl):
    for i in fractal_rewards:
        low, high = i.split('-')
        low, high = int(low), int(high)
        if lvl >= low and lvl <= high:
            return i
    return '0-0'


def count_remaining_runs(fractal_rewards, current_inventory, item_price, starting_f_level=0, target_inventory=250, lvl_cap=48, starting_relics=0):
    current_inventory = int(current_inventory)
    togo = target_inventory - current_inventory
    cur_lvl = starting_f_level
    f_length = (4, 3)

    print 'Target Inventory:  {0}'.format(target_inventory)
    print 'Current Inventory:  {0}'.format(current_inventory)
    print 'Needed Inventory:  {0}'.format(togo)
    print 'Relics per item:  {0}'.format(item_price)

    runs = 0
    result = []
    reward = starting_relics

    while togo > 0:
        runs += 1
        tkey = get_tier_key(fractal_rewards, cur_lvl)
        reward += fractal_rewards[tkey]['norm'] * f_length[cur_lvl % 2]
        if cur_lvl % 2 == 0:
            reward += fractal_rewards[tkey]['boss']

        result.append([runs, cur_lvl, reward, reward / item_price, togo, reward % item_price])
        togo -= reward / item_price
        reward = reward % item_price
        if cur_lvl < lvl_cap:
            cur_lvl += 1

    print "Runs remaining: ", runs
    print "Final level", cur_lvl
    return result



fractal_rewards = generate_fractal_rewards()
result = count_remaining_runs(fractal_rewards, 217, 15, target_inventory=250, starting_f_level=8, starting_relics=14)
print tabulate(result, ['Run', 'Level', 'Relics', 'Target Items', 'Remaining Items', 'Unused Relics'])
