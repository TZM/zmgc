# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@khine.net>

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
from ikaaro.messages import MSG_CHANGES_SAVED, MSG_NEW_RESOURCE
from ikaaro.messages import MSG_BAD_NAME
from ikaaro.registry import get_resource_class
from ikaaro.views import ContextMenu, CompositeForm, SearchForm, BrowseForm
from ikaaro.views_new import NewInstance
from ikaaro.folder import Folder
from ikaaro.folder_views import Folder_BrowseContent

# Import from here
from tzm.datatypes import Industry, BusinessSector, BusinessType
from tzm.messages import MSG_EXISTANT_CHAPTER, MSG_CHOOSE_REGION
from tzm.skins_views import TabsTemplate
from tzm.utils import fix_website_url
from tzm.company.address.views import Address_NewInstance
#from tzm.datatypes import getCountries, getRegions, sort_key, getCounties

class Company_NewInstance(NewInstance):
    """
    When adding a new company, we always have to add an address.
    """
    access = 'is_allowed_to_view'
    schema = merge_dicts(NewInstance.schema,
            {'title': Unicode(mandatory=True),
            'vhosts': String,
            'industry': Tokens,
            'business': BusinessSector(multiple=True, mandatory=True),
            'business_type': BusinessType(multiple=True, mandatory=True, selected=False),
            'address': Unicode(mandatory=True),
            }, Address_NewInstance.address_schema)
    
    widgets = [
        TextWidget('title', title=MSG(u'Company Name'), default=''),
        TextWidget('vhosts', title=MSG(u'Company URL Address')),
        SelectWidget('business', title=MSG(u'Business Sector'), has_empty_option=False, size=4),
        RadioWidget('business_type', title=MSG(u'Business Type'), oneline=True, has_empty_option=False),
        MultilineWidget('address', title=MSG(u'Address'), default='', rows=3, cols=40)
        ] + Address_NewInstance.address_widgets

    def GET(self, resource, context):
        county = context.get_form_value('county')
        if county is not None:
             if 'switch' in county.rsplit('#'):
                 context.message = MSG_CHOOSE_REGION
        return NewInstance.GET(self, resource, context)

    #def on_form_error(self, resource, context):
    #    county = context.get_form_value('county')
    #    if county is not None:
    #        if 'switch' in county.rsplit('#'):
    #            print 'we choose region after county'
    #            context.message = INFO(u'Please choose your Region')
    #            return self.GET
    #    return self.GET

    def action(self, resource, context, form):
        title = form['title'].strip()
        name = form['name']
        name = checkid(title)
        if name is None:
            raise FormError, messages.MSG_BAD_NAME
        vhosts = []
        # We add the default vhost entry
        site_url = ('%s.expert.travel' % name)
        vhosts.append(site_url)
        url = ('%s' % form['vhosts'])
        # XXX We need to check the domain name is valid
        vhosts.append(url)
        vhosts = [ x for x in vhosts if x ]
        
        # Create the resource
        class_id = 'company'
        cls = get_resource_class(class_id)
        container = resource.get_resource('/companies')
        # check if name is taken
        if container.get_resource(name, soft=True) is not None:
            company = container.get_resource(name, soft=True)
            # List addresses for this company
            return context.come_back(MSG_EXISTANT_CHAPTER)
        # what if the form is all field, but thu user decides to change to different region?
        county = form['county']
        if county is not None:
            if 'switch' in county.rsplit('#'):
                #return context.come_back(MSG_CHOOSE_REGION)
                return self.GET
        # We are now ready to make the company resource
        company = container.make_resource(name, cls)
        # The metadata
        metadata = company.metadata
        language = resource.get_edit_languages(context)[0]
        metadata.set_property('title', Property(title, lang=language))
        metadata.set_property('vhosts', vhosts)
        metadata.set_property('website_is_open', 'community')
        # TODO we need to make this based on the URL of the
        # site expert.travel or buildersmerchants.info
        metadata.set_property('industry', ('travel',))
        metadata.set_property('business', tuple(form['business']))
        metadata.set_property('business_type', tuple(form['business_type']))
        # User id
        user = context.user
        # Remove user from old company
        companies = user.get_company()
        if companies:
            for x in companies:
                resource.get_resource(x.abspath).set_user_role(user.name, None)
        # Link the User to the newly created Company
        default_role = company.class_roles[0]
        company.set_user_role(user.name, default_role)
        # Add the user to the expert.travel site as a 'Member'
        root = user.get_expert_site_root()
        if root:
            root.set_user_role(user.name, root.class_roles[1])
        # Add the address
        address_title = form['address']
        address_title = [ x.strip() for x in address_title.splitlines() ]
        address_title = [ x for x in address_title if x ]
        address_name = checkid(address_title[0])
        if address_name is None:
            return context.come_back(MSG_EXISTANT_CHAPTER) # FIXME
        address_class_id = 'address'
        address_cls = get_resource_class(address_class_id)
        if company.get_resource(address_name, soft=True) is not None:
            return context.come_back(MSG_EXISTANT_CHAPTER)
        address = company.make_resource(address_name, address_cls)
        address_vhosts = []
        # We add the default vhost entry for the address
        address_site_url = ('%s.%s.expert.travel' % (address_name, company.name))
        # Split the Country, Region and County
        iana_root_zone, region, county = form['county'].rsplit('#', 2)
        address_vhosts.append(address_site_url)
        address_metadata = address.metadata
        address_metadata.set_property('title', Property(address_title[0], lang=language))
        address_metadata.set_property('address', address_title[1:])
        address_metadata.set_property('postcode', form['postcode'])
        address_metadata.set_property('county', county)
        address_metadata.set_property('region', region)
        address_metadata.set_property('iana_root_zone', iana_root_zone)
        address_metadata.set_property('vhosts', address_vhosts)
        address_metadata.set_property('website_is_open', 'community')
        addresses = user.get_address()
        if addresses:
            for x in addresses:
                resource.get_resource(x.abspath).set_user_role(user.name, None)
                # Link the User to the newly created Address and make them the Branch Manager
                default_role = address.class_roles[0]
                address.set_user_role(user.name, default_role)
        # go to the user's profile page
        goto = '/users/%s' % user.name
        return context.come_back(MSG_NEW_RESOURCE, goto=goto)


