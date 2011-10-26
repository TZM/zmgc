# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@khine.net>

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
        {'name': 'branch_manager', 'title':  MSG(u'Branch Manager')},
        {'name': 'branch_member', 'title':  MSG(u'Branch Member')},
        {'name': 'partners', 'title':  MSG(u'Partner')},
        {'name': 'reviewers', 'title': MSG(u"Reviewer")},
        {'name': 'members', 'title': MSG(u"Member")},
        {'name': 'guests', 'title': MSG(u"Guest")},
    ]
