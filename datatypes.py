# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@khine.net>

# Import from the Standard Library
from operator import itemgetter

# Import from itools
from itools.core import get_abspath
from itools.csv import CSVFile
from itools.datatypes import Boolean, Integer, String, Unicode,\
                    Email, Tokens, Date, Decimal, Enumerate
from itools.gettext import MSG
from itools.handlers import RWDatabase, ro_database, checkid
from itools.web import get_context

# Geographical datatypes
def sort_key(option):
    return "other" in option.itervalues(), option["name"]


class WorldSchema(CSVFile):
    class_csv_guess = True
    
    columns = ['id', 'continent', 'sub_id', 'sub_continent', 'country_id',
                'iana_root_zone', 'country', 'region', 'county']

    schema = {'id': Integer,
            'continent': String,
            'sub_id': Integer,
            'sub_continent': String,
            'country_id': Integer,
            'iana_root_zone': String,
            'country': String,
            'region': Unicode,
            'county': Unicode}

def get_world():
    context = get_context()
    root = context.resource.get_root().handler
    world = root.get_handler('world.csv', WorldSchema)
    rows = [
       x for x in world.get_rows() if x.get_value('region') != u"" ]
    return rows

class getCountries(Enumerate):

    @classmethod
    def get_options(cls):
        '''
            return JSON ser
        '''
        list_countries = set()
        for row in get_world():
            country = row.get_value('country')
            iana_root_zone = row.get_value('iana_root_zone')
            list_countries.add((iana_root_zone, country))
        options = []
        for index, row in enumerate(list_countries):
            options.append({'name': row[0], 'value': MSG(row[1]), 'title': checkid(row[1]), 'selected': None})
        return sorted(options, key=itemgetter('title'))


class getRegions(Enumerate):

    @classmethod
    def get_options(cls, iana_root_zone):

        list_regions = set()
        country_name = []
        for row in get_world():
            if row.get_value('iana_root_zone') == iana_root_zone:
                list_regions.add(row.get_value('region'))
                if country_name == []:
                    country_name.append(row.get_value('country'))
        options = []
        for index, row in enumerate(list_regions):
            name = '%s#%s' % (iana_root_zone, checkid(row))
            options.append({'name': name, 'value': row, 'selected': False})
        options.sort(key=sort_key)
        options.insert(0, {'name': 'switch', 'value': '* not from ' + country_name[0] + ' *', 'selected': False})

        return options


class getCounties(Enumerate):

    @classmethod
    def get_options(cls, iana_root_zone, region, county_name=None):
        options = []
        for row in get_world():
            if region == checkid(row.get_value('region')):
                county = row.get_value('county')
                name = '%s#%s#%s' % (iana_root_zone, region, checkid(county))
                if county_name == checkid(row.get_value('county')):
                    options.append({'name': name, 'value': county, 'selected': True })
                else:
                    options.append({'name': name, 'value': county, 'selected': False})
        options.sort(key=sort_key)
        if iana_root_zone:
            switch = '%s#%s#switch' % (iana_root_zone, region)
        else:
            switch = 'none#none#switch'
        options.insert(0, {'name': switch, 'value': 'Choose different region!', 'selected': False})

        return options


class Continent(Enumerate):

    options =  [
        {'value': 'africa', 'name': MSG(u"Africa")},
        {'value': 'americas', 'name': MSG(u"Americas")},
        {'value': 'asia', 'name': MSG(u"Asia")},
        {'value': 'europe', 'name': MSG(u"Europe")},
        {'value': 'eceania', 'name': MSG(u"Oceania")}
    ]


class SubContinent(Enumerate):

    options =  [
        {'value': 'Africa', 'name': MSG(u"Africa")},
        {'value': 'Americas', 'name': MSG(u"Americas")},
        {'value': 'Asia', 'name': MSG(u"Asia")},
        {'value': 'Europe', 'name': MSG(u"Europe")},
        {'value': 'Oceania', 'name': MSG(u"Oceania")}
    ]


