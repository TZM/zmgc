# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@khine.net>

# Import from itools
from itools.web import STLForm
from itools.gettext import MSG
from itools.datatypes import Boolean, String
from itools.web import INFO, ERROR

# Import from here
from datatypes import Industry, BusinessSector, BusinessType
#from utils import get_industry_name, get_industry


class CPEditIndustry(STLForm):

    access = 'is_admin'
    title = MSG(u'Industry')
    description = MSG(u"Define the site's' industry.")
    icon_path = '/ui/core/icons/48x48/Booking48.png'
    template = '/ui/core/templates/forms/edit_industry.xml'
    schema = {
        'codes': String(multiple=True, mandatory=True)}

    def get_namespace(self, resource, context):
        industries = Industry().get_options()
        ws_industry = resource.get_property('industry')
        active = []
        if ws_industry:
            code = ws_industry[0]
        else:
            code = []
        for industry in industries:
            if industry['name'] in ws_industry:
                active.append({
                    'name': industry['name'],
                    'value': industry['value'],
                    'isdefault': code == industry['name']})

        # Not active industry
        not_active = [
            x for x in industries if x['name'] not in ws_industry ]
        not_active.sort(lambda x, y: cmp(x['name'], y['value']))

        ## Ok
        return {
            'active_industry': active,
            'not_active_industry': not_active}


    #######################################################################
    # Actions / Edit
    def action_change_default_industry(self, resource, context, form):
        codes = form['codes']

        # This action requires only one language to be selected
        if len(codes) != 1:
            message = ERROR(u'You must select one and only one industry.')
            context.message = message
            return
        default = codes[0]

        # Change the default industry 
        industries = resource.get_property('industry')
        industries = [ x for x in industries if x != default ]
        industries.insert(0, default)
        resource.set_property('industry', tuple(industries))
        # Ok
        context.message = INFO(u'The default industry has been changed.')


    def action_remove_industry(self, resource, context, form):
        codes = form['codes']

        # Check the default language is not to be removed
        industries = resource.get_property('industry')
        default = industries[0]
        if default in codes:
            message = ERROR(u'You can not remove the default industry.')
            context.message = message
            return

        # Remove the industry
        industries = [ x for x in industries if x not in codes ]
        resource.set_property('industry', tuple(industries))
        # Ok
        context.message = INFO(u'industry removed.')


    #######################################################################
    # Actions / Add
    action_add_industry_schema = {
        'code': String(mandatory=True)}

    def action_add_industry(self, resource, context, form):
        code = form['code']
        ws_industries = resource.get_property('industry')
        resource.set_property('industry', ws_industries + (code,))
        # Ok
        context.message = INFO(u'Industry added.')


class CPEditBusinessSector(STLForm):
    access = 'is_admin'
    title = MSG(u'Business Sector')
    description = MSG(u"Define the Company's BusinessSector.")
    add_icon = '/ui/core/icons/48x48/news_folder.png'  
    #icon = '/ui/core/icons/48x48/industry48.png' 
    template = '/ui/core/templates/forms/edit_business.xml'
    schema = {
        'codes': String(multiple=True, mandatory=True)}

    def get_namespace(self, resource, context):
        businesses = BusinessSector().get_options()
        ws_business = resource.get_property('business')
        active = []
        if ws_business:
            code = ws_business[0]
        else:
            code = []
        for business in businesses:
            if business['name'] in ws_business:
                active.append({
                    'name': business['name'],
                    'value': business['value'],
                    'isdefault': code == business['name']})

        # Not active industry
        not_active = [
        x for x in businesses if x['name'] not in ws_business ]
        not_active.sort(lambda x, y: cmp(x['name'], y['value']))

        ## Ok
        return {
                'active_business': active,
                'not_active_business': not_active}


    #######################################################################
    # Actions / Edit
    def action_change_default_business(self, resource, context, form):
        codes = form['codes']
        # Change the default business
        businesses = resource.get_property('business')
        default = codes[0]
        businesses = [ x for x in businesses if x != default ]
        businesses.insert(0, default)
        resource.set_property('business', tuple(businesses))
        # Ok
        context.message = INFO(u'The default business sector has been changed.')


    def action_remove_business(self, resource, context, form):
        codes = form['codes']

        # Check the default language is not to be removed
        businesses = resource.get_property('business')
        default = businesses[0]
        if default in codes:
            message = ERROR(u'You can not remove the default business sector that the company belongs to.')
            context.message = message
            return

        # Remove the business
        businesses = [ x for x in businesses if x not in codes ]
        resource.set_property('business', tuple(businesses))
        # Ok
        context.message = INFO(u'Company has been removed from the business sector..')


    #######################################################################
    # Actions / Add
    action_add_business_schema = {
        'code': String(mandatory=True)}

    def action_add_business(self, resource, context, form):
        code = form['code']

        ws_businesses = resource.get_property('business')
        resource.set_property('business', ws_businesses + (code,))
        # Ok
        context.message = INFO(u'Company has been added to the business sector.')

#
class CPEditBusinessType(STLForm):
    access = 'is_admin'
    title = MSG(u'Business Type')
    description = MSG(u"Define the Company's Business Type.")
    add_icon = '/ui/core/icons/48x48/news_folder.png'  
    #icon = '/ui/core/icons/industry.png' 
    template = '/ui/core/templates/forms/edit_business.xml'
    schema = {
        'codes': String(multiple=True, mandatory=True)}

    def get_namespace(self, resource, context):
        business_types = BusinessType().get_options()
        ws_business = resource.get_property('type')
        active = []
        if ws_business:
            code = ws_business[0]
        else:
            code = []
        for business in business_types:
            if business['name'] in ws_business:
                active.append({
                    'name': business['name'],
                    'value': business['value'],
                    'isdefault': code == business['name']})

        # Not active industry
        not_active = [
        x for x in business_types if x['name'] not in ws_business ]
        not_active.sort(lambda x, y: cmp(x['name'], y['value']))

        ## Ok
        return {
                'active_business': active,
                'not_active_business': not_active}


    #######################################################################
    # Actions / Edit
    def action_change_default_business(self, resource, context, form):
        codes = form['codes']
        # Change the default business
        businesses = resource.get_property('type')
        default = codes[0]
        businesses = [ x for x in businesses if x != default ]
        businesses.insert(0, default)
        resource.set_property('type', tuple(businesses))
        # Ok
        context.message = INFO(u'The default business type has been changed.')


    def action_remove_business(self, resource, context, form):
        codes = form['codes']

        # Check the default language is not to be removed
        businesses = resource.get_property('type')
        default = businesses[0]
        if default in codes:
            message = ERROR(u'You can not remove the default business sector that the company belongs to.')
            context.message = message
            return

        # Remove the business
        businesses = [ x for x in businesses if x not in codes ]
        resource.set_property('type', tuple(businesses))
        # Ok
        context.message = INFO(u'Company has been removed from the business sector..')


    #######################################################################
    # Actions / Add
    action_add_business_schema = {
        'code': String(mandatory=True)}

    def action_add_business(self, resource, context, form):
        code = form['code']

        ws_businesses = resource.get_property('type')
        resource.set_property('type', ws_businesses + (code,))
        # Ok
        context.message = INFO(u'Company has been added to the business sector.')
