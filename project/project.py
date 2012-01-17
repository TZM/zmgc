# -*- coding: UTF-8 -*-
# Copyright (C) 2012 Norman Khine <norman@khine.net>
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
from itools.datatypes import Tokens
from itools.gettext import MSG

# Import form ikaaro
from ikaaro.folder import Folder
from ikaaro.registry import register_resource_class, register_document_type
from ikaaro.skins import UI, ui_path

# Import from tzm
from tzm.website import WebSite

# Import from here
from views import Project_NewInstance, View, ProjectsView


class Project(WebSite):
    
    class_id = 'project'
    class_title = MSG(u'Project virtual site')
    class_description = MSG(u'Adds a core project website.')
    class_icon16 = 'icons/16x16/website.png'
    class_icon48 = 'icons/48x48/website.png'
    class_views = Folder.class_views + ['control_panel']
    class_skin = 'ui/project'
    class_control_panel = WebSite.class_control_panel + [
                        'edit_industry', 'edit_business', 'edit_business_type']
                            
    class_schema = merge_dicts(
        WebSite.class_schema,
        )

    def _get_resource(self, name):
        if name == 'ui':
            ui = UI(ui_path)
            ui.database = self.metadata.database
            return ui
        # we need to get to the root
        root = self.get_root()
        if name in ('chapters', 'chapters.metadata'):
            return root._get_resource(name)
        if name in ('projects', 'projects.metadata'):
            return root._get_resource(name)
        if name in ('users', 'users.metadata'):
            return root._get_resource(name)
        return WebSite._get_resource(self, name)


    ########################################################################
    ## UI
    ########################################################################
    view = View()
    # Industry view
    new_instance = Project_NewInstance()

class Projects(Folder):
    class_id = 'projects'
    class_version = '20101112'
    class_title = MSG(u'Projects folder')
    class_description = MSG(u'Projects container.')
    class_icon16 = 'icons/16x16/folder.png'
    class_icon48 = 'icons/48x48/folder.png'
    class_views = Folder.class_views

    def get_document_types(self):
        return [Project]
    ########################################################################
    ## UI
    ########################################################################
    view = ProjectsView()

# Register
register_document_type(Project, Project.class_id)

