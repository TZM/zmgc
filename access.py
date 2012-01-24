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
from itools.web import ERROR, get_context
from itools.database import AndQuery, OrQuery, PhraseQuery, StartQuery

# Import from ikaaro
from ikaaro.access import RoleAware as SiteRoleAware
from ikaaro.buttons import RemoveButton
import ikaaro.messages
from ikaaro.views import SearchForm
from ikaaro.workflow import WorkflowAware

# Import from here
from tzm.messages import MSG_EXISTING_CHAPTER_ADMIN

class RoleAware(SiteRoleAware):
    """This base class implements access control based on the concept of
    roles.  Includes a user interface.
    """
    
    def is_allowed_to_create_chapter(self, user, resource):
        if user is None:
            return False
        if self.is_admin(user, resource):
            return True
        user_get_chapters = user.get_chapters()
        if user_get_chapters:
            context = get_context()
            context.message = MSG_EXISTING_CHAPTER_ADMIN
            return False 
        #elif self.is_admin(user, resource):
        #    role = 'admins'
        #else:
        #    role = self.get_user_role(user.name)
        ## The state of the resource
        #if isinstance(resource, WorkflowAware):
        #    state = resource.workflow_state
        #else:
        #    state = 'public'
        #
        ## Case 1: Extranet or Community
        #if security_policy in ('extranet', 'community'):
        #    if state == 'public':
        #        return True
        #    return role is not None
        #
        ## Case 2: Intranet
        #if role in ('admins', 'reviewers', 'members'):
        #    return True
        #elif role == 'guests':
        #    return state == 'public'
        return True
