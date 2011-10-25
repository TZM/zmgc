# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@abakuc.com>

# Import from the Standard Library

# Import from itools
from itools.csv import CSVFile
from itools.gettext import MSG
from itools.core import get_abspath
from itools.datatypes import Integer, String, Unicode

# Import from ikaaro
from ikaaro.folder_views import Folder_BrowseContent
from ikaaro.registry import register_resource_class
from ikaaro.revisions_views import DBResource_CommitLog
from ikaaro.root import Root as BaseRoot
from ikaaro.text import CSV

# Import from tzm
from company.company import Companies
from expert.expert import Expert
#from training.training import Training
from country.country import Countries

###########################################################################
# Resource
###########################################################################

class Affiliations(CSV):
    
    class_id = 'affiliations'
    def init_resource(self):
        super(Affiliations, self).init_resource()
        path =  get_abspath('data/affiliations.csv')
        self.handler.load_state_from_uri(path)

class Industry(CSV):
    
    class_id = 'industry'
    def init_resource(self):
        super(Industry, self).init_resource()
        path = get_abspath('data/industry.csv')
        self.handler.load_state_from_uri(path)

class Topics(CSV):
    
    class_id = 'topics'
    def init_resource(self):
        super(Topics, self).init_resource()
        path =  get_abspath('data/topics.csv')
        self.handler.load_state_from_uri(path)

class Types(CSV):
    
    class_id = 'types'
    def init_resource(self):
        super(Types, self).init_resource()
        path = get_abspath('data/types.csv')
        self.handler.load_state_from_uri(path)

class Functions(CSV):
    
    class_id = 'functions'
    def init_resource(self):
        super(Functions, self).init_resource()
        path =  get_abspath('data/functions.csv')
        self.handler.load_state_from_uri(path)

class World(CSV):
    
    class_id = 'world'
    class_csv_guess = True
    def init_resource(self):
        super(World, self).init_resource()
        path =  get_abspath('data/countries.csv')
        self.handler.load_state_from_uri(path)


class Root(BaseRoot):
    
    class_id = 'tzm'
    class_version = '20090606'
    class_title = MSG(u'Zeitgeist Application Server')
    class_description = MSG(u'One back-office to bring them all and in the'
                            u' darkness bind them, in an'
                            u' anarchically scalable information system.')
    def init_resource(self, email, password, admins=('0',)):
        super(Root, self).init_resource(email, password, admins=admins)
        affiliations = self.make_resource('affiliations', Affiliations)
        industry = self.make_resource('industry', Industry)
        topics = self.make_resource('topics', Topics)
        types = self.make_resource('types', Types)
        functions = self.make_resource('functions', Functions)
        world = self.make_resource('world', World)
        # Add the expert travel website - http://expert.travel
        # Expert Travel
        hosts = ['uk.expert_travel', 'fr.expert_travel']
        expert = self.make_resource('expert', Expert,
            title={'en': u'Expert Travel'},
            website_is_open='community',
            website_languages=('en', 'fr'),
            vhosts=hosts,
            description={'en':u'One back-office to bring them all and in the'
                      u' darkness bind them, in an'
                      u' anarchically scalable information system.'},
            industry=('travel',)
            )
        # Add the companies folder - here we store the company objects
        companies = self.make_resource('companies', Companies,
                                        title={'en': u'Companies'},
                                        description={'en': u'Companies folder'})
        
        ### Add the http://destinationsguide.info web site - dispaly all countries
        #hosts = ['destinationsguide.info', 'destinationsguide_info']
        #destinationsguide_info = self.make_resource('destinationsguide', Expert,
        #       title={'en': u'Destinations Guide'},
        #       vhosts=['destinationsguide.info', 'destinationsguide_info'],
        #       website_is_open=True,
        #       website_languages=('en', 'fr'),
        #       description={'en':u'Destinations guide, part of the Abakuc Application'
        #                       u' Server information system.'}
        #           )
        # Add the countries folder - here we store the country objects
        countries = self.make_resource('countries', Countries, title={'en': u'Countries'},
            description={'en': u'Countries folder'})
        ## Add the http://traveluniversity.net - here we list all the training sites.
        #hosts = ['traveluniversity.net', 'traveluniversity_net']
        #traveluniversity_net = self.make_resource('training', Training, title={'en': u'Training'},
        #   vhosts=hosts, website_is_open=True,
        #   website_languages=('en', 'fr'),
        #   description={'en':u'Training, part of the Abakuc Application'
        #             u' Server information system.'})
        ### Add the training folder, here we store all the training sub-site objects
        ##training = Folder.build_metadata(title={'en': u'Training Folder'},
        ##      description={'en': u'Expert.Travel folder containing'
        ##                u' training applications based on business function.'})
        ##folder.set_handler('training.metadata', training)
        ### Add the http://riverguides.info site - list all rivers
        ##hosts = ('riverguides.info', 'riverguides_info')
        ##riverguides_info = BaseSiteRoot.build_metadata(title={'en': u'River Guides'},
        ##      vhosts=hosts, website_is_open=True,
        ##      website_languages=('en', 'fr'),
        ##      description={'en':u'River guides, part of the Abakuc Application'
        ##                u' Server information system.'})
        ##folder.set_handler('riverguides.metadata', riverguides_info)
        ### Add the rivers folder - here we store the river objects
        ##rivers = Folder.build_metadata(title={'en': u'Rivers Folder'},
        ##      description={'en': u'Expert.Travel folder containing'
        ##                u' river objects, to be listed in the riverguides.'})
        ##folder.set_handler('rivers.metadata', rivers)
    
    ########################################################################
    # API
    ########################################################################
    def get_page_title(self):
        return None
    
    def get_document_types(self):
        return BaseRoot.get_document_types(self) + [BaseRoot]
    
    # Restrict access to the folder's views
    browse_content = Folder_BrowseContent(access='is_allowed_to_edit')
    last_changes = DBResource_CommitLog(access='is_allowed_to_edit')

###########################################################################
# Register
###########################################################################
register_resource_class(Root)
