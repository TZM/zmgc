var http = require('http'),
	util  = require('util'),
	static = require('node-static'),
	url = require('url'),
	nowjs = require('now'),
	express = require( 'express' ),
	City = require('geoip').City;

function ZMGC(options) {
	if (! (this instanceof arguments.callee)) {
		return new arguments.callee(arguments);
	}
	var self = this;
	self.settings = {
		port: options.port
	};
	self.init();
};

var everyone;
ZMGC.prototype.init = function() {
	var self = this;

	self.httpServer = self.createHTTPServer();
	everyone = nowjs.initialize(self.httpServer);
	self.httpServer.listen(self.settings.port);
	console.log('Server started on PORT: ' + self.settings.port);
};

ZMGC.prototype.createHTTPServer = function() {
	var self = this;

	var server = http.createServer(function(request, response) {
		var remoteIp = request.connection.remoteAddress;
		var file = new static.Server('./public', {
			cache: false
		});
		function onEnd() {
			/* if new connection identify user */
			var location = url.parse(request.url, true);
			//params = (location.query || request.headers);
			if (location.pathname == '/config.json' && request.method == "GET") {
				response.writeHead(200, {
					'Content-Type': 'application/x-javascript'
				});
				var jsonString = JSON.stringify({
					port: self.settings.port
				});
				response.end(jsonString);
			} else if (location.pathname == '/stat/1.gif' && request.method == 'GET') {
				var time = +new Date();
				var origin;
				response.writeHead(200, {
					'Content-Type': 'image/gif'
				});
				origin = /\/(.*)\.gif/.exec(request.url);
				if (origin) {
					var ip = request.headers['x-real-ip'];
					if (ip === null || ip === "127.0.0.1") {
					  console.log('dddd');
						ip = "82.246.239.187";
					}
					//city = new City('/home/andumitru/freelancer/phoenix/data/GeoLiteCity.dat');
					city = new City('../../../../data/GeoLiteCity.dat');
					city.lookup(ip, function(err, location) {
						var obj;
						console.log( err );
						if ( !err && location ) {
							obj = {
								city: location.city
								,longitude: location.longitude
								,latitude: location.latitude
								,ip: ip
								,timestamp: time
							};
						} else { 
							console.log( 'server fake location' );
							obj ={ 
								city: 'Bexleyheath',
								longitude: 0.15000000596046448,
								latitude: 51.45000076293945,
								ip: '86.173.61.119',
								timestamp: 1343054092459 
							};
						}
						console.log(obj);
						console.log(everyone);
						everyone.now.receiveLocation(obj);
					});
				}
				response.end("OK");
			} else {
				file.serve(request, response);
				/*
						var	obj ={ 
								city: 'Bexleyheath',
								longitude: 0.15000000596046448,
								latitude: 51.45000076293945,
								ip: '86.173.61.119',
								timestamp: 1343054092459 
							};
						everyone.now.receiveLocation(obj);
						*/
			}
		}
		
		request.on('end', onEnd);
	});
	return server;
};

module.exports = ZMGC;
