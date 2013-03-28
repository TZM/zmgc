
/**
 * Module dependencies.
 */

var express = require('express')
  , routes = require('./routes')
	, util  = require('util')
  , user = require('./routes/user')
  , http = require('http')
	, url = require('url')
	, nowjs = require('now')
	, City = require('geoip').City
  , path = require('path');

var app = express();

app.configure(function(){
  app.set('port', process.env.PORT || 29080);
  app.set('views', __dirname + '/views');
  app.set('view engine', 'jade');
  app.use(express.favicon());
  app.use(express.logger('dev'));
  app.use(express.bodyParser());
  app.use(express.methodOverride());
  app.use(app.router);
  app.use(express.static(path.join(__dirname, 'public')));
});
app.locals.pretty = true;

app.configure('development', function(){
  app.use(express.errorHandler());
});

app.get('/', routes.index);
app.get('/users', user.list);

var server = http.createServer(app);
var everyone = nowjs.initialize( server );
server.listen(app.get('port'), function(){
  console.log("Express server listening on port " + app.get('port'));
});
