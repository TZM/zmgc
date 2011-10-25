# -*- coding: UTF-8 -*-
# Copyright (C) 2009 Norman Khine <norman@abakuc.com>

# Import from itools
from itools.core import get_abspath

# Import from ikaaro
from ikaaro.skins import register_skin 

# Import from here
from expert import Expert
from abakuc.skins import Skin

__all__ = [
    'Expert'
    ]

# Register skin
path = get_abspath('ui')
register_skin('expert', Skin(path))
