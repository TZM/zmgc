# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@abakuc.com>

from json import dumps

# Import from itools
from itools.core import freeze
from itools.core import merge_dicts
from itools.database import AndQuery, OrQuery, PhraseQuery, StartQuery
from itools.datatypes import Boolean, String, Unicode, Integer
from itools.gettext import MSG
from itools.web import BaseView, ERROR, get_context, INFO, STLView
from itools.uri import get_reference

# Import from ikaaro
from ikaaro.autoform import PasswordWidget, SelectWidget, TextWidget
from ikaaro.messages import MSG_CHANGES_SAVED
from ikaaro.user_views import User_ConfirmRegistration, User_EditAccount, User_Profile
#from ikaaro.website_views import RegisterForm
from ikaaro.views import IconsView, SearchForm, ContextMenu
from ikaaro.utils import get_base_path_query

from datatypes import Functions, getCountries, getRegions, getCounties


# Import from here
from company.views import Company_NewInstance
from company.address.views import Address_NewInstance

class SiteUser_EditAccount(User_EditAccount):
    
    access = 'is_allowed_to_edit'
    title = MSG(u'Edit Account')
    description = MSG(u'Edit your name and email address.')
    schema = merge_dicts(
                User_EditAccount.schema,
                {'phone': Unicode,
                'mobile': Unicode,
                'functions': Functions(mandatory=True)})
    
    def get_widgets(self, resource, context):
        widgets = User_EditAccount.get_widgets(self, resource, context)
        extra_widgets = [TextWidget('phone', title=MSG(u"Phone number")),
                    TextWidget('mobile', title=MSG(u"Mobile")),
                    SelectWidget('functions', title=MSG(u"Job Function"),
                                    has_empty_option=False)]
        # We need to put the Password field at the end
        widgets[-1:-1]=list(extra_widgets)
        
        return widgets

    def get_value(self, resource, context, name, datatype):
        if name == 'password':
            return None
        if name == 'functions':
            return list(resource.get_property('functions'))
        if name == 'phone':
            return resource.get_property('phone')
        if name == 'mobile':
            return resource.get_property('mobile')
        return super(User_EditAccount, self).get_value(resource, context,
                    name, datatype)
        
    def action(self, resource, context, form):
        
        firstname = form['firstname']
        lastname = form['lastname']
        email = form['email']
        #job_function = tuple(form['job_function'])
        
        # Check password to confirm changes
        is_same_user = (resource.name == context.user.name)
        if is_same_user:
            password = form['password']
            if not resource.authenticate(password, clear=True):
                context.message = ERROR(
                    u"You mistyped your actual password, your account is"
                    u" not changed.")
                return
        # If the user changes his email, check there is not already other
        # user with the same email in the database.
        if email != resource.get_property('email'):
            results = context.root.search(email=email)
            if len(results):
                context.message = ERROR(
                    u'There is another user with the email "{email}", please'
                    u' try again.', email=email).gettext()
                return
            # Check email address has an MX record
            email_uri = 'mailto:'+email
            r1 = get_reference(email_uri)
            host = r1.host
            import dns.resolver
            from dns.exception import DNSException
            # Here we check to see if email host has an MX record
            try:
                # This may take long
                answers = dns.resolver.query(host, 'MX')
                print answers
            except DNSException, e:
                answers = None
            if not answers:
                context.message = ERROR(
                    u"The email supplied is invalid, your account"
                    u" has not been changed!")
                #return context.come_back(message, keep=keep)
                return
        # Save changes
        resource.set_property('firstname', firstname)
        resource.set_property('lastname', lastname)
        resource.set_property('email', email)
        resource.set_property('phone', form['phone'])
        resource.set_property('mobile', form['mobile'])
        resource.set_property('functions', (form['functions'],))
        # Ok
        context.message = MSG_CHANGES_SAVED

class SiteUser_Profile(User_Profile):
    def get_namespace(self, resource, context):
        root = context.root
        user = context.user
        ac = resource.get_access_control()
        # The icons menu
        items = []
        for name in ['edit_account', 'edit_preferences', 'edit_password',
                    'tasks', 'company', 'address']:
            # Get the view & check access rights
            view = resource.get_view(name)
            if view is None:
                continue
            if not ac.is_access_allowed(user, resource, view):
                continue
            # Append
            items.append({
                'url': ';%s' % name,
                'title': view.title,
                'description': getattr(view, 'description', None),
                'icon': resource.get_method_icon(view, size='48x48'),
            })

        # Ok
        is_owner = user is not None and user.name == resource.name
        return {
            'items': items,
            'is_owner_or_admin': is_owner or root.is_admin(user, resource),
            'user_must_confirm': resource.has_property('user_must_confirm')}
        
class SiteUser_ConfirmRegistration(User_ConfirmRegistration):

    def action(self, resource, context, form):
        must_confirm = resource.get_property('user_must_confirm')
        if form['key'] != must_confirm:
            context.message = messages.MSG_BAD_KEY
            return
        # Check passwords
        password = form['newpass']
        password2 = form['newpass2']
        if password != password2:
            context.message = messages.MSG_PASSWORD_MISMATCH
            return
        # Set user
        resource.set_password(password)
        resource.del_property('user_must_confirm')
        # Set cookie
        resource.set_auth_cookie(context, password)
        # Ok
        message = INFO(u'Operation successful! Welcome. Please setup your company details.')
        return context.come_back(message, goto='./;company')
    

