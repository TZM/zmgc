# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@abakuc.com>

# Import from itools
from itools.core import freeze, merge_dicts
from itools.datatypes import Tokens
from itools.gettext import MSG

# Import form ikaaro
from ikaaro.folder import Folder
from ikaaro.registry import register_resource_class, register_document_type
from ikaaro.skins import UI, ui_path

# Import from abakuc
from abakuc.website import SiteRoot

# Import from here
from views import Country_NewInstance, ImportCountries, View
#from address.address import Address


class Country(SiteRoot):
    
    class_id = 'country'
    class_title = MSG(u'Country virtual site')
    class_description = MSG(u'Adds a core country website.')
    class_icon16 = 'icons/16x16/website.png'
    class_icon48 = 'icons/48x48/website.png'
    class_views = Folder.class_views + ['control_panel']
    class_skin = 'ui/country'
    class_control_panel = ['browse_users', 'add_user', 'edit_virtual_hosts',
                            'edit_security_policy', 'edit_languages',
                            'edit_contact_options', 'broken_links', 'orphans',
                            'edit_business_type']
                            
    class_roles = freeze(['country_manager', 'country_member'])
    class_schema = merge_dicts(
        SiteRoot.class_schema,
        {'country_manager': Tokens(source='metadata',
            title=MSG(u"Country Manager"))},
        {'country_member': Tokens(source='metadata',
            title=MSG(u"Country Member"))},
        )

    def _get_resource(self, name):
        if name == 'ui':
            ui = UI(ui_path)
            ui.database = self.metadata.database
            return ui
        # we need to get to the root
        root = self.get_root()
        if name in ('users', 'users.metadata'):
            return root._get_resource(name)
        if name in ('training', 'training.metadata'):
            return root._get_resource(name)
        return SiteRoot._get_resource(self, name)

    def get_document_types(self):
        return [Region]

    ########################################################################
    ## UI
    ########################################################################
    view = View()
    # Industry view
    new_instance = Country_NewInstance()

class Countries(Folder):
    class_id = 'countries'
    class_version = '20101112'
    class_title = MSG(u'Countries folder')
    class_description = MSG(u'Countries container.')
    class_icon16 = 'icons/16x16/folder.png'
    class_icon48 = 'icons/48x48/folder.png'
    class_views = Folder.class_views + ['import_countries']

    def get_document_types(self):
        return [Country]

    
    ########################################################################
    ## UI
    ########################################################################
    import_countries = ImportCountries() 
# Register
register_document_type(Country, Country.class_id)

