var http = require('http'),
    util  = require('util'),
    static = require('node-static'),
    faye = require('faye'),
    url = require('url'),
	City = require('geoip-static').City;

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

ZMGC.prototype.init = function() {
  var self = this;

  self.bayeux = self.createBayeuxServer();
  self.httpServer = self.createHTTPServer();

  self.bayeux.attach(self.httpServer);
  self.httpServer.listen(self.settings.port);
  console.log('Server started on PORT: ' + self.settings.port);
};

ZMGC.prototype.createBayeuxServer = function() {
  var self = this;
  
  var bayeux = new faye.NodeAdapter({
    mount: '/faye',
    timeout: 45
  });
  
  return bayeux;
};

ZMGC.prototype.createHTTPServer = function() {
  var self = this;

  var server = http.createServer(function(request, response) {
    var file = new static.Server('./public', {
      cache: false
    });

    request.addListener('end', function() {
			
      var location = url.parse(request.url, true),
          params = (location.query || request.headers);
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
				//db.enableIndex('users');
				//var results = db.search('users', { timestamp: [1330536456424,1330593323542] });
				//console.log(results);
				response.writeHead(200, {
		      		'Content-Type': 'image/gif'
		    	});
				origin = /\/(.*)\.gif/.exec(request.url);
				if (origin) {
					var ip = request.headers['x-real-ip'];
					if (ip === null || ip === "127.0.0.1") {
					    ip = "82.246.239.187";
					}
					city = new City("../../../../data/GeoLiteCity.dat");
					city.lookup(ip, function(err, location) {
							obj = {
								city: location.city
	            				,longitude: location.longitude
								,latitude: location.latitude
	            				,ip: ip
								,timestamp: time
							}
							self.bayeux.getClient().publish('/stat', obj);
							console.log(obj);
							// write to riak cluster
							//db.save('users', ip, obj, { index: {timestamp: time} });
							//console.log('was saved in the riak cluster');
					});
					//console.log(origin[1], request.connection.remoteAddress, request.headers['user-agent']);
				  
		    	}
				response.end("OK");
      } else {
        file.serve(request, response);
      }
    });
  });
  return server;
};

module.exports = ZMGC;
