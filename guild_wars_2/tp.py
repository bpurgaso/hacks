#!/usr/bin/python

from requests import get
from simplejson import loads
from datetime import datetime, timedelta
from calendar import timegm

import yaml

cache = {}
def memoize(expiry=1):
    global cache
    def function1(f):
        def function2(*args, **kwargs):
            key = str(hash(str(f.__name__)) + hash(str(args)) + hash(str(kwargs)))
            date_key = key + 'date'
            if key in cache and cache[date_key] > timegm(datetime.utcnow().timetuple()):
                return cache[key]
            else:
                tmp = f(*args, **kwargs)
                cache[key] = tmp
                cache[date_key] = timegm((datetime.utcnow() + timedelta(seconds=expiry)).timetuple())
                return tmp
        return function2
    return function1

class Helios(object):
    def __init__(self, base_url='https://api.guildwars2.com'):
        self.base_url = base_url

    # utility methods
    def api_call(self, endpoint, version='v2', params=[], kparams=[]):
        '''params should be a list of tuples where key is fist and value is second
        '''
        if params and kparams:
            raise Exception('cannot create call with p and pk.')

        base_rest_target = '/'.join([self.base_url, version, endpoint])
        if params:
            parameters = ','.join(params)
            rest_target = '/'.join([base_rest_target, parameters])
        else:
            parameters = ['{0}={1}'.format(key, val) for key, val in kparams]
            rest_target = '&'.join([base_rest_target] + parameters).replace('&', '?', 1)
        #print base_rest_target, parameters, rest_target
        print rest_target
        return loads(get(rest_target).text)

    # items api
    def get_all_item_ids(self):
        return self.api_call('items')

    def get_item_info(self, id):
        return self.api_call('items', params=[id])

    def get_all_recipe_ids(self):
        return self.api_call('recipes')

    def get_recipe_info(self, id):
        return self.api_call('recipes', params=[id])

    def search_recipe(self, id, id_is_output=False):
        if id_is_output:
            return self.api_call('recipes/search', kparams=[('output', id)])
        else:
            return self.api_call('recipes/search', kparams=[('input', id)])

    def get_recipe_that_uses_id(self, id):
        return self.search_recipe(id)

    def get_recipe_that_makes_id(self, id):
        return self.search_recipe(id, id_is_output=True)

    def get_all_skin_ids(self):
        return self.api_call('skins')

    def get_skin_info(self, id):
        return self.api_call('skins', params=[id])

    # listings
    def get_listings_for_ids(self, id_list):
        return self.api_call('commerce/listings', kparams=[('ids', ','.join(id_list))])

    def get_prices_for_ids(self, id_list):
        return self.api_call('commerce/prices', kparams=[('ids', ','.join(id_list))])

    # DOES NOT IMPLEMENT COINS/GEMS/CONTINENTS

#driver
h = Helios()
#print h.get_all_item_ids()
#print h.get_item_info('68344')
#print h.get_all_recipe_ids()
#print h.get_recipe_info('9775')
#print h.search_recipe('46731')
#print h.get_recipe_that_uses_id('46731')
#print h.get_recipe_that_makes_id('50065')
#print h.get_all_skin_ids()
#print h.get_skin_info('10')
#print h.get_listings_for_ids(['19684'])
#print h.get_listings_for_ids(['19684', '19709'])
#print h.get_prices_for_ids(['19684'])
#print h.get_prices_for_ids(['19684', '19709'])

with open('./config.yaml') as f:
    config = yaml.load(f.read())
