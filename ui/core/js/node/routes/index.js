
/*
 * GET home page.
 */
var geoipCity = require('geoip').City;
var	city = new geoipCity('/home/andumitru/freelancer/phoenix/data/GeoLiteCity.dat');

exports.index = function(req, res){
	var ip = ( req.connection.remoteAddress !== "127.0.0.1" ) ?req.connection.remoteAddress:"72.196.192.58" ;
	city.lookup( ip, function( err, loc ) { 
//		console.log( loc );
		if ( err ) { 
			loc = { };
		}
  	res.render('index', { title: 'Express', loc: loc });
	});
};
