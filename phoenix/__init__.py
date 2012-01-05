# -*- coding: UTF-8 -*-
# Copyright (C) 2009 Norman Khine <norman@khine.net>

# Import from itools
from itools.core import get_abspath

# Import from ikaaro
from ikaaro.skins import register_skin 

# Import from here
from phoenix import Phoenix
from tzm.skins import Skin

# Silent pyflakes
Phoenix

# Register skin
path = get_abspath('ui')
register_skin('phoenix', Skin(path))
