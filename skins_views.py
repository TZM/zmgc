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
from itools.core import thingy_lazy_property

# Import from ikaaro
from ikaaro.utils import reduce_string
from ikaaro.skins_views import LocationTemplate, LanguagesTemplate
from ikaaro.utils import CMSTemplate, reduce_string


class SiteLanguagesTemplate(LanguagesTemplate):

    template = 'ui/core/templates/widgets/languages.xml'

class SiteLocationTemplate(LocationTemplate):

    template = 'ui/core/templates/widgets/location.xml'

    @thingy_lazy_property
    def location(self):
        return bool(LocationTemplate.breadcrumb)

class SiteMenuTemplate(CMSTemplate):

    template = 'ui/core/templates/widgets/sitemenu.xml'
    
    @thingy_lazy_property
    def tabs(self):
        return bool(LocationTemplate.tabs)

class TabsTemplate(CMSTemplate):

    template = 'ui/core/templates/widgets/tabs.xml'

class PlayerTemplate(CMSTemplate):
    """
        jPlayer implementation
    """
    template = 'ui/core/templates/widgets/player.xml'