# Industry datatypes
class Industry(Enumerate):
    options =  [
        {'name': 'building', 'value': MSG(u"Building Trade")},
        {'name': 'travel', 'value': MSG(u"Travel & Hospitality")},
    ]

class Affiliation(Enumerate):
    '''
    returns a list of dictionaries such as
    {'industry': 'travel', 'value': 'AAC', 'name': MSG(u"Association of Airline Cons.")}
    '''
    def get_options(cls):
        context = get_context()
        here = context.resource
        root = here.get_root().handler
        csv = root.get_handler('affiliations.csv')
        options = []
        for index, row in enumerate(csv.get_rows()):
            options.append({'name': row[0], 'value': MSG(row[1])})
        options.sort(key=sort_key)
        
        return options

class BusinessSector(Enumerate):
    '''
    returns a list of dictionaries such as
    {'industry': 'travel', 'name': 'air-brokers-or-charters', 'value': MSG(u"Air brokers/air charter")}
    '''
    def get_options(cls):
        context = get_context()
        here = context.resource
        root = here.get_root().handler
        csv = root.get_handler('topics.csv')
        options = []
        # TODO check the root site and add Industry
        industry = 'travel'
        for index, row in enumerate(csv.get_rows()):
            # TODO filter rows only for specific industry
            options.append({'name': row[0], 'value': MSG(row[1])})  
        options.sort(key=sort_key)
        
        return options

class BusinessType(Enumerate):
    '''
    returns a list of dictionaries such as
    {'name': 'multiple', 'value': MSG(u"Multiple")},
    '''
    def get_options(cls):
        context = get_context()
        here = context.resource
        root = here.get_root().handler
        csv = root.get_handler('types.csv')
        options = []
        for index, row in enumerate(csv.get_rows()):
            options.append({'name': row[0], 'value': MSG(row[1])})
        options.sort(key=sort_key)
        
        return options

# Job datatypes
class Functions(Enumerate):
    '''
    returns a list of dictionaries such as
    {'name': 'multiple', 'value': MSG(u"Multiple")},
    '''
    def get_options(cls):
        context = get_context()
        here = context.resource
        root = here.get_root().handler
        csv = root.get_handler('functions.csv')
        options = []
        for index, row in enumerate(csv.get_rows()):
            options.append({'name': row[0], 'value': MSG(row[1])})
        options.sort(key=sort_key)
        
        return options

class JobSector(Enumerate):

    options = [
        {'industry': 'travel', 'value': 'airlines', 'name': MSG(u"Airlines")},
        {'industry': 'travel', 'value': 'business-travel', 'name': MSG(u"Business Travel")},
        {'industry': 'travel', 'value': 'call-centre-telesales', 'name': MSG(u"Call Centre/Telesales")},
        {'industry': 'travel', 'value': 'car-hire', 'name': MSG(u"Car Hire")},
        {'industry': 'travel', 'value': 'conference-incentives-events', 'name': MSG(u"Conference/Incentives/Events")},
        {'industry': 'travel', 'value': 'cruises', 'name': MSG(u"Cruises")},
        {'industry': 'travel', 'value': 'executive-management', 'name': MSG(u"Executive/Management")},
        {'industry': 'travel', 'value': 'foreign-exchange', 'name': MSG(u"Foreign Exchange")},
        {'industry': 'travel', 'value': 'hotel-leisure', 'name': MSG(u"Hotel/Leisure")},
        {'industry': 'travel', 'value': 'other', 'name': MSG(u"Other")},
        {'industry': 'travel', 'value': 'rail', 'name': MSG(u"Rail")},
        {'industry': 'travel', 'value': 'retail', 'name': MSG(u"Retail")},
        {'industry': 'travel', 'value': 'support-staff', 'name': MSG(u"Support Staff")},
        {'industry': 'travel', 'value': 'temporary', 'name': MSG(u"Temporary")},
        {'industry': 'travel', 'value': 'operations', 'name': MSG(u"Tour Operations")},
        {'industry': 'travel', 'value': 'overseas', 'name': MSG(u"Overseas")},
        {'industry': 'travel', 'value': 'reservations-ticketing', 'name': MSG(u"Reservations/Ticketing")},
        {'industry': 'travel', 'value': 'it', 'name': MSG(u"IT")},
        {'industry': 'travel', 'value': 'sales-marketing', 'name': MSG(u"Sales/Marketing")},
        {'industry': 'travel', 'value': 'student', 'name': MSG(u"Student")}]

