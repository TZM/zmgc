# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@abakuc.com>

# Import from the Standard Library

# Import from itools
from itools.csv import CSVFile
from itools.datatypes import Integer, String, Tokens, Unicode, URI
from itools.gettext import MSG
from itools.handlers import RWDatabase, ro_database, checkid
from itools.core import get_abspath, merge_dicts
from itools.csv import Property
from itools.uri import get_reference, get_uri_path
from itools.web import STLView, STLForm

# Import from ikaaro
from ikaaro.autoform import RadioWidget, SelectWidget, TextWidget
from ikaaro.autoform import AutoForm, MultilineWidget
from ikaaro.messages import MSG_CHANGES_SAVED, MSG_NEW_RESOURCE
from ikaaro.messages import MSG_BAD_NAME
from ikaaro.registry import get_resource_class
from ikaaro.views import ContextMenu, CompositeForm
from ikaaro.views_new import NewInstance
from ikaaro.folder import Folder
from ikaaro.website import WebSite

# Import from here
from abakuc.messages import MSG_EXISTANT_COMPANY
from abakuc.skins_views import TabsTemplate
from abakuc.datatypes import World, getCountries, getRegions, getCounties
from abakuc.resource_views import RegionSelect


class Country_NewInstance(NewInstance):
    
    schema = merge_dicts(NewInstance.schema,
            {'vhosts': String, 'rselect': String})
    widgets = [
        TextWidget('title', title=MSG(u'Country Name'), default=''),
        TextWidget('vhosts', title=MSG(u'Country URL Address')),
        RegionSelect('rselect', title=MSG(u'Region/Country'))
        ]

    def GET(self, resource, context):
        path = get_uri_path(context.uri)
        if path.endswith(';country_form'):
            context.set_content_type('text/html')
        return NewInstance.GET(self, resource, context)
        
    def action(self, resource, context, form):
        title = form['title'].strip()
        name = form['name']
        name = checkid(title)
        if name is None:
            raise FormError, messages.MSG_BAD_NAME
        vhosts = []
        # We add the default vhost entry
        site_url = ('%s.destinationsguide.info' % name)
        vhosts.append(site_url) 
        url = ('%s' % form['vhosts'])
        # XXX We need to check the domain name is valid
        vhosts.append(url)
        vhosts = [ x for x in vhosts if x ]
        
        # Create the resource
        class_id = 'country'
        cls = get_resource_class(class_id)
        container = resource.get_resource('/countries')
        # check if name is taken
        if container.get_resource(name, soft=True) is not None:
            item = container.get_resource(name, soft=True)
            # List addresses for this company
            return context.come_back(MSG_EXISTANT_COMPANY)
        item = container.make_resource(name, cls)
        # The metadata
        metadata = item.metadata
        language = resource.get_edit_languages(context)[0]
        metadata.set_property('title', Property(title, lang=language))
        metadata.set_property('vhosts', vhosts)
        metadata.set_property('website_is_open', 'community')
        # TODO we need to make this based on the URL of the 

        # go to the user's profile page
        goto = '/countries/%s' % item.name
        return context.come_back(MSG_NEW_RESOURCE, goto=goto)

class ImportCountries(STLForm):
    access = 'is_admin'
    title = MSG(u'Import countries')
    template = '/ui/abakuc/import.xml'

    def get_namespace(self, resource, context):
        country = 'fr'
        region = 'languedoc-roussillon'
        list_countries = getCounties().get_options(country, region)
        print len(list_countries)
        for x in list_countries:
            print x
        
    def action(self, resource, context, form):
        # For each country, region and county we create a website
        country_class_id = 'country'
        rw_database = RWDatabase()
        csv = rw_database.get_handler(get_abspath('/Users/khinester/lib/python2.6/site-packages/abakuc/data/countries_austria_full.csv'), World)
        rows = csv.get_rows()
        list_countries = set()
        # List countries and its regions
        for row in rows:
            country = row.get_value('country')
            iana_root_zone = row.get_value('iana_root_zone')
            name = checkid(country)
            list_countries.add((name, country, iana_root_zone))
        list_countries = sorted(list_countries)
        from country import Country
        print len(list_countries)
        for x in list_countries[233:235]:
            hosts = []
            hosts.append('%s.destinationsguide.info' % x[2])
            hosts.append('%s.destinationsguide.info' % x[0])
            title = u'%s' % x[1]
            # TODO pull the country description from
            # http://www.worldtravelguide.net use urllib2 and BeautifulSoup
            country = resource.make_resource(x[0], 
                Country, 
                title={'en': title},
                website_is_open='community',
                website_languages=('en', 'fr'),
                vhosts=hosts,
                description={'en':u'Country description'},
                #industry=('travel',)
                )
            # Add the Region sites
            regions = set()
            rows = csv.get_rows()
            for row in rows:
                if row[5] == x[2]:
                    if row[7] != u'none':
                        regions.add(row[7])
            if regions:
                for y in sorted(regions):
                    name = checkid(y)
                    hosts = '%s.%s.destinationsguide.info' % (x[2], name)
                    title = u'%s' % y
                    region = country.make_resource(name, WebSite, title={'en': title},
                    website_is_open='community',
                    website_languages=('en', 'fr'),
                    vhosts=hosts,
                    description={'en':u'Region description'},
                    #industry=('travel',)
                    )
                    # Add the County sites
                    print y, 'REGION'
                    rows = csv.get_rows()
                    counties = set()
                    for row in rows:
                        if row[7] == y:
                            if row[8] != u'none':
                                print row[8], 'COUNTY'
                                counties.add(row[8])
                    if counties:
                        print counties
                        for county in sorted(counties):
                            county_name = checkid(county)
                            print x[2], county_name
                            hosts = []
                            hosts.append('%s.destinationsguide.info' % checkid(row[8]))
                            #hosts.append('%s.%s.destinationsguide.info' % checkid(row[8]), checkid(row[7]))
                            #hosts.append('%s.destinationsguide.info' % x[0])
                            county = region.make_resource(county_name, WebSite, title={'en': county},
                                                website_is_open='community',
                                                website_languages=('en', 'fr'),
                                                vhosts=hosts,
                                                description={'en':u'Region description'},
                                                #industry=('travel',)
                                                )
                    
                    #counties.add()
class View(STLView):
    access = True
    title = MSG(u'Welcome')
    template = 'ui/country/home.xml'
    
    def get_namespace(self, resource, context):
        tabs = TabsTemplate(context)
        user = context.user
        if user is None:
            return {'info': None, 'tabs': tabs}
        home = '/users/%s' % user.name
        info = {'name': user.name, 
                'title': user.get_title(),
                'home': home}
        return {'info': info, 'tabs': tabs}
