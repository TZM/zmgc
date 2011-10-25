# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@abakuc.com>

# Import from the Standard Library

# Import from itools
from itools.gettext import MSG

# Import from ikaaro
from ikaaro.buttons import BrowseButton

class CountryButton(BrowseButton):
    access = True
    css = 'button-country'
    name = 'country'
    title = MSG(u'Country')

class RegionButton(BrowseButton):
    access = True
    css = 'button-region'
    name = 'region'
    title = MSG(u'Region')