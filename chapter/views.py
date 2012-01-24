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
#

# Import from the Standard Library


# Import from itools
from itools.datatypes import String, Tokens, Unicode, URI
from itools.gettext import MSG
from itools.handlers import checkid
from itools.core import freeze, merge_dicts
from itools.csv import Property
from itools.uri import get_reference, get_uri_path
from itools.web import STLView, ERROR, INFO, FormError
from itools.database import AndQuery, OrQuery, PhraseQuery, StartQuery
from itools.stl import stl


# Import from ikaaro
from ikaaro.autoform import RadioWidget, SelectWidget, TextWidget
from ikaaro.autoform import AutoForm, MultilineWidget
from ikaaro.blog import Blog
from ikaaro.calendar import Calendar
from ikaaro.messages import MSG_CHANGES_SAVED, MSG_NEW_RESOURCE
from ikaaro.messages import MSG_BAD_NAME
from ikaaro.registry import get_resource_class
from ikaaro.views import ContextMenu, CompositeForm, SearchForm, BrowseForm
from ikaaro.views_new import NewInstance
from ikaaro.folder import Folder
from ikaaro.folder_views import Folder_BrowseContent
from ikaaro.tracker import Tracker

# Import from Wiki
from wiki import WikiFolder

# Import from here
#from tzm.access import RoleAware
from tzm.datatypes import Industry, BusinessSector, BusinessType
from tzm.messages import MSG_EXISTANT_CHAPTER, MSG_CHOOSE_REGION
from tzm.messages import MSG_NEW_CHAPTER, MSG_EXISTING_CHAPTER_ADMIN
from tzm.resource_views import RegionSelect
from tzm.skins_views import TabsTemplate
from tzm.utils import fix_website_url, clean_website_url
from tzm.forums.forums import Forums

class Chapter_NewInstance(NewInstance):
    """
    Adding new Chapter site, check if User.id is not a manager of a chapter
    User.id can only manage one chapter, but can be a member of all.
    """
    access = 'is_allowed_to_create_chapter'
    schema = merge_dicts(NewInstance.schema,
            {'title': Unicode(mandatory=True),
            'vhosts': String,
            'country': String(mandatory=False),
            'region': String(mandatory=False),
            'county': String(mandatory=True),
            },)
    
    widgets = [
        TextWidget('title', title=MSG(u'Chapter Name'), default=''),
        TextWidget('vhosts', title=MSG(u'Chapter URL Address')),
        RegionSelect('county', title=MSG(u'Country/Region/County'), has_empty_option = True),
        ]

    def GET(self, resource, context):
        county = context.get_form_value('county')
        if county is not None:
             if 'switch' in county.rsplit('#'):
                 context.message = MSG_CHOOSE_REGION

        return NewInstance.GET(self, resource, context)

    def action(self, resource, context, form):
        # User id
        user = context.user
        # Check to see if the user is an Administrator for another chapter.
        user_get_chapters = user.get_chapters()
        # this returns a document
        # A user may be part of many chapters, we want to make sure
        # they are only administrators for one chapter.
        #for x in user.get_chapters():
        #    if user.name in x.get_members_classified_by_role()['admins']:
        #        # Give admin rights to a new member then proceed
        #        # otherwise the chapter may end up without an administrator
        #        # so we take the user to the browse user's interface.
        #        goto = '/chapters/%s/;browse_users' % x.name
        #        return context.come_back(MSG_EXISTING_CHAPTER_ADMIN, goto=goto)      
        title = form['title'].strip()
        name = form['name']
        name = checkid(title)
        if name is None:
            raise FormError, messages.MSG_BAD_NAME
        vhosts = []
        # We add the default vhost entry
        site_url = ('%s.zmgc.net' % name)
        vhosts.append(site_url)
        url = ('%s' % form['vhosts'])
        # XXX We need to check the domain name is valid
        vhosts.append(clean_website_url(url))
        vhosts = [ x for x in vhosts if x ]
        print vhosts
        # Create the resource
        class_id = 'chapter'
        cls = get_resource_class(class_id)
        container = resource.get_resource('/chapters')
        # check if name is taken
        if container.get_resource(name, soft=True) is not None:
            chapter = container.get_resource(name, soft=True)
            return context.come_back(MSG_EXISTANT_CHAPTER)
        # what if the form is all field, but thu user decides to change to different region?
        county = form['county']
        if county is not None:
            if 'switch' in county.rsplit('#'):
                return self.GET
        # We are now ready to make the chapter resource
        chapter = container.make_resource(name, cls)
        # The metadata
        metadata = chapter.metadata
        language = resource.get_edit_languages(context)[0]
        metadata.set_property('title', Property(title, lang=language))
        metadata.set_property('vhosts', vhosts)
        metadata.set_property('website_is_open', 'community')
        county = context.get_form_value('county').split('#')
        # set chapter location
        selected_region = context.get_form_value('county').split('#')
        metadata.set_property('country', selected_region[0])
        metadata.set_property('region', selected_region[1])
        metadata.set_property('county', selected_region[2])
        
        # Link the User to the newly created Chapter and make them the Administrator
        print chapter.class_roles[-1], 'chapter.class_roles[-1]'
        chapter.set_user_role(user.name, chapter.class_roles[-1])
        # Add the user to the Phoenix site as a 'Member'
        phoenix_site_root = user.get_phoenix_site_root()
        phoenix_site_root.set_user_role(user.name, phoenix_site_root.class_roles[1])
        
        # Now we add the forum, wiki specific for this chapter website.
        blog = chapter.make_resource('blog', Blog)
        calendar = chapter.make_resource('calendar', Calendar)
        forums = chapter.make_resource('forums', Forums)
        wiki = chapter.make_resource('wiki', WikiFolder)
        tracker = chapter.make_resource('tracker', Tracker)
        # TODO send an email with details
        email = user.get_property('email')
        print email
        #if email:
        #    user.send_chapter_confirmation(context, email, chapter)
        # FIXME: we want to take the member to the new site.
        goto = '/chapters/%s/;control_panel' % chapter.name
        return context.come_back(MSG_NEW_CHAPTER, goto=goto)


