# -*- coding: UTF-8 -*-
# Copyright (C) 2009 Norman Khine <norman@khine.net>

# Import from the Standard Library
import hashlib, urllib
from random import sample
from hashlib import sha1
from sys import platform
from urllib import quote

# Import from itools
from itools.core import freeze
from itools.web import get_context
from itools.database import AllQuery, PhraseQuery, NotQuery, OrQuery, StartQuery
from itools.database import AndQuery


###########################################################################
# Navigation helper functions
###########################################################################
def get_parameters(prefix, **kw):
    """Gets the parameters from the request form, the keyword argument
    specifies which are the parameters to get and which are their default
    values.

    The prefix argument lets to create different namespaces for the
    parameters, so the same page web can have different sections with
    different but equivalent parameters.

    For example, call it like:

      get_parameters('resources', sortby='id', sortorder='up')
    """
    # Get the form field from the request (a zope idiom)
    get_parameter = get_context().request.get_parameter

    # Get the parameters
    parameters = {}
    for key, value in kw.items():
        parameters[key] = get_parameter('%s_%s' % (prefix, key),
                                        default=value)

    return parameters


def preserve_parameters(preserve=freeze([])):
    """Returns an HTML snippet with hidden input html elements, there will
    be one element for each request parameter that starts with any of
    the prefixes contained in the preserve parameter.

    This lets to pass url request parameters through form actions, so we
    don't lose important navigation information.
    """
    snippet = []

    form = get_context().request.get_form()
    for k, v in form.items():
        for prefix in preserve:
            if k.startswith(prefix):
                snippet.append('<input type="hidden" name="%s" value="%s">'
                               % (k, quote(v)))
                break

    return '\n'.join(snippet)



###########################################################################
# Languages
###########################################################################

# Mark for translatios
u'Basque'
u'Catalan'
u'English'
u'French'
u'German'
u'Hungarian'
u'Italian'
u'Japanese'
u'Portuguese'
u'Spanish'


###########################################################################
# String format for display
###########################################################################

def reduce_string(title='', word_treshold=15, phrase_treshold=40):
    """Reduce words and string size.
    """
    ellipsis = '…'
    if isinstance(title, unicode):
        ellipsis = u'…'
    words = title.strip().split(' ')
    for i, word in enumerate(words):
        if len(word) > word_treshold:
            words.pop(i)
            word = word[:word_treshold] + ellipsis
            words.insert(i, word)
    title = ' '.join(words)
    if len(title) > phrase_treshold:
        title = title[:phrase_treshold] + ellipsis
    return title


###########################################################################
# User and Authentication
###########################################################################
# ASCII letters and digits, except the characters: 0, O, 1, l
tokens = 'abcdefghijkmnopqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ23456789'
def generate_password(length=6):
    return ''.join(sample(tokens, length))


def crypt_password(password):
    return sha1(password).digest()


###########################################################################
# Generate next name
###########################################################################
def generate_name(name, used, suffix='_'):
    """Generate a name which is not in list "used" based on name and suffix.
    Example:
      With name='toto.txt', used=['toto.txt', 'toto_0.txt']
      --> toto.txt and toto_0.txt are used so it returns toto_1.txt
      With name='toto.txt', used=['toto.txt', 'toto_0.txt'], suffix='_copy_'
      --> toto.txt is used so it returns toto_copy_0.txt
    """
    if name not in used:
        return name

    items = name.split('.', 1)
    basename = items[0]
    extent = ''
    if len(items) > 1:
        extent = '.%s' % items[1]

    # 1st time called
    if suffix not in basename:
        index = 0
    else:
        basename, index = basename.rsplit(suffix, 1)
        try:
            index = int(index) + 1
        except ValueError:
            basename = '%s%s%s' % (basename, suffix, index)
            index = 0

    name = ''.join([basename, suffix, str(index), extent])
    while name in used:
        index += 1
        name = ''.join([basename, suffix, str(index), extent])

    return str(name)


###########################################################################
# Generate next object name
###########################################################################
def generate_object_name(name, used, suffix='_'):
    """Generate a name which is not in list "used" based on class id.
    Example:
      class_name = 'news', with name news.xhtml --> news_0.xhtml etc... 
    """
    if name not in used:
        return name

    items = name.split('.', 1)
    basename = items[0]
    extent = ''
    if len(items) > 1:
        extent = '.%s' % items[1]

    # 1st time called
    if suffix not in basename:
        index = 0
    else:
        basename, index = basename.rsplit(suffix, 1)
        try:
            index = int(index) + 1
        except ValueError:
            basename = '%s%s%s' % (basename, suffix, index)
            index = 0

    name = ''.join([basename, suffix, str(index), extent])
    while name in used:
        index += 1
        name = ''.join([basename, suffix, str(index), extent])

    return str(name)

###########################################################################
# Index and Search
###########################################################################
def get_base_path_query(abspath, include_container=False):
    """Builds a query that will return all the objects within the given
    absolute path, like it is returned by 'resource.get_abspath()'.

    If 'include_container' is true the resource at the given path will be
    returned too.
    """
    # Case 1: everything
    if abspath == '/' and include_container is True:
        return AllQuery()

    # Case 2: everything but the root
    if abspath == '/':
        return NotQuery(PhraseQuery('abspath', '/'))

    # Case 3: some subfolder
    content = StartQuery('abspath', abspath + '/')
    if include_container is False:
        return content

    container = PhraseQuery('abspath', abspath)
    return OrQuery(container, content)

# Widgets
def fix_website_url(url):
    if url.startswith('http://'):
        return url
    return 'http://' + url
    
def clean_website_url(url):
    return url.lstrip('http://').rstrip('/')
    
def gravatar_url(email):
    default = "/ui/core/resources/no-gravatar.gif"
    size = 40

    # construct the url
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
    
    return gravatar_url
    