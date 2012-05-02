# -*- coding: UTF-8 -*-
# Copyright (C) 2011 Norman Khine <norman@khine.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Import from itools
from itools.core import get_abspath, merge_dicts
from itools.gettext import MSG

# Import from ikaaro
from ikaaro.skins import Skin as BaseSkin

# Import from here
from skins_views import SiteLanguagesTemplate, SiteLocationTemplate
from skins_views import FooterTemplate, SiteMenuTemplate


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
    site_menu_template = SiteMenuTemplate
    upper_footer = FooterTemplate

    #######################################################################
    # Styles and Scripts
    #######################################################################
    def get_styles(self, context):
        # Generic
        styles = [
            '/ui/core/css/yui/cssreset/reset-min.css',
            '/ui/core/css/yui/cssgrids/grids-min.css',
			'/ui/core/css/footer.css',
            '/ui/core/css/core.css',
            '/ui/core/css/flags-sprite.css',
            '/ui/core/css/widgets.css',
            '/ui/js_calendar/calendar-aruni.css',
            '/ui/wiki/style.css',
        ]

        # Skin styles
        if self.get_handler('style.css',
                            cls=self.get_resource_cls('style.css'),
                            soft=True) is not None:
            styles.append('%s/style.css' % self.get_canonical_path())

        # View styles
        get_styles = getattr(context.view, 'get_styles', None)
        if get_styles is None:
            extra = getattr(context.view, 'styles', [])
        else:
            extra = get_styles(context)
        styles.extend(extra)
        
        # Database style
        db_style = context.site_root.get_resource('theme/style')
        ac = db_style.get_access_control()
        if ac.is_allowed_to_view(context.user, db_style):
            styles.append('%s/;download' % context.get_link(db_style))

        return styles
    
    def get_scripts(self, context):
        scripts = [
            '/ui/core/js/jquery/jquery-1.6.2.min.js',
			#'/ui/core/js/footer_plugins.js',
            '/ui/core/js/javascript.js',
            #'/ui/core/js/raphaeljs/raphael-min.js',
            #'/ui/core/js/world.js'
            ]

        #
        # Calendar (http://code.google.com/p/dyndatetime/)
        scripts.append('/ui/js_calendar/jquery.dynDateTime.pack.js')
        languages = [
            'af', 'al', 'bg', 'br', 'ca', 'da', 'de', 'du', 'el', 'en', 'es',
            'fi', 'fr', 'hr', 'hu', 'it', 'jp', 'ko', 'lt', 'lv', 'nl', 'no',
            'pl', 'pt', 'ro', 'ru', 'si', 'sk', 'sp', 'sv', 'tr', 'zh']
        accept = context.accept_language
        language = accept.select_language(languages)
        if language is None:
            language = 'en'
        scripts.append('/ui/js_calendar/lang/calendar-%s.js' % language)
        
        # View scripts
        get_scripts = getattr(context.view, 'get_scripts', None)
        if get_scripts is None:
            extra = getattr(context.view, 'scripts', [])
        else:
            extra = get_scripts(context)
        scripts.extend(extra)
        
        return scripts
    #
    #######################################################################
    # Main
    #######################################################################
    def build_namespace(self, context):
        namespace = merge_dicts(BaseSkin.build_namespace(self, context), {
        'upper_footer': self.upper_footer(context=context),
        })
        #print namespace
        return namespace


class ChapterSkin(Skin):
    """
        Returns a list of get_styles and get_scripts
        
        This allows us to have different navigation setup and skin.
        
        We have 3 layers:
        1/. The YUI3 reset and grids, plus the flags-sprite.css
        2/. The basic layout which is located in the chapter/ui/style.css
        3/. The overwirites db_style where each chapter can modify the style.css in the database
        
        Currently the get_scripts uses the core js scripts, this can be extended so that each indivudual
        chapter could extend the list. Similiar to the way the db_styles works.
    """
    
    def get_styles(self, context):
        styles = Skin.get_styles(self, context)

        return styles
        
    def get_scripts(self, context):
        scripts = Skin.get_scripts(self, context)
        
        return scripts
#
class ProjectSkin(Skin):
    """
        Each project can have its own specific skin.
    """
    
    def get_styles(self, context):
        styles = Skin.get_styles(self, context)

        return styles
        
    def get_scripts(self, context):
        scripts = Skin.get_scripts(self, context)
        
        return scripts