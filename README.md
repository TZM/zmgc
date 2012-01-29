README for $package_name

Requirements
============

Software    Version   Used by         Home
---------   -------   -------------   ----------------------------------------
Python        2.6.6   itools          http://www.python.org/
iTools	      0.60.2  tzm             http://www.hforge.org/	
SoX	          14.2.0  tzm             http://sox.sourceforge.net/
SWFTools      0.8.1+  tzm             http://www.swftools.org/		


Sound files
===========
These were generated from the IBM Text-to-Speech: Unconstrained U.S. English Text Demo http://www.research.ibm.com/tts/coredemo.shtml


Install
=======

MacOSX
------

using Homebrew package manager

	# install the base libraries and applications
	# homebrew, see https://github.com/mxcl/homebrew/wiki/installation
	/usr/bin/ruby -e "$(curl -fsSL https://raw.github.com/gist/323731)"
	# follow this https://gist.github.com/1128998
	# to get the pygobject, gtk+ installed
	
	# here is a list of the libraries that i use
	☺  brew list
                                                      
	| library                   | library      | library    | library    |
	|:--------------------------|:-------------|:-----------|:-----------|
	| atk                       | imagemagick  | libsoup    | pixman     |
	| cairo                     | intltool     | libtasn1   | pkg-config |
	| cmake                     | jasper       | libtiff    | poppler    |
	| flac                      | jpeg         | libvorbis  | python     |
	| gd                        | lame         | libwmf     | readline   |
	| gdbm                      | libao        | little-cms | sqlite     |
	| gdk-pixbuf                | libcroco     | lua        | subversion |
	| gettext                   | libffi       | mad        | wget       |
	| git                       | libgcrypt    | mysql      | wv         |
	| glib                      | libgpg-error | neon       | xapian     |
	| glib-networking           | libgsf       | node       | xapian     |
	| gnutls                    | libmagic     | pango      |            |
	| gsettings-desktop-schemas | libogg       | pcre       |            |
	| gtk+                      | libsndfile   | pidof      |            |

	# PIL doesn't know OS X comes with freetype, we need to link this
	ln -s /usr/X11/include/freetype2 /usr/local/include/ 
	ln -s /usr/X11/include/ft2build.h /usr/local/include/ 
	ln -s /usr/X11/lib/libfreetype.6.dylib /usr/local/lib/ 
	ln -s /usr/X11/lib/libfreetype.6.dylib /usr/local/lib/libfreetype.dylib
	
	# install SOX, used for generating the sound files
	brew install -dv sox


i18n
----
$ /Users/khine/usr/local/python2.6/bin/python setup.py install
$ /Users/khine/usr/local/python2.6/bin/ipkg-update-locale.py
this will update all the locals and generate the xx.po files
* Extract text strings................
* Update PO template 
* Update PO files:
  en.po ................. done.
  fr.po (new)

$ /Users/khine/usr/local/python2.6/bin/ipkg-build.py
* Version: 0.60-200907171253
* Compile message catalogs: en fr
* Build XHTML files***
* Build MANIFEST file (list of files to install)


Initialise the app
==================

./bin/icms-init.py -p19080 -ea -wa --modules=ikaaro.blog,ikaaro.calendar,wiki -r tzm tzm && ./bin/icms-start.py tzm


The basics:
===========

Virtual hosts:
==============
NGINX conf file

    server {
            server_name  zmgc.aqoon.local;
            # All R-ead URI's point to 19080 instance
            location /
                    {
                    proxy_pass http://127.0.0.1:19080;
                    proxy_set_header        Host            $host;
                    proxy_set_header        X-Real-IP       $remote_addr;
                    proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
                    }
            # All W-rite point to 18080 instance
            # TODO get a list of all actions
            location ~* "(\;login|\;contact|\;edit|\;new_instance)" {
                    proxy_pass http://127.0.0.1:18080;
                    proxy_set_header        Host            $host;
                    proxy_set_header        X-Real-IP       $remote_addr;
                    proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
                    }

httpd-vhosts
============


Resetting itools and ikaaro
---------------------------

rm -rf /Users/khine/usr/local/python2.6/lib/python2.6/site-packages/itools*
rm -rf /Users/khine/usr/local/python2.6/lib/python2.6/site-packages/ikaaro*
rm /Users/khine/usr/local/python2.6/bin/iodf-greek.py 
rm /Users/khine/usr/local/python2.6/bin/igettext-*
rm /Users/khine/usr/local/python2.6/bin/icms-*
rm /Users/khine/usr/local/python2.6/bin/ipkg-*

python26 setup.py install


Node chat server
----------------

In order to run the chat server, you need to have installed nodejs and nowjs
then execute from the root of the the directory

    $ node ui/core/js/node/chat.js

TODO:

create storage for the messages, so that when the page is refreshed or when the user
has logged in, there is a list of all the messages that have been sent.

user_id, users, message

user_id - this is the user who sent the message
users - tuple of all the users who got the message, this will allow us to filter by recipients
message - lang;the actual message

alternative solution is to put the data into postgre db, something:

    everyone.now.sendGb = function(message) {
        client.query(
            'INSERT INTO messages SET owner_id = ?, user_id = ?, message = ?',
            [message.id, message.user_id, sanitize(message.message).entityEncode().trim()],
            function(err, info) {
                if (!err) {
                    everyone.now.pushMessage(message.message);
                }
            }
        );
    };


into a riak cluster see http://riakjs.org/:

    // npm install riak-js@latest
    var db = require('riak-js').getClient({host: "riak.myhost", port: "8098" });
    db.save('user', {users: ['user_id', 'user_id_n'...]}, 'message', 'timestamp'});

Favicon
-------

Generate it as a 32x32 desktop icon and upload this to the root of your folder.