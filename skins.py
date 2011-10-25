# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@abakuc.com>

# Import from itools
from itools.core import get_abspath
from itools.gettext import MSG

# Import from ikaaro
from ikaaro.skins import Skin as BaseSkin

# Import from here
from skins_views import SiteLanguagesTemplate, SiteLocationTemplate

class Skin(BaseSkin):
    '''
        As a front office we require 3 types of navigation:
        1) On the main directories sites such as
        a) Expert.Travel - we want to list all business functions
        b) Destinations Guide - we want to list all continents
        2) We also have Company views, where each Company object has
        its own navigation:
        a) News
        b) Jobs
        c) Branches
        3) Lastly we also have Training programme view, here we list
        all the Modules for each training programme.

        We also need to consider the fact that expert.travel has
        i18n versions so that http://uk.expert.travel will list
        only companies that have UK addresses.
    '''

    languages_template = SiteLanguagesTemplate
    location_template = SiteLocationTemplate

    #######################################################################
    # Styles and Scripts
    #######################################################################
    def get_styles(self, context):
        # Generic
        styles = [
            '/ui/abakuc/yui/reset-fonts-grids/reset-fonts-grids.css',
            '/ui/expert/custom-theme/jquery-ui-1.8.7.custom.css',
            '/ui/abakuc/css/jquery.ui.selectmenu.css',
        ]
        # We load the site specific styles for Expert.Travel, DestinationsGuide etc...
        if self.has_handler('style.css'):
            styles.append('%s/style.css' % self.get_canonical_path())

        return styles
    
    def get_scripts(self, context):
        # TODO upgrade to latest jQuery
        #scripts = super(Skin, self).get_scripts(context) + [
        scripts = [
        '/ui/abakuc/js/javascript.js',
        '/ui/abakuc/js/jquery-1.4.4.min.js',
            '/ui/abakuc/js/jquery-ui-1.8.7.custom.min.js',
            '/ui/abakuc/js/jquery.cookie.js',
            '/ui/abakuc/js/jquery.ui.selectmenu.js',
            '/ui/abakuc/js/abakuc.js',
        #'http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.js',
        #'http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/jquery-ui.js',
            ]

        get_scripts = getattr(context.view, 'get_scripts', None)
        if get_scripts is None:
            extra = getattr(context.view, 'scripts', [])
        else:
            extra = get_scripts(context)
        scripts.extend(extra)
        return scripts

class CompanySkin(Skin):
    def get_styles(self, context):
        styles = Skin.get_styles(self, context)
        if self.has_handler('style'):
            styles.append('/style/;download')
        else:
            styles.append('/ui/abakuc/style.css')

        return styles

class TrainingSkin(Skin):
    template = '/ui/training/template.xhtml'

    #here = context.handler
    #keywords = here.get_property('dc:subject')
    #meta = [{'name': 'description',
    #         'content': here.get_property('dc:description')},
    #        {'name': 'keywords',
    #         'content': keywords},
    #        {'name': 'robots',
    #         'content': 'index,follow'}]
    #site_root = here.get_site_root()
    #site_title = site_root.get_title()
    #title = '%s: %s' % (site_title, here.get_title())
    #if site_root is here:
    #    if isinstance(site_root, ExpertTravel):
    #        root = context.root
    #        countries = [x[1] for x in root.get_authorized_countries(context)]
    #        country = str.upper(countries[0])
    #        level1 = context.get_form_value('level1')
    #        level2 = context.get_form_value('level2')
    #        level3 = context.get_form_value('level3')
    #        level4 = context.get_form_value('level4')
    #        keywords = '%s, %s, %s' % (site_title, country, here.get_title())
    #        if level1 is not None:
    #            keywords = {'name': 'keywords', 'content': '%s, %s, %s' % \
    #            (site_title, country, level1)}
    #            #meta[keywords] = keywords

