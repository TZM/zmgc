README for $package_name

#Requirements

| Software  | Version | Used by | Home                        |
|:----------|:--------|:--------|:----------------------------|
| Python    | 2.7.2   | itools  | http://www.python.org/      |
| iTools    | 0.62    | tzm     | http://www.hforge.org/      |
| iKaaro    | 0.62    | tzm     | http://www.hforge.org/      |
| SoX       | 14.3.2  | tzm     | http://sox.sourceforge.net/ |
| dnspython | 1.9.4   | tzm     | http://www.dnspython.org/   |


##Sound files

These were generated from the IBM Text-to-Speech: Unconstrained U.S. English Text Demo http://www.research.ibm.com/tts/coredemo.shtml

#Install

##MacOSX

using Homebrew package manager

	# install the core libraries and applications
	# homebrew, see https://github.com/mxcl/homebrew/wiki/installation
	/usr/bin/ruby -e "$(curl -fsSL https://raw.github.com/gist/323731)"
	
	☺  brew install -dv git
	# install SOX, used for generating the sound files
	☺  brew install -dv sox
	
	☺  brew install -dv ...
	
	# here is a list of the libraries that i have
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

##Virtual Environment

We want to run our instance within a virtual environment
	
	# follow this https://gist.github.com/1128998
	# to get the pygobject, gtk+ installed
	
	# PIL doesn't know OS X comes with freetype, we need to link this
	ln -s /usr/X11/include/freetype2 /usr/local/include/ 
	ln -s /usr/X11/include/ft2build.h /usr/local/include/ 
	ln -s /usr/X11/lib/libfreetype.6.dylib /usr/local/lib/ 
	ln -s /usr/X11/lib/libfreetype.6.dylib /usr/local/lib/libfreetype.dylib

##i18n

	☺  $WORKON_HOME/itools/bin/python setup.py install
	☺  $WORKON_HOME/itools/bin/ipkg-update-locale.py
	this will update all the locals and generate the xx.po files
	* Extract text strings................
	* Update PO template 
	* Update PO files:
	en.po ................. done.
	fr.po (new)

	$ $WORKON_HOME/itools/bin/ipkg-build.py
	* Version: 0.60-200907171253
	* Compile message catalogs: en fr
	* Build XHTML files***
	* Build MANIFEST file (list of files to install)

##Initialise the app

	☺  cd $WORKON_HOME/itools/
	☺  ./bin/icms-init.py --help #to show you all the options
	☺  ./bin/icms-init.py -p19080 -eyour@email.tld -wpassword --modules=ikaaro.blog,ikaaro.calendar,wiki -r tzm instance-name
	☺  ./bin/icms-start.py instance-name

#Virtual hosts

##NGINX

    server {
            server_name  zmgc.aqoon.local;
            # All R-ead URI's point to 19080 instance
            location / {
				proxy_pass http://127.0.0.1:19080;
				proxy_set_header        Host            $host;
				proxy_set_header        X-Real-IP       $remote_addr;
				proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
			}
			# If we want to cluster
            # All W-rite point to 18080 instance
            # TODO get a list of all actions
            # location ~* "(\;login|\;contact|\;edit|\;new_instance)" {
            #         proxy_pass http://127.0.0.1:18080;
            #         proxy_set_header        Host            $host;
            #         proxy_set_header        X-Real-IP       $remote_addr;
            #         proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
            #         }
			# Adding the nodejs proxy
			location ~* "(/config.json|/nowjs/now.js|socket.io|/stat/1.gif)" {
				proxy_pass http://127.0.0.1:29080;
				proxy_set_header        Host            $host;
				proxy_set_header        X-Real-IP       $remote_addr;
				proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
			}

##APACHE

##Resetting itools and ikaaro

	☺  rm -rf $WORKON_HOME/itools/lib/python2.7/site-packages/itools*
	☺  rm -rf $WORKON_HOME/itools/lib/python2.7/site-packages/ikaaro*
	☺  rm $WORKON_HOME/itools/bin/iodf-greek.py 
	☺  rm $WORKON_HOME/itools/bin/igettext-*
	☺  rm $WORKON_HOME/itools/bin/icms-*
	☺  rm $WORKON_HOME/itools/bin/ipkg-*

#Nodejs and Nowjs

In order to run the chat server, you need to have installed nodejs and nowjs
then execute from the root of the the directory

	☺  brew install -dv node
	☺  curl http://npmjs.org/install.sh | sh
	☺  npm install nowjs -g
	☺  npm install validator -g

	☺  node ui/core/js/node/chat.js

#Nodester

It is planned to store the chat node application on nodester, and keep the chat logs into CouchDb, Riak or AWS RDS micro instance
More investigation would need to be done.

http://admin.nodester.com

#iriscouch.com
Free CouchDb store

http://zmgc.iriscouch.com/

#AWS RDS

We can also setup MySQL m1.micro instances.

##Favicon

Generate it as a 32x32 desktop icon and upload this to the root of your folder.

#How to contribute a patch:

1. Fork [Phoenix](https://github.com/nkhine/phoenix) from github.com
2. Create a new branch
3. Commit changes to this branch
4. Send a pull request

#Icons
[http://findicons.com/pack/2357/dortmund/1](http://findicons.com/pack/2357/dortmund/1)

#MaxMind Databases
[http://www.maxmind.com/download/geoip/database/](http://www.maxmind.com/download/geoip/database/)