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
from user_views import UserAddress, UserCompany, SiteUser_Profile
from user_views import ListCompanyNames, ListCompanyAddresses
from user_views import SiteUser_ConfirmRegistration, SiteUser_EditAccount
from user_views import ChooseRegion
from company import Company
from company.views import Company_NewInstance, Company_SearchForm
from company.address.views import Address_NewInstance 


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
    company = UserCompany()
    address = UserAddress()
    companies = ListCompanyNames()
    addresses = ListCompanyAddresses()
    # This needs to be called twice due to the AJAX form
    company_form = Company_NewInstance()
    address_form = Address_NewInstance()
    company_search_form = Company_SearchForm()
    unimatrix = ChooseRegion()

    def get_companies(self):
        root = self.get_root()
        if root is None:
            return ()
        results = root.search(format='company')
        items = [ x for x in results.get_documents() ]
        return tuple(items)

    def get_company(self):
        # a user can only be a member of one company
        # FIXME if a user is added manually to a Company or Address
        root = self.get_root()
        if root is None:
            return ()
        results = root.search(format='company', users=self.name)
        items = [ x for x in results.get_documents() ]

        return tuple(items)

    def get_address(self):
        root = self.get_root()
        if root is None:
            return ()
        results = root.search(format='address', users=self.name)
        items = [ x for x in results.get_documents() ]

        return tuple(items)

    def get_expert_site_root(self):
        root = self.get_root()
        if root is None:
            return ()
        results = root.search(format='expert')
        items = [ x for x in results.get_documents() ]
        return self.get_resource(items[0].abspath)

register_resource_class(SiteUser)