class Company_SearchForm(SearchForm):
    """
    Creates the Company Search Form
    """
    access = 'is_allowed_to_view'
    title = MSG(u'Company Search Form')
    description = MSG(u"Company search page.")
    icon = 'action_home.png'
    template = '/ui/core/templates/forms/company_search.xml'
    
    search_schema = {'company': Unicode}
    
    query_schema = freeze({
            'name': String,
            'title': Unicode})
    
    def get_namespace(self, resource, context):
        root = context.root
        found = None
        search_term = context.query['company'].strip()
        if search_term:
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
        
        return {'found': found}

class View(STLView):
    access = True
    title = MSG(u'Welcome')
    template = 'ui/company/home.xml'
    max_items_number = 1
    
    def get_max_items_number(self, resource, context):
        return self.max_items_number
    
    def get_items(self, resource, context):
        from tzm.company.address.address import Address
        addresses = []
        for _address in resource.search_resources(cls=Address):
            hosts = [fix_website_url(x) for x in _address.get_property('vhosts')]
            address = {'name': _address.get_title(),
                        'path': resource.get_pathto(_address),
                        'mtime': _address.get_property('mtime'),
                        'description': _address.get_property('description'),
                        'vhosts': hosts,
                        'subject': _address.get_property('subject'),
                      }
            addresses.append(address)
        return addresses

    def sort_and_batch(self, resource, context, items):
        size = self.get_max_items_number(resource, context)
        return items
    
    def get_items_namespace(self, resource, context):
    
        industry = resource.get_property('industry')
        vhosts = resource.get_property('vhosts')
        
        items = {}
        # Company addresses
        addresses = self.get_items(resource, context)

        items['company_title'] = resource.get_property('title')
        items['company_description'] = resource.get_property('description')
        items['vhosts'] = resource.get_property('vhosts')
        items['industry'] = resource.get_property('industry')
        items['business_type'] = resource.get_property('business_type')
        items['addresses'] = addresses
        
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
        addresses = self.get_items_namespace(resource, context)
        #if self.batch_template is not None:
        #    template = self.get_template(self.batch_template)
        #    namespace = self.get_batch_namespace(resource, context, items)
        #    batch = stl(template, namespace)
    
        # Content
        #items = self.sort_and_batch(resource, context, items)
        #if self.items_template is not None:
        #    template = self.get_template(context, self.items_template)
        #    namespace = self.get_item_namespace(resource, context, items)
        #    table = stl(template, namespace)
        #items = merge_dicts(addresses, {'batch': batch, 'info': info, 'tabs': tabs})

        return merge_dicts(addresses, {'batch': batch, 'info': info, 'tabs': tabs})
