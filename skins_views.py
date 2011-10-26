# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@khine.net>

# Import from ikaaro
from ikaaro.utils import reduce_string
from ikaaro.skins_views import LocationTemplate, LanguagesTemplate
from ikaaro.utils import CMSTemplate, reduce_string


class SiteLanguagesTemplate(LanguagesTemplate):

    template = 'ui/core/templates/widgets/languages.xml'

class SiteLocationTemplate(LocationTemplate):

    template = 'ui/core/templates/widgets/location.xml'

class TabsTemplate(CMSTemplate):

    template = 'ui/core/templates/widgets/tabs.xml'


