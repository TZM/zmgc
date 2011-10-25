# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@abakuc.com>

# Import from itools
from itools.core import freeze, get_abspath, merge_dicts
from itools.gettext import MSG
from itools.datatypes import Boolean, Email, Tokens, Unicode, String

# Import form ikaaro
from ikaaro.access import RoleAware
from ikaaro.folder import Folder
from ikaaro.registry import register_resource_class, register_document_type
from ikaaro.skins import register_skin, UI, ui_path
from ikaaro.website import WebSite

# Import from abakuc
from abakuc.website import SiteRoot 
 
# Import from here
from views import View
from abakuc.resource_views import Captcha


class Expert(SiteRoot):

    class_id = 'expert'
    class_title = MSG(u'Expert Site')
    class_description = MSG(u'Adds the core directory website.')
    class_icon16 = 'icons/16x16/website.png'
    class_icon48 = 'icons/48x48/website.png'
    class_views = Folder.class_views + ['control_panel']
    class_skin = 'ui/expert'
    class_control_panel = ['browse_users', 'add_user', 'edit_virtual_hosts',
        'edit_security_policy', 'edit_languages',
        'edit_contact_options', 'broken_links', 'orphans', 'edit_industry'
        ]

    __fixed_handlers__ = SiteRoot.__fixed_handlers__[:0] + ['404']

    def _get_resource(self, name):
        if name == 'ui':
            ui = UI(ui_path)
            ui.database = self.metadata.database
            return ui
        # we need to get to the root
        root = self.get_root()
        if name in ('users', 'users.metadata'):
            return root._get_resource(name)
        if name in ('companies', 'companies.metadata'):
            return root._get_resource(name)
        if name in ('countries', 'countries.metadata'):
            return root._get_resource(name)
        if name in ('training', 'training.metadata'):
            return root._get_resource(name)
        return SiteRoot._get_resource(self, name)


    def get_document_types(self):
        return []

    ########################################################################
    # Views
    ########################################################################
    view = View()
    captcha = Captcha()

#Register
register_resource_class(Expert)
register_document_type(Expert, Expert.class_id)
