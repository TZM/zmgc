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
from itools.datatypes import String, Tokens, Unicode
from itools.gettext import MSG
from itools.uri import Reference

# Import from ikaaro
from ikaaro.folder_views import GoToSpecificDocument
from ikaaro.registry import register_resource_class
from ikaaro.user import User

# Import from project
from datatypes import Functions
from user_views import UserChapter, SiteUser_Profile
from user_views import ListChapterNames
from user_views import SiteUser_ConfirmRegistration, SiteUser_EditAccount
from user_views import ChooseRegion
from chapter import Chapter
from chapter.views import Chapter_NewInstance, Chapter_SearchForm
from utils import fix_website_url


class SiteUser(User):
    class_views = ['profile', 'edit_account', 'my_threads',
                    'edit_preferences', 'edit_password', 
                    'company', 'address']
    class_schema = merge_dicts(User.class_schema,  
                mobile=Unicode(source='metadata', indexed=True, stored=True),
                phone=Unicode(source='metadata', indexed=True, stored=True),
                country=Tokens(source='metadata', default=('', )),
                functions=Tokens(source='metadata', default=('', )))
    class_schema = freeze(class_schema)
    # Views
    profile = SiteUser_Profile()
    edit_account = SiteUser_EditAccount()
    confirm_registration = SiteUser_ConfirmRegistration()
    my_threads = None
    chapters = ListChapterNames()
    chapter_form = Chapter_NewInstance()
    unimatrix = ChooseRegion()

    def get_chapters(self):
        """
            returns a tuple of the chapters that this user is a member of
        """
        root = self.get_root()
        if root is None:
            return ()
        results = root.search(format='chapter',  users=self.name)
        items = [ x for x in results.get_documents() ]
        chapters = []
        for x in items:
            chapters.append(self.get_resource(x.abspath))

        return tuple(chapters)

    def get_phoenix_site_root(self):
        root = self.get_root()
        if root is None:
            return ()
        results = root.search(format='phoenix')
        items = [ x for x in results.get_documents() ]
        return self.get_resource(items[0].abspath)

    def get_firstname(self):
        firstname = self.get_title().split()[0]
        if firstname:
            return firstname.decode('utf-8')
        return self.get_login_name().decode('utf-8')
    
    ########################################################################
    # Email: Chapter Creation
    ########################################################################
    
    chapter_confirmation_subject = MSG(u"Chapter {site_name} has been created.")
    chapter_confirmation_txt = MSG(u"This email confirms that your chapter {site_name} has been created."
                           u"\n"
                           u"\nPlease visit the documentation link. {site_uri}docs/chapter"
                           u"\nWe have created a domain URL for you {zgc_uri} in addition to your own URL"
                           u" {chapter_uri}"
                           u"\n"
                           u"Phoenix Team")

    def send_chapter_confirmation(self, context, email, chapter):
        site_name = chapter.get_title()
        uri = context.uri
        vhosts = chapter.get_property('vhosts')
        site_uri = Reference(uri.scheme, uri.authority, '/', {}, None)
        text = self.chapter_confirmation_txt.gettext(site_name=site_name,
                                             site_uri=site_uri,
                                             zgc_uri=fix_website_url(vhosts[0]),
                                             chapter_uri=fix_website_url(vhosts[1]))

        context.root.send_email(email, self.chapter_confirmation_subject.gettext(site_name=site_name),
                                text=text)

register_resource_class(SiteUser)
