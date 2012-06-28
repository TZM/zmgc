# -*- coding: UTF-8 -*-
# Copyright (C) 2011 Norman Khine <norman@khine.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Import from itools
from itools.gettext import MSG

# Import form ikaaro
from ikaaro.folder import Folder
from ikaaro.registry import register_document_type
from ikaaro.skins import UI, ui_path

# Import from tzm
from tzm.website import WebSite 
 
# Import from here
from views import View, ChapterGenerator, More
from tzm.resource_views import Captcha, Map


class Phoenix(WebSite):

    class_id = 'phoenix'
    class_title = MSG(u'Phoenix Site')
    class_description = MSG(u'Adds the core phoenix directory website.')
    class_icon16 = 'icons/16x16/website.png'
    class_icon48 = 'icons/48x48/website.png'
    class_views = Folder.class_views + ['control_panel']
    class_skin = 'ui/phoenix'
    class_control_panel = ['browse_users', 'add_user', 'edit_virtual_hosts',
        'edit_security_policy', 'edit_languages',
        'edit_contact_options', 'broken_links', 'orphans',
        'edit_seo', 'edit_theme', 'edit_industry',
        'create'
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
        if name in ('chapters', 'chapters.metadata'):
            return root._get_resource(name)
        if name in ('projects', 'projects.metadata'):
            return root._get_resource(name)
        if name in ('countries', 'countries.metadata'):
            return root._get_resource(name)
        return WebSite._get_resource(self, name)


    def get_document_types(self):
        return []

    ########################################################################
    # Views
    ########################################################################
    view = View()
    captcha = Captcha()
    create = ChapterGenerator()
    more = More()
    maps = Map()
    #site_search = Search_View()

#Register
register_document_type(Phoenix, Phoenix.class_id)
