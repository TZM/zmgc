# -*- coding: UTF-8 -*-
# Copyright (C) 2009 Norman Khine <norman@khine.net>

# Import from itools
from itools.core import get_abspath

# Import from ikaaro
from ikaaro.skins import register_skin

# Import from tzm
from tzm.skins import ChapterSkin

# Import from here
from country import Country

__all__ = [
    'Country'
    ]
# Register skin
path = get_abspath('ui')
register_skin('country', ChapterSkin(path))