class Chapter_SearchForm(SearchForm):
    """
    Creates the Chapter Search Form
    """
    access = 'is_allowed_to_view'
    title = MSG(u'Chapter Search Form')
    description = MSG(u"Chapter search page.")
    icon = 'action_home.png'
    template = '/ui/core/templates/forms/chapter_search.xml'
    
    search_schema = {'chapter': Unicode}
    
    query_schema = freeze({
            'name': String,
            'title': Unicode})
    
    def get_namespace(self, resource, context):
        root = context.root
        found = None
        search_term = context.query['chapter'].strip()
        if search_term:
            found = []
            # Search
            search_query = PhraseQuery('format', 'chapter')
            # TODO fix the search so that it is more full proof
            search_query = AndQuery(search_query,
                            StartQuery('name', search_term.split()[0]))
            results = context.root.search(search_query)
            if results:
                for item in results.get_documents():
                    found.append({'name': item.name, 'title': item.title})
                n_found = len(found)
        
        return {'found': found}

class View(STLView):
    access = True
    title = MSG(u'Welcome')
    template = 'ui/chapter/home.xml'
    max_items_number = 1
    
    def get_max_items_number(self, resource, context):
        return self.max_items_number

    def sort_and_batch(self, resource, context, items):
        size = self.get_max_items_number(resource, context)
        return items
    
    def get_items_namespace(self, resource, context):
        vhosts = resource.get_property('vhosts')
        
        items = {}
        items['chapter_title'] = resource.get_property('title')
        items['chapter_description'] = resource.get_property('description')
        items['vhosts'] = resource.get_property('vhosts')
        
        return items
        
    
    def get_namespace(self, resource, context):
        tabs = TabsTemplate(context)
        user = context.user
        if user is None:
            info = None
        else:
            home = '/users/%s' % user.name
            info = {'name': user.name,
                'title': user.get_title(),
                'home': home}
        batch = None
        table = None
        # Batch
        chapters = self.get_items_namespace(resource, context)

        return merge_dicts(chapters, {'batch': batch, 'info': info, 'tabs': tabs})


class ChaptersView(STLView):
    access = True
    title = MSG(u'Chapters')
    template = '/ui/chapter/chapters.xml'