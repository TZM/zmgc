# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@abakuc.com>

# Import from the Standard Library

# Import from itools
from itools.gettext import MSG
from itools.web import STLView

# Import from here
from abakuc.skins_views import TabsTemplate

class View(STLView):

    access = True
    title = MSG(u'Welcome')
    template = 'ui/expert/home.xml'


    def get_namespace(self, resource, context):
        tabs = TabsTemplate(context)
        #tabs = None 
        user = context.user

        if user is None:
            return {'info': None, 'tabs': tabs}

        home = '/users/%s' % user.name
        info = {'name': user.name, 'title': user.get_title(),
                'home': home}
        print {'info': info, 'tabs': tabs}
        return {'info': info, 'tabs': tabs}

