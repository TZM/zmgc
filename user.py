# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@khine.net>

# Import from itools
from itools.core import freeze, merge_dicts
from itools.datatypes import String, Tokens, Unicode
from itools.gettext import MSG

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

register_resource_class(SiteUser)
