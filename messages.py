# -*- coding: UTF-8 -*-
# Copyright (C) 2007 Norman Khine <norman@khine.net>
# Import from itools
from itools.gettext import MSG
from itools.web import INFO, ERROR


MSG_EXISTANT_CHAPTER = ERROR(
    u'A chapter with this name is already in the database!')

MSG_NON_EXISTANT_CHAPTER = ERROR(
    u'There is no chapter with this name on the database, please first create a chapter!')

MSG_EXISTANT_ADDRESS = ERROR(
    u'An address with this name already exists in the database!')

MSG_CHOOSE_REGION = ERROR(
    u'Please choose your region!')
    
MSG_NEW_CHAPTER = INFO(
    u'Your chapter site has been created and you will receive an email with further details.')