class SalaryRange(Enumerate):

    options = [
        {'value': '1', 'name': MSG(u"Under £15K")},
        {'value': '2', 'name': MSG(u"£15K-£20K")},
        {'value': '3', 'name': MSG(u"£20K-£25K")},
        {'value': '4', 'name': MSG(u"£25K-£30K")},
        {'value': '5', 'name': MSG(u"£30K-£35K")},
        {'value': '6', 'name': MSG(u"£35K-£40K")},
        {'value': '7', 'name': MSG(u"£40K-£45K")},
        {'value': '8', 'name': MSG(u"£45K-£50K")},
        {'value': '9', 'name': MSG(u"£50K-£70K")},
        {'value': '10', 'name': MSG(u"£70K-£100K")},
        {'value': '11', 'name': MSG(u"£100K+")}]


# Hotel datatypes
class HotelTheme(Enumerate):

    options = [
    {'value': 'airport', 'name': MSG(u"Airport")},
    {'value': 'beach', 'name': MSG(u"Beach")},
    {'value': 'boutique', 'name': MSG(u"Boutique")},
    {'value': 'countryside', 'name': MSG(u"Countryside")},
    {'value': 'design', 'name': MSG(u"Design")},
    {'value': 'family-friendly', 'name': MSG(u"Family-friendly")},
    {'value': 'golf', 'name': MSG(u"Golf")},
    {'value': 'historic', 'name': MSG(u"Historic")},
    {'value': 'romantic', 'name': MSG(u"Romantic")},
    {'value': 'self-catering', 'name': MSG(u"Self-catering")},
    {'value': 'ski', 'name': MSG(u"Ski")},
    {'value': 'spa-hotel', 'name': MSG(u"Spa Hotel ")}]


class Rating(Enumerate):

    options = [
    {'value': 'one-star', 'name': MSG(u"One star")},
    {'value': 'two-stars', 'name': MSG(u"Two stars")},
    {'value': 'three-stars', 'name': MSG(u"Three stars")},
    {'value': 'four-stars', 'name': MSG(u"Four stars")},
    {'value': 'five-stars', 'name': MSG(u"Five stars")},
    {'value': 'five-stars-deluxe', 'name': MSG(u"Five stars - Deluxe")}]

class BoardType(Enumerate):

    options = [
    {'value': 'all', 'name': MSG(u"All Inclusive")},
    {'value': 'full-board', 'name': MSG(u"Full Board")},
    {'value': 'half-board', 'name': MSG(u"Half Board")},
    {'value': 'bed-and-breakfast', 'name': MSG(u"Bed & Breakfast")},
    {'value': 'self-catering', 'name': MSG(u"Self Catering")},
    {'value': 'room-only', 'name': MSG(u"Room Only")}
    ]

