# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@khine.net>

# Import from itools
from itools import get_version
from itools.core import get_abspath

# Import from ikaaro
from ikaaro.skins import register_skin

# Import from here 
from root import Root
import skins
import user

# Make the product version available to Python code
__version__ = get_version()

# Register skins
#register_skin('zeitgeist', get_abspath('ui/zeitgeist'))
register_skin('core', get_abspath('ui/core'))
