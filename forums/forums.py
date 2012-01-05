# -*- coding: UTF-8 -*-
# Copyright (C) 2012 Norman Khine <norman@khine.net>
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


# Import from the Standard Library

# Import from itools
from itools.gettext import MSG

# Import from ikaaro
from ikaaro.blog import Blog

class Forums(Blog):
    """
        Here we have a forum with a view to all chapter forums.
        We also link content comment threads, as these are discussions.
        
    """
    class_id = 'forums'
    class_title = MSG(u'Base view for the forums')