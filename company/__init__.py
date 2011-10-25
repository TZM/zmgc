# -*- coding: UTF-8 -*-
# Copyright (C) 2009 Norman Khine <norman@abakuc.com>

# Import from itools
from itools.core import get_abspath

# Import from ikaaro
from ikaaro.skins import register_skin

# Import from tzm
from tzm.skins import CompanySkin

# Import from here
from company import Companies, Company

__all__ = [
    'Companies',
    'Company'
    ]
# Register skin
path = get_abspath('ui')
register_skin('company', CompanySkin(path))
