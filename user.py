# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@khine.net>

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
        root = self.get_root()
        if root is None:
            return ()
        results = root.search(format='chapter')
        items = [ x for x in results.get_documents() ]
        return tuple(items)

    def get_phoenix_site_root(self):
        root = self.get_root()
        if root is None:
            return ()
        results = root.search(format='phoenix')
        items = [ x for x in results.get_documents() ]
        return self.get_resource(items[0].abspath)

    ########################################################################
    # Email: Chapter Creation
    ########################################################################
    
    confirmation_subject = MSG(u"Chapter {site_name} has been created.")
    confirmation_txt = MSG(u"This email confirms that your chapter {site_name} has been created."
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
        text = self.confirmation_txt.gettext(site_name=site_name,
                                             site_uri=site_uri,
                                             zgc_uri=fix_website_url(vhosts[0]),
                                             chapter_uri=fix_website_url(vhosts[1]))

        context.root.send_email(email, self.confirmation_subject.gettext(),
                                text=text)

register_resource_class(SiteUser)
