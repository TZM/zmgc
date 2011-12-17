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
from itools.core import merge_dicts
from itools.datatypes import String
from itools.gettext import MSG
from itools.web import STLView

# Import from tzm
from tzm.skins_views import TabsTemplate
from tzm.resource_views import LoginView
from ikaaro.autoform import make_stl_template

# Import from chapter
from tzm.chapter import Chapter
from tzm.chapter.views import Chapter_NewInstance

class View(STLView):

    access = True
    title = MSG(u'Welcome')
    template = 'ui/phoenix/home.xml'
    styles = ['ui/phoenix/jquery/custom-theme/jquery-ui-1.8.16.custom.css', '/ui/core/css/jPlayer/jplayer.pink.flag.css']
    scripts = ['ui/phoenix/jquery/jquery-ui-1.8.16.custom.min.js', '/ui/core/js/jPlayer/jquery.jplayer.min.js', '/ui/core/js/jplayer.controls.js', ]


    def get_namespace(self, resource, context):
        tabs = TabsTemplate(context)
        #tabs = None 
        user = context.user

        if user is None:
            return {'info': None, 'tabs': tabs}

        home = '/users/%s' % user.name
        info = {'name': user.name, 'title': user.get_title(),
                'home': home}

        return {'info': info, 'tabs': tabs}


class ChapterGenerator(STLView):
    """
        Form which allows members to be able to add chapter sites that will be included
        in the main ZGC site.
    """
    access = 'is_allowed_to_view'
    title = MSG(u'Create your chapter')
    description = 'Create new chapter'
    template = 'ui/phoenix/chapter-generator.xml'
    query_schema = {'name': String, 'title': String, 'type': String, 'username': String}

    def get_namespace(self, resource, context):
        # options would be based on user's permissions
        user = context.user
        if user is None:
            form = LoginView().GET(resource, context)
            return {'name': None, 'form': form}
        
        #context.method = 'POST'
        #form = Chapter_NewInstance().GET(resource, context)
        form = make_stl_template("""Please follow this <a href="/chapters/;new_resource?type=chapter">
                                link</a> to create your chapter.""")
        firstname = user.get_property('firstname')
        if firstname:
            return {'name': firstname, 'form': form}
        return {'name': user.get_title(), 'form': form}