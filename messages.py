# -*- coding: UTF-8 -*-
# Copyright (C) 2011 Norman Khine <norman@khine.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
