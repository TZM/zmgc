# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@khine.net>

# Import from itools
from itools.core import freeze, merge_dicts
from itools.gettext import MSG
from itools.datatypes import String, Tokens, Unicode

# Import form ikaaro
from ikaaro.folder import Folder
from ikaaro.registry import register_resource_class, register_document_type
from ikaaro.skins import UI, ui_path

# Import from tzm
from tzm.website import SiteRoot 
#from tzm.skins import ChapterSkin 
#
# Import from here
from views import Address_NewInstance, View



class Address(SiteRoot):
    
    class_id = 'address'
    class_title = MSG(u'Address virtual site')
    class_description = MSG(u'Adds a core address website.')
    class_icon16 = 'icons/16x16/website.png'
    class_icon48 = 'icons/48x48/website.png'
    class_views = Folder.class_views + ['control_panel']
    class_skin = 'ui/address'
    class_control_panel = ['browse_users', 'add_user', 'edit_virtual_hosts',
                           'edit_security_policy', 'edit_languages',
                           'edit_contact_options', 'broken_links', 'orphans']


    class_roles = freeze(['branch_manager', 'branch_member', 'guest'])

    class_schema = merge_dicts(
        SiteRoot.class_schema,
        {'branch_manager': Tokens(source='metadata',
            title=MSG(u"Branch Manager"))},
        {'branch_member': Tokens(source='metadata',
            title=MSG(u"Branch Member"))},
        {'guest': Tokens(source='metadata',
            title=MSG(u"Guest"))},
        {'postcode': String(source='metadata',indexed=True, stored=True)},
        {'country': Unicode(source='metadata',indexed=True, stored=True)},
        {'region': Unicode(source='metadata',indexed=True, stored=True)},
        {'county': Unicode(source='metadata',indexed=True, stored=True)},
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
        return SiteRoot._get_resource(self, name)


    ########################################################################
    ## HTTP stuff
    ########################################################################
    #http_main = ChapterSkin()

    ########################################################################
    ## UI
    ########################################################################
    view = View()
    new_instance = Address_NewInstance()

    #def get_document_types(self):
    #    return [Company]

# Register
register_resource_class(Address)
register_document_type(Address, Address.class_id)
