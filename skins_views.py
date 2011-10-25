# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@abakuc.com>

# Import from ikaaro
from ikaaro.utils import reduce_string
from ikaaro.skins_views import LocationTemplate, LanguagesTemplate
from ikaaro.utils import CMSTemplate, reduce_string


class SiteLanguagesTemplate(LanguagesTemplate):

    template = 'ui/abakuc/languages.xml'

class SiteLocationTemplate(LocationTemplate):

    template = 'ui/abakuc/location.xml'

class TabsTemplate(CMSTemplate):

    template = 'ui/abakuc/tabs.xml'


