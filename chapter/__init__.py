# -*- coding: UTF-8 -*-
# Copyright (C) 2009 Norman Khine <norman@khine.net>

# Import from itools
from itools.core import get_abspath

# Import from ikaaro
from ikaaro.skins import register_skin

# Import from tzm
from tzm.skins import ChapterSkin

# Import from here
from chapter import Chapters, Chapter

# Silent pyflakes
Chapters, Chapter

# Register skin
register_skin('chapter', ChapterSkin(get_abspath('ui')))
