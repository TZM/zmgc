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
from abakuc.training.views import View



class Programme(SiteRoot):

    class_id = 'programme'
    class_title = MSG(u'Programme virtual site')
    class_description = MSG(u'Adds a training programme site.')
    class_icon16 = 'icons/16x16/website.png'
    class_icon48 = 'icons/48x48/website.png'
    class_views = Folder.class_views + ['control_panel']
    class_control_panel = ['browse_users', 'add_user', 'edit_virtual_hosts',
                           'edit_security_policy', 'edit_languages',
                           'edit_contact_options', 'broken_links', 'orphans']
    __roles__ = [
        {'name': 'training_managers', 'title':  MSG(u'Training Manager')},
        {'name': 'members', 'title':  MSG(u'Member')},
        {'name': 'partners', 'title':  MSG(u'Partner')},
        {'name': 'guests', 'title':  MSG(u'Guest')},
        ]

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


  #  #######################################################################
  #  # HTTP stuff
  #  #######################################################################
    #http_main = TrainingSkin()

  #  #######################################################################
  #  # UI
  #  #######################################################################
    view = View()

    #def get_document_types(self):
    #    return [Company]

# Register
register_resource_class(Programme)
register_document_type(Programme, Programme.class_id)

