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


# Import from the Standard Library

# Import from itools
from itools.datatypes import Integer, String, Tokens, Unicode, URI
from itools.gettext import MSG
from itools.handlers import checkid
from itools.core import get_abspath, merge_dicts
from itools.csv import Property
from itools.uri import get_reference, get_uri_path
from itools.web import STLView

# Import from ikaaro
from ikaaro.autoform import TextWidget
from ikaaro.messages import MSG_CHANGES_SAVED, MSG_NEW_RESOURCE
from ikaaro.messages import MSG_BAD_NAME
from ikaaro.registry import get_resource_class
from ikaaro.views_new import NewInstance
from ikaaro.folder import Folder
from ikaaro.website import WebSite

# Import from here
from tzm.messages import MSG_EXISTANT_PROJECT


class Project_NewInstance(NewInstance):
    
    access = 'is_allowed_to_view'
    schema = merge_dicts(NewInstance.schema,
            {'vhosts': String})
    widgets = [
        TextWidget('title', title=MSG(u'Project Name'), default=''),
        TextWidget('vhosts', title=MSG(u'Project URL Address')),
        ]

    def GET(self, resource, context):
        return NewInstance.GET(self, resource, context)
        
    def action(self, resource, context, form):
        title = form['title'].strip()
        name = form['name']
        name = checkid(title)
        if name is None:
            raise FormError, messages.MSG_BAD_NAME
        vhosts = []
        # We add the default vhost entry
        site_url = ('%s.projects.zmgc.net' % name)
        vhosts.append(site_url) 
        url = ('%s' % form['vhosts'])
        # XXX We need to check the domain name is valid
        vhosts.append(url)
        vhosts = [ x for x in vhosts if x ]
        
        # Create the resource
        class_id = 'project'
        cls = get_resource_class(class_id)
        container = resource.get_resource('/projects')
        # check if name is taken
        if container.get_resource(name, soft=True) is not None:
            item = container.get_resource(name, soft=True)
            return context.come_back(MSG_EXISTANT_PROJECT)
        item = container.make_resource(name, cls)
        # The metadata
        metadata = item.metadata
        language = resource.get_edit_languages(context)[0]
        metadata.set_property('title', Property(title, lang=language))
        metadata.set_property('vhosts', vhosts)
        metadata.set_property('website_is_open', 'community')
        # TODO we need to make this based on the URL of the 

        # go to the user's profile page
        goto = '/projects/%s' % item.name
        return context.come_back(MSG_NEW_RESOURCE, goto=goto)

class View(STLView):
    access = True
    title = MSG(u'Welcome')
    template = '/ui/project/home.xml'
    
    def get_namespace(self, resource, context):
        user = context.user
        if user is None:
            return {'info': None}
        home = '/users/%s' % user.name
        info = {'name': user.name, 
                'title': user.get_title(),
                'home': home}
        return {'info': info}
        
class ProjectsView(STLView):
    access = True
    title = MSG(u'Projects view page')
    template = '/ui/project/projects.xml'
    
    def get_namespace(self, resource, context):
        user = context.user
        if user is None:
            return {'info': None}
        home = '/users/%s' % user.name
        info = {'name': user.name, 
                'title': user.get_title(),
                'home': home}
        return {'info': info}