class HotelFacilities(Enumerate):

    options = [
    {'value': '24-hour-reception', 'name': MSG(u"24 hour reception")},
    {'value': 'babysitting-service', 'name': MSG(u"Babysitting service")},
    {'value': 'business-centre', 'name': MSG(u"Business centre")},
    {'value': 'child-activities', 'name': MSG(u"Child Activities")},
    {'value': 'currency-exchange-facilities', 'name': MSG(u"Currency exchange facilities")},
    {'value': 'exercise-room', 'name': MSG(u"Exercise room ")},
    {'value': 'express-check-in-check-out', 'name': MSG(u"Express check-in & check-out")},
    {'value': 'hot-tub', 'name': MSG(u"Hot Tub")},
    {'value': 'in-room-dining', 'name': MSG(u"In-room dining")},
    {'value': 'indoor-swimming-pool', 'name': MSG(u"Indoor swimming pool")},
    {'value': 'laundry-dry-cleaning-service', 'name': MSG(u"Laundry & dry cleaning service")},
    {'value': 'luggage-storage', 'name': MSG(u"Luggage storage")},
    {'value': 'outdoor-swimming-pool', 'name': MSG(u"Outdoor swimming pool")},
    {'value': 'parking', 'name': MSG(u"Parking")},
    {'value': 'pet-friendly', 'name': MSG(u"Pet Friendly")},
    {'value': 'restaurant-bar', 'name': MSG(u"Restaurant & bar")},
    {'value': 'wheelchair-accessible-rooms', 'name': MSG(u"Wheelchair accessible rooms ")},
    {'value': 'wireless-internet', 'name': MSG(u"Wireless internet")},
    {'value': 'with-spa', 'name': MSG(u"With Spa")}]


class RoomType(Enumerate):

    options =  [
        {'value': 'standard', 'name': MSG(u"Standard")},
        {'value': 'executive', 'name': MSG(u"Executive")},
        {'value': 'deluxe', 'name': MSG(u"Deluxe")},
        {'value': 'family', 'name': MSG(u"Family")},
        {'value': 'presidential', 'name': MSG(u"Presidential")},
    ]

# Holiday datatypes

class HolidayType(Enumerate):

    options = [
    {'value': 'camping-holiday', 'name': MSG(u"Camping Holiday")},
    {'value': 'coach-holiday', 'name': MSG(u"Coach holiday")},
    {'value': 'cruise', 'name': MSG(u"Cruise")},
    {'value': 'cultural', 'name': MSG(u"Cultural/historical/heritage")},
    {'value': 'flight-only', 'name': MSG(u"Flight only")},
    {'value': 'golfing-holiday', 'name': MSG(u"Golfing holiday")},
    {'value': 'wellness', 'name': MSG(u"Relax at a resort in a warm climate")},
    {'value': 'school-holiday-break', 'name': MSG(u"School Holiday Breaks")},
    {'value': 'short-city-break', 'name': MSG(u"Short/City Break")},
    {'value': 'ski-winter-sports', 'name': MSG(u"Ski/ Winter sports")},
    {'value': 'theme-park-based', 'name': MSG(u"Theme park based holiday")},
    {'value': 'villa-holidays', 'name': MSG(u"Villa Holidays")},
    {'value': 'walking-rambling', 'name': MSG(u"Walking/ Rambling")}]


