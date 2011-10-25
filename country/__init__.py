# -*- coding: UTF-8 -*-
# Copyright (C) 2009 Norman Khine <norman@abakuc.com>

# Import from itools
from itools.core import get_abspath

# Import from ikaaro
from ikaaro.skins import register_skin

# Import from abakuc
from abakuc.skins import CompanySkin

# Import from here
from country import Country

__all__ = [
    'Country'
    ]
# Register skin
path = get_abspath('ui')
register_skin('country', CompanySkin(path))
