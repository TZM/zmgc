# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@abakuc.com>

# Import from itools
from itools.gettext import MSG

# Import form ikaaro
from ikaaro.folder import Folder
from ikaaro.registry import register_resource_class, register_document_type
from ikaaro.skins import UI, ui_path

# Import from abakuc
from abakuc.website import SiteRoot 
#from abakuc.skins import TrainingSkin 
#
# Import from here
from views import View
from programme.programme import Programme


class Training(SiteRoot):

    class_id = 'training'
    class_title = MSG(u'Training virtual site')
    class_description = MSG(u'Adds a core training website.')
    class_icon16 = 'icons/16x16/website.png'
    class_icon48 = 'icons/48x48/website.png'
    class_views = Folder.class_views + ['control_panel']
    class_control_panel = ['browse_users', 'add_user', 'edit_virtual_hosts',
    'edit_security_policy', 'edit_languages',
    'edit_contact_options', 'broken_links', 'orphans']

    class_roles = freeze(['training_managers', 'training_member', 'training_partner'])
    class_schema = merge_dicts(
        SiteRoot.class_schema,
        training_managers=Tokens(source='metadata', title=MSG(u"Training Manager")),
        training_member=Tokens(source='metadata', title=MSG(u"Training Member")),
        training_partner=Tokens(source='metadata', title=MSG(u"Training Partner")),
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
        if name in ('companies', 'companies.metadata'):
            return root._get_resource(name)
        return SiteRoot._get_resource(self, name)

    def get_document_types(self):
        return [Programme]

  #  #######################################################################
  #  # HTTP stuff
  #  #######################################################################
    #http_main = TrainingSkin()

  #  #######################################################################
  #  # UI
  #  #######################################################################
    view = View()

# Register
register_resource_class(Training)
register_document_type(Training, Training.class_id)