class HolidayActivity(Enumerate):

    options = [
    {'value': 'adults-only', 'name': MSG(u"Adults Only")},
    {'value': 'agricultural', 'name': MSG(u"Agricultural")},
    {'value': 'military-history', 'name': MSG(u"Military History")},
    {'value': 'various', 'name': MSG(u"Various")},
    {'value': 'general', 'name': MSG(u"General")},
    {'value': 'all-inclusive', 'name': MSG(u"All inclusive")},
    {'value': 'spiritual', 'name': MSG(u"Spiritual")},
    {'value': 'wellness', 'name': MSG(u"Wellness")},
    {'value': 'holistic', 'name': MSG(u"Holistic")},
    {'value': 'dialysis', 'name': MSG(u"Dialysis ")},
    {'value': 'motor-racing', 'name': MSG(u"Motor Racing")},
    {'value': 'motoring-self-drive', 'name': MSG(u"Motoring (Self Drive)")},
    {'value': 'mountaineering', 'name': MSG(u"Mountaineering")},
    {'value': 'music-opera', 'name': MSG(u"Music (Opera)")},
    {'value': 'music-rock-pop', 'name': MSG(u"Music (Rock & Pop)")},
    {'value': 'murder-mystery', 'name': MSG(u"Murder Mystery")},
    {'value': 'music-jazz', 'name': MSG(u"Music (Jazz)")},
    {'value': 'boxing', 'name': MSG(u"Boxing")},
    {'value': 'netball', 'name': MSG(u"Netball")},
    {'value': 'naturist', 'name': MSG(u"Naturist")},
    {'value': 'nostalgia', 'name': MSG(u"Nostalgia")},
    {'value': 'older-generation', 'name': MSG(u"Older Generation")},
    {'value': 'olympics-summer', 'name': MSG(u"Olympics (Summer)")},
    {'value': 'olympics-winter', 'name': MSG(u"Olympics (Winter)")},
    {'value': 'paralympics', 'name': MSG(u"Paralympics")},
    {'value': 'backpacking', 'name': MSG(u"Backpacking")},
    {'value': 'outdoor-pursuits', 'name': MSG(u"Outdoor Pursuits")},
    {'value': 'paragliding', 'name': MSG(u"Paragliding")},
    {'value': 'parasailing', 'name': MSG(u"Parasailing")},
    {'value': 'photography', 'name': MSG(u"Photography")},
    {'value': 'polo', 'name': MSG(u"Polo")},
    {'value': 'beer-festivals', 'name': MSG(u"Beer Festivals")},
    {'value': 'ranch-holidays', 'name': MSG(u"Ranch Holidays")},
    {'value': 'rail-railways', 'name': MSG(u"Rail/Railways")},
    {'value': 'religious-pilgrimages', 'name': MSG(u"Religious/Pilgrimages")},
    {'value': 'rugby-playing', 'name': MSG(u"Rugby (Playing)")},
    {'value': 'rugby-watching', 'name': MSG(u"Rugby (Watching)")},
    {'value': 'romantic', 'name': MSG(u"Romantic")},
    {'value': 'round-the-world', 'name': MSG(u"Round the World")},
    {'value': 'basketball', 'name': MSG(u"Basketball")},
    {'value': 'safari-wildlife', 'name': MSG(u"Safari/Wildlife")},
    {'value': 'sailing-boating-yachting', 'name': MSG(u"Sailing/Boating/Yachting")},
    {'value': 'school-tours', 'name': MSG(u"School Tours")},
    {'value': 'shooting', 'name': MSG(u"Shooting")},
    {'value': 'singles', 'name': MSG(u"Singles")},
    {'value': 'skiing', 'name': MSG(u"Skiing")},
    {'value': 'snowboarding', 'name': MSG(u"Snowboarding")},
    {'value': 'ornithology', 'name': MSG(u"Ornithology")},
    {'value': 'squash', 'name': MSG(u"Squash")},
    {'value': 'scrabble', 'name': MSG(u"Scrabble")},
    {'value': 'tailor-made', 'name': MSG(u"Tailor-Made")},
    {'value': 'tennis-playing', 'name': MSG(u"Tennis (Playing)")},
    {'value': 'tennis-watching', 'name': MSG(u"Tennis (Watching)")},
    {'value': 'theme-park', 'name': MSG(u"Theme Park")},
    {'value': 'trade-fairs', 'name': MSG(u"Trade Fairs")},
    {'value': 'trekking', 'name': MSG(u"Trekking")},
    {'value': 'battlefield-tours', 'name': MSG(u"Battlefield Tours")},
    {'value': 'upmarket', 'name': MSG(u"Upmarket")},
    {'value': 'volleyball', 'name': MSG(u"Volleyball")},
    {'value': 'botany-naturalist', 'name': MSG(u"Botany/Naturalist")},
    {'value': 'walking-rambling', 'name': MSG(u"Walking/Rambling")},
    {'value': 'watersports', 'name': MSG(u"Watersports")},
    {'value': 'weddings-abroad', 'name': MSG(u"Weddings Abroad")},
    {'value': 'white-water-rafting', 'name': MSG(u"White Water Rafting")},
    {'value': 'windsurfing', 'name': MSG(u"Windsurfing")},
    {'value': 'vineyard-wine-tasting', 'name': MSG(u"Vineyard/Wine Tasting")},
    {'value': 'winter-sports', 'name': MSG(u"Winter Sports")},
    {'value': 'young-persons-summer-camps', 'name': MSG(u"Young Persons - Summer Camps")},
    {'value': 'young-persons-18-30', 'name': MSG(u"Young Persons (18-30)")},
    {'value': 'bowls-crown-greens', 'name': MSG(u"Bowls (Crown & Greens)")},
    {'value': 'young-persons', 'name': MSG(u"Young Persons")},
    {'value': 'whale-dolphin-watching', 'name': MSG(u"Whale/Dolphin Watching")},
    {'value': 'single-parents', 'name': MSG(u"Single Parents")},
    {'value': 'sports-general', 'name': MSG(u"Sports - General")},
    {'value': 'martial-arts', 'name': MSG(u"Martial Arts")},
    {'value': 'the-arts', 'name': MSG(u"The Arts")},
    {'value': 'bowling-ten-pin', 'name': MSG(u"Bowling (Ten-Pin)")},
    {'value': 'activity', 'name': MSG(u"Activity")},
    {'value': 'bungee-jumping', 'name': MSG(u"Bungee Jumping")},
    {'value': 'groups', 'name': MSG(u"Groups")},
    {'value': 'bridge', 'name': MSG(u"Bridge")},
    {'value': 'country-retreats', 'name': MSG(u"Country Retreats")},
    {'value': "children's-holiday-club", 'name': MSG(u"Children\'s Holiday Club")},
    {'value': 'ballooning', 'name': MSG(u"Ballooning")},
    {'value': 'eco-tours', 'name': MSG(u"Eco Tours")},
    {'value': 'camper-motorhome', 'name': MSG(u"Camper/Motorhome")},
    {'value': 'camping-caravan', 'name': MSG(u"Camping/Caravan")},
    {'value': 'canal-river-cruises', 'name': MSG(u"Canal/River Cruises")},
    {'value': 'canoeing', 'name': MSG(u"Canoeing")},
    {'value': 'adventure', 'name': MSG(u"Adventure")},
    {'value': 'christmas-new-year', 'name': MSG(u"Christmas/New Year")},
    {'value': 'church-cathedral', 'name': MSG(u"Church/Cathedral")},
    {'value': 'city-tours', 'name': MSG(u"City Tours")},
    {'value': 'coach', 'name': MSG(u"Coach")},
    {'value': 'cook-gastronomic', 'name': MSG(u"Cook/Gastronomic")},
    {'value': 'cricket', 'name': MSG(u"Cricket")},
    {'value': 'cruise', 'name': MSG(u"Cruise")},
    {'value': 'cultural', 'name': MSG(u"Cultural")},
    {'value': 'cycling', 'name': MSG(u"Cycling")},
    {'value': 'crusader-castle-tours', 'name': MSG(u"Crusader/Castle Tours")},
    {'value': 'american-sports', 'name': MSG(u"American Sports")},
    {'value': 'corporate', 'name': MSG(u"Corporate")},
    {'value': 'visa-service', 'name': MSG(u"Visa Service")},
    {'value': 'parking', 'name': MSG(u"Parking")},
    {'value': 'dancing', 'name': MSG(u"Dancing")},
    {'value': 'transport-to-from-airports', 'name': MSG(u"Transport To & From Airports")},
    {'value': 'gay', 'name': MSG(u"Gay")},
    {'value': 'airport-hotel-reservations', 'name': MSG(u"Airport Hotel Reservations")},
    {'value': 'day-trips', 'name': MSG(u"Day Trips")},
    {'value': 'disabled', 'name': MSG(u"Disabled")},
    {'value': 'diving', 'name': MSG(u"Diving")},
    {'value': 'drama-tours', 'name': MSG(u"Drama Tours")},
    {'value': 'dream-machines', 'name': MSG(u"Dream Machines")},
    {'value': 'animal-watching', 'name': MSG(u"Animal Watching")},
    {'value': 'long-stay-duration', 'name': MSG(u"Long Stay/Duration")},
    {'value': 'music-classical', 'name': MSG(u"Music (Classical)")},
    {'value': 'out-of-the-ordinary', 'name': MSG(u"Out of the Ordinary")},
    {'value': 'educational', 'name': MSG(u"Educational")},
    {'value': 'expeditions', 'name': MSG(u"Expeditions")},
    {'value': 'exhibitions', 'name': MSG(u"Exhibitions")},
    {'value': 'escorted-tours', 'name': MSG(u"Escorted Tours")},
    {'value': 'space-travel', 'name': MSG(u"Space Travel")},
    {'value': 'titanic-trips', 'name': MSG(u"Titanic Trips")},
    {'value': 'archaeology', 'name': MSG(u"Archaeology")},
    {'value': 'underwater-caves', 'name': MSG(u"Underwater Caves")},
    {'value': 'shopping-markets', 'name': MSG(u"Shopping/Markets")},
    {'value': 'festivals-carnivals', 'name': MSG(u"Festivals/Carnivals")},
    {'value': 'fishing', 'name': MSG(u"Fishing")},
    {'value': 'fishing-deep-sea', 'name': MSG(u"Fishing (Deep Sea)")},
    {'value': 'floral-gardening', 'name': MSG(u"Floral/Gardening")},
    {'value': 'football-playing', 'name': MSG(u"Football (Playing)")},
    {'value': 'football-watching', 'name': MSG(u"Football (Watching)")},
    {'value': 'fly-drive', 'name': MSG(u"Fly-Drive")},
    {'value': 'stag-hen-dos', 'name': MSG(u"Stag & Hen Dos")},
    {'value': 'archery', 'name': MSG(u"Archery")},
    {'value': 'extreme-sports', 'name': MSG(u"Extreme Sports")},
    {'value': 'villa-rentals', 'name': MSG(u"Villa Rentals")},
    {'value': 'short-weekend-breaks', 'name': MSG(u"Short/Weekend Breaks")},
    {'value': 'golf-playing', 'name': MSG(u"Golf (Playing)")},
    {'value': 'ghost-hunting-hauntings', 'name': MSG(u"Ghost Hunting/Hauntings")},
    {'value': 'golf-watching', 'name': MSG(u"Golf (Watching)")},
    {'value': 'voluntary', 'name': MSG(u"Voluntary")},
    {'value': 'working-holidays', 'name': MSG(u"Working Holidays")},
    {'value': 'health-spa-fitness', 'name': MSG(u"Health/Spa/Fitness")},
    {'value': 'architecture', 'name': MSG(u"Architecture")},
    {'value': 'historical-heritage', 'name': MSG(u"Historical/Heritage")},
    {'value': 'special-needs', 'name': MSG(u"Special Needs")},
    {'value': 'hockey', 'name': MSG(u"Hockey")},
    {'value': 'horse-riding', 'name': MSG(u"Horse Riding")},
    {'value': 'horse-racing', 'name': MSG(u"Horse Racing")},
    {'value': 'incentive', 'name': MSG(u"Incentive")},
    {'value': 'art-craft', 'name': MSG(u"Art & Craft")},
    {'value': 'island-hopping', 'name': MSG(u"Island Hopping")},
    {'value': 'language-tours', 'name': MSG(u"Language Tours")}] 


# Currencies

class Currency(Enumerate):

    options = [
    {'value': 'EURO', 'name': MSG(u"EUR")},
    {'value': 'Pound', 'name': MSG(u"GBP")},
    {'value': 'Dollar', 'name': MSG(u"USD")}
    ]


