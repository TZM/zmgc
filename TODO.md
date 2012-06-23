#The Phoenix project roadmap

More info at [https://trello.com/zmgc](https://trello.com/zmgc)

The following list is just for this prototype, but the ideas can be applied using any other framework, provided the libraries are supported by the language/application used to develop.

1. wireframes for main portal and chapter sites
2. questionnaire module - MCQ, MAQ and Free text input, so that it can be also used as a Poll
3. user profile, allow sites to control what data they want to store
4. video room - integrate nodejs using the python library to create a chat/video room see http://driv.in
5. enhance the existing style, perhaps use YUI2 grids, this way we can have a template that can be control by each individual users' preferences
6. right-to-left template for: 
 Arabic alphabet - used for Arabic, Persian, Urdu and many other languages.
 Hebrew alphabet - used for Hebrew, Yiddish and some other Jewish languages.
 Syriac alphabet - used for varieties of the Syriac language.
 Thaana - used for Dhivehi.
 N'Ko script - used for several languages of Africa.
8. up-to-down template for Mandarin Cantonese Taiwanese Shanghainese Japanese languages
9. mobile
10. create import scripts for different forums, wikis and documents from drupal, joomla, phpboard, wordpress etc... link these to the appropriate module, so if we are on the Forum, the user should have a tab 'Import'
11. ikaaro.turk - this will be a separate module, similar to ikaaro.wiki, and is based on mTurk from Amazon Web Services, where 'work' is distributed across many persons, thus the result is achieved much faster. For example, if we have an Open Office document, written in English, then the ikaaro.turk module will: 
	a. create a 'clone' of the document in how ever many languages that the original document needs to be translated in
	b. each 'clone', will then be split into small sections, if the document is 1,000 words containing 25 paragraphs then it will be split in 5 paragraphs (~ 200 words per paragraph)
	c. we will then have a form, which will contain:
	
	~~~
	-----------------------
	original 200 word text
	-----------------------

	[button ... (Translate)] - when clicked, an input form is created
 
	[input form for the translator to type into]

	[button ... (Submit)]
	~~~

	Using this model, we can distribute the translation work to many members. And as we are using Git we can then automatically merge all the sections, back to the main translated document.

	We must build workflows that is related to the size of the document and split the content by the amount of volunteers who have accepted to work on this, so if 25 people volunteer to help to translate the document, then the 25 paragraphs will be one paragraph by a person.

	Extendability - the same workflow can apply to other media projects, for example if we need a sound file to be transcoded, we can calculate the length of the sound file (for this example, lets say it is 10 minutes), and the language is English.

	We have a button (Call for Action...) on a form that contains the file, when a volunteer clicks on this button, we register that this person wants to help in transcoding the sound file. At the end of a set period, hopefully we can have 10 people willing to transcode the sound file. The sound file is then pushed through Audacity and split into 10 chunks of 1 minute each.

	A form is then presented with the 1 minute file and an input form for the transcoder to type the text. When all 10 chunks have been transcoded the text can then be pushed into the translation workflow, as discussed in the first example. So we have also a translation of the transcoded file.

	Then this transcoded and translated piece of work can be sent to the voice over group for the specific language where a new recording can be made in that language. Or the subtitle group etc...

	core tools to use: audacity, python's NLMP library which will be used to process the raw text data. maybe even push this into an mechanical translation service, so that most of the work is done and then a human volunteer can simply verify that the text makes sense.
 
12. set workflow for images, where the raw file (.psd, .gimp etc...) is uploaded, and other artists can localize this. 

13. Search - create the autofill so that http://localhost:8080/;search?text=''&output=json so in my class if the output is json this can then be pushed into the autofill, otherwise on submit, we just return the results on the page.

14. for mass server processing create an army of clustered hardware and launch this using boto and ec2, each chapter co-ordinator should setup a AWS account and setup a user, who can use the resources. Then if we have 10 chapters with AWS accounts, we can launch 200 micro-instances to distribute the work load. so the overall cost will be much lower, then having one big instance or using the existing server to do the heavy work.

15. Video and Audio streaming - custom jPlayer widget, to link files uploaded or linked in the user's profile page/playlist use, see the http://code.google.com/apis/youtube/2.0/reference.html#youtube_data_api_tag_media:content

	here is the example for TZMOfficialChannel http://gdata.youtube.com/feeds/api/users/TZMOfficialChannel/uploads?v=2&alt=jsonc 

	also see this: http://code.google.com/apis/youtube/articles/view_youtube_jsonc_responses.html

	also look at the http://icant.co.uk/easy-youtube/ perhaps it can be integrated.

	Using jPlayer it is not possible (well i have not found a way yet) to stream the YouTube video, I will have to hack the zPlayer module and create a template so that if the user adds a link to a video such as YouTube/Vimeo this is correctly displayed in the zPlayer.

	Also create a new class so that we can pull the metadata values directly from the YouTube API, here is an example code:

	~~~
	import gdata.youtube
	import gdata.youtube.service
	yt_service = gdata.youtube.service.YouTubeService()
	yt_service.ssl = True
	yt_service.developer_key = '53cr3t'
	yt_service.client_id = 'zeitgeist'
	~~~

	and see http://code.google.com/apis/youtube/1.0/developers_guide_python.html#RetrievingVideoEntry

16. pipes.yahoo.com - to aggregate the content from different sites not on the Phoenix.

	example: http://pipes.yahoo.com/pipes/pipe.run?_id=26ca074a13d28a8ad64e154a76244d43&_callback=eYTp.getFeed&_render=json&s=TZMOfficialChannel

17. User profile - make user's skills a prominent requirement so that you can then link these skills to the projects. for example a user adds a project, from the project description it will be possible to pull out a number of tags and then match this with a persons who's skills may fulfill the requirements for the project.
an example script based on project data pulled from http://www.tzmnetwork.com/forums/topic/61/education-amp-art:

	~~~
	>>>  from nltk import pos_tag, word_tokenize
	>>>  description = """Hello. \
	I'm Irish but based in France. At the moment, I'm working to create a business/charity which incorporates a traditional montessori school and artists ateliers in the same building. Practical education should be an important part of the process for the Zeitgeist movement and the principles which I am working towards are very compatible with the Zeitgeist movements declared aspirations. \
	There is a lot of discussion here but education is more than that. It hardwires the young person to think for themselves as opposed to adding untraditional thought patterns, in later years. It also creates a dynamic peer group. \
	This school is for children aged 3-18 years. The artists will be adults. I'm hoping to be able to facilitate education for both groups using the principles of montessori education. Whether the adults can learn as much as the children is a question. The expectation and plan is that they can cross pollinate. The children's school (3-18 years) will involve education in the arts and science. Covering traditional topics, creative practices and environmental awareness and systems of living.\
	I'm looking for financial aid or guidance, to raise the finances required. This will be the second school in france, though radically different to the first. \
	My intention is to look to foundations in the USA, UK, Ireland and France. Asking foundations for aid is not something which I have any experience with, so if there is anyone here who has, I would appreciate any constructive advice you can offer.\
	The school / arts atelier and training centre, has a volume of 3000 metres square or 9000 square feet. It's in a slightly run down factory on the edge of Paris, in a poor area within ile de France and will need total refurbishment. \
	The first school was much smaller than this, being of 110 metres square and is a great success. This second one is obviously a much larger project. \
	I can send references to anyone interested in becoming involved. Feel free to email me. \
	best regards \
	Tom""""
	>>> tagged_description = pos_tag(word_tokenize(description))
	>>> default_tagger.tag(tagged_description)
	[(('Hello.', 'NN'), 'NN'), (('I', 'PRP'), 'NN'), (("'m", 'VBP'), 'NN'), (('Irish', 'JJ'), 'NN'), (('but', 'CC'), 'NN'), (('based', 'VBN'), 'NN'), (('in', 'IN'), 'NN'), (('France.', 'NNP'), 'NN'), (('At', 'NNP'), 'NN'), (('the', 'DT'), 'NN'), (('moment', 'NN'), 'NN'), ((',', ','), 'NN'), (('I', 'PRP'), 'NN'), (("'m", 'VBP'), 'NN'), (('working', 'VBG'), 'NN'), (('to', 'TO'), 'NN'), (('create', 'VB'), 'NN'), (('a', 'DT'), 'NN'), (('business/charity', 'NN'), 'NN'), (('which', 'WDT'), 'NN'), (('incorporates', 'VBZ'), 'NN'), (('a', 'DT'), 'NN'), (('traditional', 'JJ'), 'NN'), (('montessori', 'NN'), 'NN'), (('school', 'NN'), 'NN'), (('and', 'CC'), 'NN'), (('artists', 'NNS'), 'NN'), (('ateliers', 'NNS'),

	>>> nltk.help.upenn_tagset('RB')
	RB: adverb
	occasionally unabatingly maddeningly adventurously professedly
	stirringly prominently technologically magisterially predominately
	swiftly fiscally pitilessly ...
	>>> nltk.help.upenn_tagset('NN')
	NN: noun, common, singular or mass
	common-carrier cabbage knuckle-duster Casino afghan shed thermostat
	investment slide humour falloff slick wind hyena override subhumanity
	machinist ...
	>>> nltk.help.upenn_tagset('VB')
	VB: verb, base form
	ask assemble assess assign assume atone attention avoid bake balkanize
	bank begin behold believe bend benefit bevel beware bless boil bomb
	boost brace break bring broil brush build ...
	~~~
        
	Now that we have the 'description' broken down by verbs, nouns etc... we can match against user profile data and suggest to the user possible members who may be able to help with the project.

	Obviously we can go deeper using the NLTK library and analyze the project description more accurately, but this is a further study, for more information see, Chapter 7: http://nltk.googlecode.com/svn/trunk/doc/book/ch07.html


#Storage

Create storage for the messages, so that when the page is refreshed or when the user has logged in, there is a list of all the messages that have been sent.

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

current [chat.zmgc.net](chat.zmgc.net) uses MangoDB see [https://github.com/nkhine/chat](https://github.com/nkhine/chat) for the code - this will be merged into the Phoenix project as a widget.
    
Also we need to utilise the local storage, html5. 

#Using nodejs within python

`scraper.js`

    var jsdom = require('jsdom');

    var args = process.argv.slice(2),
        html = unescape(args[0]),
        parser = unescape(args[1]);

    jsdom.env({
        html: html,
        scripts: ['./jquery.js']
    }, function(err, window){
        $ = window.jQuery;
        try{
            eval(parser);
        }catch(e){console.log({error: e});}
    });

`foo.py`
    
	import urllib2
    import commands

    html = urllib2.urlopen('http://google.com').read();
    parser = """var title = $('#hplogo').attr('alt');
    console.log({'title':title});
    """
    content = commands.getoutput('node ./scraper.js %s %s' % 
                                 (urllib2.quote(html), urllib2.quote(parser)))

	>>> "{title: 'Google'}"

#Update Tue 27 Mar 2012 10:14:00 CEST

* the map.zmgc.net is functioning and needs to be integrated into this project
* use redis to log data from the map stats and then push this into itools, it will be more efficient

#Gitlib and Gitolite

* use gitolite/gitlib to make communication between remote nodes more efficient
* use riak cluster to store the user sessions and then clone these across the nodes

#Project.py

A core project website has members