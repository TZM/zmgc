var server = require('http').createServer(function(req, res){
  res.end(html);
});
server.listen(29080);
console.log("This server's process pid is: " + process.pid);

var nowjs = require("now");
var everyone = nowjs.initialize(server);
var MESSAGE_BACKLOG = 200,
    SESSION_TIMEOUT = 60 * 1000;

var check = require('validator').check,
    sanitize = require('validator').sanitize

var sys = require('sys'),
  fs = require('fs'),
    spawn = require('child_process').spawn,
  file = __dirname + '/' + "messages";

spawn('touch' + file);

function updateRSS () {
  var bytes = parseInt(rss);
  if (bytes) {
    var megabytes = bytes / (1024*1024);
    megabytes = Math.round(megabytes*10)/10;
    $("#rss").text(megabytes.toString());
  }
}

var mem = process.memoryUsage();
var rss;

setInterval(function () {
  mem = process.memoryUsage();
}, 10*1000);

var messages = [];
var rss = updateRSS();

everyone.now.distributeMessage = function(message){
    var messagetime = (new Date()).getTime();
    // var mem = process.memoryUsage();
    console.log(mem.rss);
    console.log('User '+this.now.name+' added message ' +message + messagetime + ' ' + mem + ' mem: ' + rss);
    var str = sanitize(message).xss();
    everyone.now.receiveMessage(this.now.name, str, messagetime);
    messages.push([this.now.name, str, messagetime]);
    var message = {user_id: this.now.name, message: str, timestamp: messagetime};
    console.log(message);
    // we write the messages to the filesystem or feed it into the database
    fs.open(file, 'a+', 0666, function(err, fd) {
        if (!err) fs.write(fd, JSON.stringify(message) + '\n', null, 'utf8');
        })
};