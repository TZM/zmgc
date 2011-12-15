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
from itools.core import merge_dicts
from itools.datatypes import Boolean, Email, Tokens, Unicode, String
from itools.gettext import MSG
from itools.web import AccessControl as BaseAccessControl, STLForm, INFO
from itools.web import ERROR
from itools.database import AndQuery, OrQuery, PhraseQuery, StartQuery

# Import from ikaaro
from ikaaro.access import RoleAware
from ikaaro.buttons import RemoveButton
import ikaaro.messages
from ikaaro.views import SearchForm
from ikaaro.workflow import WorkflowAware

class SiteRoleAware(RoleAware):
    """This base class implements access control based on the concept of
    roles.  Includes a user interface.
    """
    
    # To override
    __roles__ = [
        {'name': 'admins', 'title': MSG(u'Admin')},
        {'name': 'chapter_manager', 'title':  MSG(u'Chapter Manager')},
        {'name': 'chapter_member', 'title':  MSG(u'Chapter Member')},
        {'name': 'partners', 'title':  MSG(u'Partner')},
        {'name': 'reviewers', 'title': MSG(u"Reviewer")},
        {'name': 'members', 'title': MSG(u"Member")},
        {'name': 'guests', 'title': MSG(u"Guest")},
    ]
