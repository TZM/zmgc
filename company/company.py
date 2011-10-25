# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@abakuc.com>

# Import from itools
from itools.core import freeze, merge_dicts
from itools.datatypes import Tokens, Unicode
from itools.gettext import MSG

# Import form ikaaro
from ikaaro.folder import Folder
from ikaaro.registry import register_resource_class, register_document_type
from ikaaro.root import Root
from ikaaro.skins import UI, ui_path

# Import from tzm
from tzm.website import SiteRoot
from tzm.control_panel import CPEditBusinessSector, CPEditBusinessType
#
# Import from here
from views import Company_NewInstance, View
from address.address import Address


class Company(SiteRoot):
    
    class_id = 'company'
    class_title = MSG(u'Company virtual site')
    class_description = MSG(u'Adds a core company website.')
    class_icon16 = 'icons/16x16/website.png'
    class_icon48 = 'icons/48x48/website.png'
    class_views = Folder.class_views + ['control_panel']
    class_skin = 'ui/company'
    class_control_panel = ['browse_users', 'add_user', 'edit_virtual_hosts',
                            'edit_security_policy', 'edit_languages',
                            'edit_contact_options', 'broken_links', 'orphans',
                            'edit_industry', 'edit_business', 'edit_business_type']
                            
    class_roles = freeze(['company_manager', 'company_member'])
    class_schema = merge_dicts(
        SiteRoot.class_schema,
        {'company_manager': Tokens(source='metadata',
            title=MSG(u"Company Manager"))},
        {'company_member': Tokens(source='metadata',
            title=MSG(u"Company Member"))},
        #{'industry': Tokens(source='metadata',indexed=True, stored=True)},
        #{'business': Tokens(source='metadata',indexed=True, stored=True)},
        #{'type': Tokens(source='metadata',indexed=True, stored=True)},
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
        return [Address]

    ########################################################################
    ## UI
    ########################################################################
    view = View()
    # Industry view
    edit_business = CPEditBusinessSector()
    edit_business_type = CPEditBusinessType()
    new_instance = Company_NewInstance() 

class Companies(Folder):
    class_id = 'companies'
    class_version = '20090722'
    class_title = MSG(u'Companies folder')
    class_description = MSG(u'Companies container.')
    class_icon16 = 'icons/16x16/folder.png'
    class_icon48 = 'icons/48x48/folder.png'
    class_views = ['view', 'browse_content', 'preview_content', 'edit',
                   'last_changes']

    def get_document_types(self):
        return [Company]

# Register
register_document_type(Company, Root.class_id)
