#!/usr/bin/python

from requests import get
from simplejson import loads
from datetime import datetime, timedelta
from calendar import timegm

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

    #build information
    def get_current_build(self):
        return self.api_call('build.json')['build_id']

    #world information
    def get_world_id_from_name(self, world_name):
        return [world['id'] for world in self.get_world_metadata() if world_name == world['name']][0]

    def get_world_name_from_id(self, uid):
        return [world['name'] for world in self.get_world_metadata() if uid == world['id']][0]

    def get_world_names(self):
        return sorted([world['name'] for world in self.get_world_metadata()])

    def get_world_metadata(self):
        return self.api_call('world_names.json')

    #guild details
    def get_guild_details_from_name(self, guild_name):
        return self.api_call('guild_details.json', params=[('guild_name', guild_name)])

    def get_guild_details_from_id(self, gid):
        return self.api_call('guild_details.json', params=[('guild_id', gid)])

    #map information
    @memoize(expiry=3600)
    def get_map_metadata(self, lang='en'):
        params = [('lang', lang)]
        return self.api_call('map_names.json', params=params)

    def get_map_id_from_name(self, map_name):
        return [wmap['id'] for wmap in self.get_map_metadata() if map_name == wmap['name']][0]

    def get_map_name_from_id(self, uid):
        return [wmap['name'] for wmap in self.get_world_metadata() if uid == wmap['id']][0]



    #event information
    @memoize(expiry=3600)
    def get_event_metadata(self, lang='en'):
        return self.api_call('event_names.json', params=[('lang', lang)])

    def get_event_id_from_name(self, event_name):
        return [event['id'] for event in self.get_event_metadata() if event['name'] == event_name][0]

    def get_event_name_from_id(self, eid):
        return [event['name'] for event in self.get_event_metadata() if event['id'] == eid][0]

    def get_dynamic_event_information(self, world_id, event_id='', map_id=''):
        params = [('world_id', world_id)]
        if event_id:
            params.append(('event_id', event_id))
        if map_id:
            params.append(('map_id', map_id))
        if event_id:
            return self.api_call('events.json', params=params)['events'][0]
        else:
            return self.api_call('events.json', params=params)['events']


    def get_all_dynamic_event_info_for_world(self, world_id):
        events = self.api_call('events.json', params=[('world_id', world_id)])['events']
        result = {}
        for event in events:
            result[event['event_id']] = event
        return result

    @memoize(expiry=3600)
    def get_all_static_event_info(self):
        result = {}
        events = self.api_call('event_details.json', params=[('lang', 'en')])['events']
        for event in events:
            result[event] = events[event]
        return events

    def get_all_events_by_state(self, world_id, states):
        events = self.get_all_dynamic_event_info_for_world(world_id)
        result = {}
        for event in events:
            if events[event]['state'] in states:
                result[event] = events[event]
        return result

    def get_all_active_events(self, world_id):
        return self.get_all_events_by_state(world_id, ['Active'])

    def get_all_events_starting_soon(self, world_id):
        return self.get_all_events_by_state(world_id, ['Warmup', 'Preparation'])


    @memoize(expiry=30)
    def get_comprehensive_event_information(self, world_id):
        result = self.get_all_static_event_info()
        dynamic = self.get_all_dynamic_event_info_for_world(world_id)
        for eid in dynamic.keys():
            if eid in result:
                result[eid] = dict(result[eid].items() + dynamic[eid].items())
            else:
                result[eid] = dynamic[eid]
        return result

    #file methods
    def get_file_information(self):
        return self.api_call('files.json')

    #item methods
    @memoize(expiry=3600)
    def get_all_item_ids(self):
        return self.api_call('items.json')['items']

    @memoize(expiry=3600)
    def get_item_details(self, item_id):
        return self.api_call('item_details.json', params=[('lang', 'en'), ('item_id', item_id)])

    @memoize(expiry=3600)
    def get_all_item_information(self):
        result = {}
        for uid in self.get_all_item_ids():
            result[uid] = self.get_item_details(uid)
        return result

    #recipe methods
    @memoize(expiry=3600)
    def get_all_recipe_ids(self):
        return self.api_call('recipes.json')['recipes']

    @memoize(expiry=3600)
    def get_recipe_details(self, recipe_id):
        return self.api_call('recipe_details.json', params=[('lang', 'en'), ('recipe_id', recipe_id)])

    @memoize(expiry=3600)
    def get_all_recipe_information(self):
        result = {}
        for uid in self.get_all_item_ids():
            result[uid] = self.get_recipe_details(uid)
        return result

    #utility methods
    def api_call(self, endpoint, version='v1', params=[]):
        '''params should be a list of tuples where key is fist and value is second
        '''
        base_rest_target = '/'.join([self.base_url, version, endpoint])
        parameters = ['{0}={1}'.format(key, val) for key, val in params]
        rest_target = '&'.join([base_rest_target] + parameters).replace('&', '?', 1)
        #print base_rest_target, parameters, rest_target
        return loads(get(rest_target).text)

    #TODO REORG
    def print_event_train_status(self, event_ids, world_id, map_id='', width=80):
        for i in event_ids:
            print '{0: <{1}}:  {2}'.format(self.get_event_name_from_id(i)[:width], width, h.get_dynamic_event_information(WORLD, map_id=map_id, event_id=i)['state'])
        print

    def fuzzy_search_event(self, event_name):
        print event_name
        for i in [event for event in h.get_event_metadata() if event_name in event['name']]:
            print i

