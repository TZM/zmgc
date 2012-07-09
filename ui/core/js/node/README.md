#Polling / Commet / Push Implementation

* iTools/iKaaro for front-end web pages
* Node.js as comet server
* Faye as the comet library
* ZeroMQ as the transport system between iTools/iKaaro and Node.js

The goal is to keep the majority of work in Python and iTools/iKaaro. Set up a iTools/iKaaro application as described in the main [README.md Install](https://github.com/nkhine/phoenix#install) section.

We then use NginX to map our requests to the Node.js application.

Trigger Faye from your visitors' browser via javascript, which then signals to Node.js, which then adds the event to the ZeroMQ queue, which iTools/iKaaro picks up and can act upon.

