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
from itools.core import freeze, merge_dicts
from itools.datatypes import Tokens, Unicode, String
from itools.gettext import MSG

# Import form ikaaro
from ikaaro.folder import Folder
from ikaaro.registry import register_resource_class, register_document_type
from ikaaro.root import Root
from ikaaro.skins import UI, ui_path
from ikaaro.webpage import WebPage
from ikaaro.website import WebSite

# Import from tzm
from tzm.website import SiteRoot
from tzm.control_panel import CPEditBusinessSector, CPEditBusinessType
#
# Import from here
from views import Chapter_NewInstance, View

class Chapter(SiteRoot):
    
    class_id = 'chapter'
    class_title = MSG(u'Chapter virtual site')
    class_description = MSG(u'Adds a core chapter website.')
    class_icon16 = 'icons/16x16/website.png'
    class_icon48 = 'icons/48x48/website.png'
    class_views = Folder.class_views + ['control_panel']
    class_skin = 'ui/chapter'
    class_control_panel = SiteRoot.class_control_panel + [
                        'edit_industry', 'edit_business', 'edit_business_type']

    class_roles = freeze(['admin', 'member', 'guest'])
    class_schema = merge_dicts(
        SiteRoot.class_schema,
            {'country': String(source='metadata',indexed=True, stored=True)},
            {'region': String(source='metadata',indexed=True, stored=True)},
            {'county': String(source='metadata',indexed=True, stored=True)},
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
        if name in ('chapters', 'chapters.metadata'):
            return root._get_resource(name)
        return SiteRoot._get_resource(self, name)

    ########################################################################
    ## UI
    ########################################################################
    view = View()
    # Industry view
    edit_business = CPEditBusinessSector()
    edit_business_type = CPEditBusinessType()
    new_instance = Chapter_NewInstance() 

class Chapters(Folder):
    class_id = 'chapters'
    class_version = '20111120'
    class_title = MSG(u'Chapters folder')
    class_description = MSG(u'Chapters container.')
    class_icon16 = 'icons/16x16/folder.png'
    class_icon48 = 'icons/48x48/folder.png'
    class_views = ['view', 'browse_content', 'preview_content', 'edit',
                   'last_changes']

    def get_document_types(self):
        return [Chapter, WebSite]

# Register
register_document_type(Chapter, Root.class_id)