h = Helios()
from pprint import pprint as pp
#print h.get_world_id_from_name('Fort Aspenwood')
#print h.get_event_id_from_name('Defeat Tequatl the Sunless.')
#print h.get_dynamic_event_information(h.get_event_id_from_name('Defeat Tequatl the Sunless.'), world_id=h.get_world_id_from_name('Fort Aspenwood'))
#pp(h.get_all_dynamic_event_info_for_world(h.get_world_id_from_name('Fort Aspenwood')))
#pp(h.get_all_static_event_info())
#pp(h.get_comprehensive_event_information(h.get_world_id_from_name('Fort Aspenwood')))
#pp(h.get_file_information())
#pp(h.get_all_item_information())
#pp(h.get_all_recipe_ids())
#pp(h.get_recipe_details(5467))
#pp(h.get_all_active_events(h.get_world_id_from_name('Fort Aspenwood')))
#pp(h.get_all_events_starting_soon(h.get_world_id_from_name('Fort Aspenwood')))

#pp(h.get_map_metadata())
#print "def get_dynamic_event_information(self, world_id, event_id='', map_id=''):"
#pp(h.get_map_id_from_name('Queensdale'))
#pp(h.get_dynamic_event_information(h.get_world_id_from_name('Fort Aspenwood'), map_id=h.get_map_id_from_name('Queensdale')))

WORLD = 'Fort Aspenwood'
WORLD_ID = h.get_world_id_from_name(WORLD)
MAP = 'Queensdale'
MAP_ID = h.get_map_id_from_name(MAP)

print 'Queensdale Event Train'
eids = [
    'D17D47E9-0A87-4189-B02A-54E23AA91A82', #cave troll
    'BC997F15-4C05-4D95-A14F-9B7C4CF41B4E', #bandit lieutenant
    '04084490-0117-4D56-8D67-C4FFFE933C0C', #rotting oakheart
    '3C3915FB-E2E4-4794-A700-E3B5FCFE0404', #wasp queen
    '69D031A8-7AD2-4419-B564-48457841A57C'] #Giant Boar
h.print_event_train_status(eids, WORLD_ID, map_id=MAP_ID)

print 'Shatterer'
eids = [
    '580A44EE-BAED-429A-B8BE-907A18E36189', #Collect siege weapon pieces for Crusader Blackhorn
    '8E064416-64B5-4749-B9E2-31971AB41783', #Escort the Sentinel squad to the Vigil camp in Lowland Burns
    '03BF176A-D59F-49CA-A311-39FC6F533F2F'] #Slay the shatterer
h.print_event_train_status(eids, WORLD_ID)

print 'Claw of Jormag'
eids = [
    '13F20FCE-45E5-4496-9EB8-31AB7199530A', #Eliminate corrupted ice cores
    '0464CB9E-1848-4AAA-BA31-4779A959DD71'] #Defat the Claw of Jormag
h.print_event_train_status(eids, WORLD_ID)
print 'Fire Elemental'
eids = [
    '5E4E9CD9-DD7C-49DB-8392-C99E1EF4E7DF',
    '2C833C11-5CD5-4D96-A4CE-A74C04C9A278',
    '33F76E9E-0BB6-46D0-A3A9-BE4CDFC4A3A4']
h.print_event_train_status(eids, WORLD_ID)
