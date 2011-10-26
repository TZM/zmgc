# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@khine.net>

# Import from itools
from itools.core import get_abspath
from itools.gettext import MSG

# Import from ikaaro
from ikaaro.skins import Skin as BaseSkin

# Import from here
from skins_views import SiteLanguagesTemplate, SiteLocationTemplate

class Skin(BaseSkin):
    '''
        As a front office we require 3 types of templates:
        1) The Phoenix Project main portal, this links all chapter sites.
        2) We also have Chapter websites, where each Chapter website object has
        its own modules:
            a) News
            b) Events
            c) Projects
            d) Forums
            e) Chat
            f) Polls
            g) Training
            h) Wiki
    '''

    languages_template = SiteLanguagesTemplate
    location_template = SiteLocationTemplate

    #######################################################################
    # Styles and Scripts
    #######################################################################
    def get_styles(self, context):
        # Generic
        styles = [
            '/ui/core/css/yui/cssreset/reset-min.css',
            '/ui/core/css/jquery-custom-theme/jquery-ui-1.8.7.custom.css',
            '/ui/core/css/flags-sprite.css',
            
        ]
        # Load the site specific styles
        if self.has_handler('style.css'):
            styles.append('%s/style.css' % self.get_canonical_path())

        return styles
    
    def get_scripts(self, context):
        #scripts = super(Skin, self).get_scripts(context) + [
        scripts = [
            '/ui/core/js/jquery/jquery-1.4.4.min.js',
            '/ui/core/js/jquery/jquery-ui-1.8.7.custom.min.js',
            ]

        get_scripts = getattr(context.view, 'get_scripts', None)
        if get_scripts is None:
            extra = getattr(context.view, 'scripts', [])
        else:
            extra = get_scripts(context)
        scripts.extend(extra)
        return scripts

class ChapterSkin(Skin):
    """
        This is the Chapter skin, this allows us to have different navigation setup
        and skin.
        For now this is just a copy of the main site.
    """
    
    def get_styles(self, context):
        styles = Skin.get_styles(self, context)
        if self.has_handler('style'):
            styles.append('/style/;download')
        else:
            styles.append('/ui/zeitgeist/style.css')

        return styles
