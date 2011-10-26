# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@khine.net>

# Import from the Standard Library

# Import from itools
from itools.datatypes import String, Tokens, Unicode, URI
from itools.gettext import MSG
from itools.handlers import checkid
from itools.core import merge_dicts
from itools.csv import Property
from itools.uri import get_reference, get_uri_path
from itools.web import STLView, ERROR, INFO

# Import from ikaaro
from ikaaro.autoform import HiddenWidget, MultilineWidget, RadioWidget, SelectWidget, TextWidget
from ikaaro.buttons import Button, AddButton, RemoveButton
from ikaaro.messages import MSG_CHANGES_SAVED, MSG_NEW_RESOURCE
from ikaaro.messages import MSG_BAD_NAME
from ikaaro.registry import get_resource_class
from ikaaro.views import SearchForm
from ikaaro.views_new import NewInstance
from ikaaro.user import User

# Import from here
from tzm.buttons import RegionButton
from tzm.datatypes import Industry, BusinessSector, BusinessType
from tzm.messages import MSG_EXISTANT_CHAPTER, MSG_CHOOSE_REGION
from tzm.skins_views import TabsTemplate
from tzm.resource_views import RegionSelect, get_host_prefix
from tzm.datatypes import getCountries, getRegions, sort_key, getCounties


class Address_NewInstance(NewInstance):

    address_schema = {'city': String(mandatory=True),
                    'postcode': String(mandatory=True),
                    'company': String(mandatory=False),
                    'country': Unicode(mandatory=False),
                    'region': Unicode(mandatory=False),
                    'county': Unicode(mandatory=True),
                    }

    address_widgets = [
            TextWidget('city', title=MSG(u'City/Town'), size=35),
            TextWidget('postcode', title=MSG(u'Post Code'), size=10),
            RegionSelect('county', title=MSG(u'Country/Region/County'), has_empty_option = True),
            ]

    widgets = [
        MultilineWidget('title', title=MSG(u'Address'), default='', rows=3, cols=40)
        ] + address_widgets

    def get_schema(self, resource, context):
        schema = merge_dicts(NewInstance.schema,{'title': Unicode(mandatory=True)},
                            self.address_schema, {'vhosts': String})
                            
        return schema

    def GET(self, resource, context):
        county = context.get_form_value('county')
        if county is not None:
             if 'switch' in county.rsplit('#'):
                 context.message = MSG_CHOOSE_REGION
        return NewInstance.GET(self, resource, context)

    def action(self, resource, context, form):
        title = form['title']
        title = [ x.strip() for x in title.splitlines() ]
        title = [ x for x in title if x ]
        name = checkid(title[0])
        if name is None:
            raise FormError, messages.MSG_BAD_NAME
        vhosts = []
        # We add the default vhost entry for the address
        site_url = ('%s.%s.expert.travel' % (name, resource.name))
        vhosts.append(site_url)
        # Get the companies folder
        container = resource.get_resource('/companies')
        
        # Create the resource
        class_id = 'address'
        cls = get_resource_class(class_id)
        if resource.get_resource(name, soft=True) is not None:
            address = resource.get_resource(name, soft=True)
            # List addresses for this company
            return context.come_back(MSG_EXISTANT_CHAPTER)
        # we get the region or county
        county = form['county']
        if county is not None:
            if 'switch' in county.rsplit('#'):
                return self.GET
        address = resource.make_resource(name, cls)
        # The metadata
        metadata = address.metadata
        language = resource.get_edit_languages(context)[0]
        metadata.set_property('title', Property(title[0], lang=language))
        metadata.set_property('address', title[1:])
        metadata.set_property('postcode', form['postcode'])
        metadata.set_property('county', form['county'])
        metadata.set_property('vhosts', vhosts)
        metadata.set_property('website_is_open', 'community')
        # TODO we need to make this based on the URL of the 
        # site expert.travel or buildersmerchants.info
        # User id
        user = context.user
        # Remove user from old company
        addresses = user.get_address()
        if addresses:
            for x in addresses:
                resource.get_resource(x.abspath).set_user_role(user.name, None) 
        # Link the User to the newly created Address and make them the Branch Manager 
        default_role = address.class_roles[0]
        address.set_user_role(user.name, default_role)
        # Add the user to the expert.travel site as a 'Member'
        #root = context.resource.get_site_root()
        root = user.get_expert_site_root()
        if root:
            root.set_user_role(user.name, root.class_roles[1])
        # go to the user profile page
        goto = '/users/%s' % user.name
        return context.come_back(MSG_NEW_RESOURCE, goto=goto)
        
class View(STLView):
    access = True
    title = MSG(u'Welcome')
    template = 'ui/address/home.xml'
    styles = ['/ui/address/style.css']
    
    def get_namespace(self, resource, context):
        tabs = TabsTemplate(context)
        user = context.user
        if user is None:
            return {'info': None, 'tabs': tabs}
        home = '/users/%s' % user.name
        info = {'name': user.name, 
                'title': user.get_title(),
                'home': home}
        return {'info': info, 'tabs': tabs}
