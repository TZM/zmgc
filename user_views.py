# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@khine.net>

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
from chapter.views import Chapter_NewInstance

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
            # By pass this check if working on local machine
            hostname = context.uri.authority
            if hostname.split('.')[-1] != 'local':
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
                    'tasks', 'chapter']:
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
        message = INFO(u'Operation successful! Welcome. Please setup your chapter details.')
        return context.come_back(message, goto='./;chapter')
    

class UserChapter(SearchForm):
    """
    Sets the user's chapter page
    """
    access = 'is_allowed_to_edit'
    title = MSG(u'Chapter')
    description = MSG(u"User's chapter page.")
    icon = 'action_home.png'
    template = '/ui/zeitgeist/chapter.xml'
    
    schema = merge_dicts(Chapter_NewInstance.schema)

    search_schema = {
        'change_chapter': Boolean,
        'chapter': Unicode,
        'country': Unicode,
        'region': Unicode,
        'n_found': Integer,
        'found': Integer,
        }

    query_schema = freeze({
            'type': String,
            'name': String,
            'title': Unicode})
    
    scripts = ['/ui/zeitgeist/js/jquery.ui.autocomplete.js']

    def get_namespace(self, resource, context):
        display = None
        change_company = None
        items = None
        found = None
        n_found = None
        n_found_msg = None
        message = None
        new_chapter_form = None
        root = context.root
        user = context.user
        # check if user wants to swich company?
        change_company = context.query['change_chapter']
        # check if user is a member of a chapter
        chapters = user.get_chapter()
        if not user.get_chapter():
            display = True
        # allow user to change their chapter
        if change_chapter:
            change_chapter = True
            display = True
        search_term = context.query['chapter'].strip()
        if search_term:
            display = True
            items = True
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
                if n_found == 1:
                    n_found_msg = 'cohapter'
                else:
                    n_found_msg = 'chapters'
                found.append({'name': 'create-new-chapter', 'title': 'Create new chapter'})
            else:
                found = None
                # get the new chapter form and display it
                new_chapter_form = Chapter_NewInstance().GET(resource, context)
                message = 'No chapters found. Create your own:'
        else:
            if chapters != ():
                items = []
                for chapter in chapters:
                    items.append(chapter.name)
            
        return {'display': display,
                'items': items, 
                'found': found, 
                'change_company': change_company,
                'n_found': n_found,
                'n_found_msg': n_found_msg,
                'message': message,
                'new_chapter_form': new_chapter_form}

    def action(self, resource, context, form):
        return Chapter_NewInstance().action(resource, context, form)

class ListChapterNames(BaseView):
    '''
    Return a JSONP list for the autocomplete. As a minimum we must have, the option:
    [{"id": "create-new-chapter", "value": "Create new chapter"}] 
    '''
    access = 'is_allowed_to_view'
    query_schema = {'term': String(mandatory=True)}

    def GET(self, resource, context):
        # Return a blank page
        context.set_content_type('text/plain')
        search_query = PhraseQuery('format', 'chapter')
        # TODO fix the search so that it is more full proof
        q = AndQuery(search_query,
                        StartQuery('name', context.query['term']))
        #q = StartQuery('name', context.query['term'])
        results = context.root.search(q)
        chapters = []
        for result in results.get_documents():
            companies.append({'value': result.title, 'id': result.name})
        companies.append({'value': 'Create new chapter', 'id': 'create-new-chapter'})

        return dumps(chapters)


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
