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
from itools import get_version
from itools.core import get_abspath
from itools.gettext import register_domain

# Import from ikaaro
from ikaaro.skins import register_skin

# Import from here 
from root import Root
import skins
import user

# Make the product version available to Python code
__version__ = get_version()

# Register the tzm domain
register_domain('tzm', get_abspath('locale'))

# Register core skins
register_skin('core', get_abspath('ui/core'))
register_skin('icons', get_abspath('ui/icons'))
register_skin('js_calendar', get_abspath('ui/js_calendar'))
register_skin('progressbar', get_abspath('ui/progressbar'))
register_skin('tiny_mce', get_abspath('ui/tiny_mce'))
register_skin('wiki', get_abspath('ui/wiki'))