class UserCompany(SearchForm):
    """
    Sets the user's company and address
    """
    access = 'is_allowed_to_edit'
    title = MSG(u'Company')
    description = MSG(u"User's company page.")
    icon = 'action_home.png'
    template = '/ui/abakuc/company.xml'
    
    schema = merge_dicts(Company_NewInstance.schema)

    search_schema = {
        'change_company': Boolean,
        'company': Unicode,
        'country': Unicode,
        'region': Unicode,
        'n_found': Integer,
        'found': Integer,
        }

    query_schema = freeze({
            'type': String,
            'name': String,
            'title': Unicode})
    
    scripts = ['/ui/abakuc/js/jquery.ui.autocomplete.js']

    def get_namespace(self, resource, context):
        display = None
        change_company = None
        items = None
        found = None
        n_found = None
        n_found_msg = None
        message = None
        new_company_form = None
        root = context.root
        user = context.user
        # check if user wants to swich company?
        change_company = context.query['change_company']
        # check if user is a member of an address and company
        companies = user.get_company()
        if not user.get_company():
            display = True
        # allow user to change their company
        if change_company:
            change_company = True
            display = True
        search_term = context.query['company'].strip()
        if search_term:
            display = True
            items = True
            found = []
            # Search
            search_query = PhraseQuery('format', 'company')
            # TODO fix the search so that it is more full proof
            search_query = AndQuery(search_query,
                            StartQuery('name', search_term.split()[0]))
            results = context.root.search(search_query)
            if results:
                for item in results.get_documents():
                    found.append({'name': item.name, 'title': item.title}) 
                n_found = len(found)
                if n_found == 1:
                    n_found_msg = 'company'
                else:
                    n_found_msg = 'companies'
                found.append({'name': 'create-new-company', 'title': 'Create new company'})
            else:
                found = None
                # get the new company form and display it
                new_company_form = Company_NewInstance().GET(resource, context)
                message = 'No companies found. Create your own:'
                #new_company_form = None
        else:
            if companies != ():
                items = []
                for company in companies:
                    items.append(company.name)
            
        return {'display': display,
                'items': items, 
                'found': found, 
                'change_company': change_company,
                'n_found': n_found,
                'n_found_msg': n_found_msg,
                'message': message,
                'new_company_form': new_company_form}

    def action(self, resource, context, form):
        return Company_NewInstance().action(resource, context, form)

class ListCompanyNames(BaseView):
    '''
    Return a JSONP list for the autocomplete. As a minimum we must have, the option:
    [{"id": "create-new-company", "value": "Create new company"}] 
    '''
    access = 'is_allowed_to_view'
    query_schema = {'term': String(mandatory=True)}

    def GET(self, resource, context):
        # Return a blank page
        context.set_content_type('text/plain')
        search_query = PhraseQuery('format', 'company')
        # TODO fix the search so that it is more full proof
        q = AndQuery(search_query,
                        StartQuery('name', context.query['term']))
        #q = StartQuery('name', context.query['term'])
        results = context.root.search(q)
        companies = []
        for result in results.get_documents():
            companies.append({'value': result.title, 'id': result.name})
        companies.append({'value': 'Create new company', 'id': 'create-new-company'})

        return dumps(companies)


class ListCompanyAddresses(BaseView):

    access = 'is_allowed_to_view'
    query_schema = {'company': String(mandatory=True)}

    def GET(self, resource, context):
        context.set_content_type('text/plain')
        company = context.query['company']
        if company:
            # we need to get the company base root
            container = resource.get_resource('/companies')
            if container.get_resource(company, soft=True) is not None:
                company_root = container.get_resource(company, soft=True)
                query = []
                query.append(PhraseQuery('format', 'address'))
                abspath = str(company_root.get_canonical_path())
                query.append(get_base_path_query(abspath))
                query = AndQuery(*query)
                results = get_context().root.search(query)
                # FIXME options dictionary is not sorted!
                norman = {}
                norman['addresses'] = [
                    {'name': x.name, 'title': x.title, 'postcode': x.postcode, 'county': x.county}
                    for x in results.get_documents() ]
                norman['addresses'].sort(key=lambda x: x['name'])
                print norman, 'norman'
                options = {}
                addresses = []
                for result in results.get_documents():
                    options[result.name] = result.title
                # we add a create new address option, this needs to be the last value
                options['aaaaa11111'] = 'Please choose an address'
                options['zzzzz99999-create-new-address'] = 'Create new address!'
                return dumps(options)


class ChooseRegion(BaseView):
    access = 'is_allowed_to_view'
    query_schema = {'iana_root_zone': String(mandatory=False), 'region': String(mandatory=False)}
    
    def GET(self, resource, context):
        context.set_content_type('text/plain')
        iana_root_zone = context.query['iana_root_zone']
        region = context.query['region']
        if iana_root_zone == '':
            countries = dumps(getCountries().get_options())
            return countries
        if iana_root_zone and region:
            return dumps(getCounties().get_options(iana_root_zone, region))
        elif iana_root_zone:
            counties = dumps(getRegions().get_options(iana_root_zone))
            return dumps(getRegions().get_options(iana_root_zone))
    
class UserAddress(STLView):
    """
    Sets the user's address
    """
    access = 'is_allowed_to_edit'
    title = MSG(u'Address')
    description = MSG(u"User's address page.")
    icon = 'action_home.png'
    template = '/ui/abakuc/address.xml'