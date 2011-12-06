# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@khine.net>

# Import from the Standard Library
from decimal import Decimal
from types import GeneratorType

# Import from itools
from itools.core import merge_dicts
from itools.datatypes import Tokens
from itools.gettext import MSG
from itools.html import stream_to_str_as_html, xhtml_doctype
from itools.web import STLView
from itools.xml import XMLParser

# Import from ikaaro
from ikaaro.control_panel import ControlPanel, CPAddUser, CPBrokenLinks
from ikaaro.control_panel import CPBrowseUsers, CPEditContactOptions, CPEditLanguages
from ikaaro.control_panel import CPEditMembership, CPEditSecurityPolicy
from ikaaro.control_panel import CPEditVirtualHosts, CPOrphans
from ikaaro.registry import register_resource_class, register_document_type
#from ikaaro.resource_views import LoginView as BaseLoginView
from ikaaro.skins import UI, ui_path
from ikaaro.text import CSS
from ikaaro.views_new import NewInstance
from ikaaro.webpage import WebPage
from ikaaro.website_views import AboutView, ContactForm, CreditsView
#from ikaaro.website_views import ForgottenPasswordForm, RegisterForm
from ikaaro.website_views import NotFoundView, ForbiddenView
from ikaaro.website import WebSite as BaseWebSite
from ikaaro.views import SearchForm

# Import from here 
from access import RoleAware
from control_panel import CPEditIndustry
from resource_views import Captcha, LoginView

class SiteRoot(BaseWebSite, RoleAware):
    class_schema = merge_dicts(
        BaseWebSite.class_schema,
        industry=Tokens(source='metadata', default=('',),indexed=True, stored=True),
        business=Tokens(source='metadata', default=('', ),indexed=True, stored=True),
        business_type=Tokens(source='metadata', default=('',),indexed=True, stored=True),
        )
    class_control_panel = BaseWebSite.class_control_panel
    class_theme = BaseWebSite.class_theme


    def _get_resource(self, name):
        if name == 'ui':
            ui = UI(ui_path)
            ui.database = self.metadata.database
            return ui
        if name in ('users', 'users.metadata'):
            return self.parent._get_resource(name)
        return BaseWebSite._get_resource(self, name)

    def _get_catalog_values(self):
        values = BaseWebSite._get_catalog_values(self)
        values['vhosts'] = self.get_property('vhosts')
        return values

    ########################################################################
    # API
    ########################################################################
    def before_traverse(self, context, min=Decimal('0.000001'),
                        zero=Decimal('0.0')):
        # Set the language cookie if specified by the query.
        # NOTE We do it this way, instead of through a specific action,
        # to avoid redirections.
        language = context.get_form_value('language')
        if language is not None:
            context.set_cookie('language', language)

        # The default language (give a minimum weight)
        accept = context.accept_language
        default = self.get_default_language()
        if accept.get(default, zero) < min:
            accept.set(default, min)
        # User Profile (2.0)
        user = context.user
        if user is not None:
            language = user.get_property('user_language')
            if language is not None:
                accept.set(language, 2.0)
        # Cookie (2.5)
        language = context.get_cookie('language')
        if language is not None:
            accept.set(language, 2.5)

    def get_skin(self, context):
        # Back-Office
        hostname = context.uri.authority
        if hostname[:3] in ['bo.', 'bo-']:
            return self.get_resource('/ui/aruni')
        # Fron-Office
        return self.get_resource(self.class_skin)

    def get_default_language(self):
        return self.get_property('website_languages')[0]

    def get_industry(self):
        return self.get_property('industry')

    #######################################################################
    # UI
    #######################################################################
    new_instance = NewInstance()
    # Control Panel
    #control_panel = ControlPanel()
    #browse_users = CPBrowseUsers()
    #add_user = CPAddUser()
    #edit_membership = CPEditMembership()
    #edit_virtual_hosts = CPEditVirtualHosts()
    #edit_security_policy = CPEditSecurityPolicy()
    #edit_contact_options = CPEditContactOptions()
    #edit_languages = CPEditLanguages()
    #broken_links = CPBrokenLinks()
    #orphans = CPOrphans()
    # Register / Login
    search = SearchForm()
    login = LoginView()
    captcha = Captcha()
    #register = RegisterForm()
    #forgotten_password = ForgottenPasswordForm()
    # Public views
    #contact = ContactForm()
    #about = AboutView()
    #credits = CreditsView()
    #license = STLView(access=True, title=MSG(u'License'),
    #                   template='/ui/root/license.xml')
    #
    # Calendar views

    # Industry views
    edit_industry = CPEditIndustry()

# Register
register_document_type(SiteRoot, SiteRoot.class_id)
