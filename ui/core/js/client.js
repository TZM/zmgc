/** UI Interaction functions **/
function appendMsg(msg)
{		
	var container = "";
	var color = "";

	container = container
		.concat("<table class='message'><tr>")
		.concat(["<td class='date'>", getTimeString(), "</td>"].join(""))
		.concat(["<td valign='top' class='nick'>", msg.username, "</td>"].join(""))
		.concat(["<td class='msg-text'>", msg.text, "</td>"].join(""))
		.concat("</tr></table>");
	$("#log").append(container);
	scrollDown();
}

function scrollDown() 
{
  window.scrollBy(0, 100000000000000000);
  $("#entry").focus();
}

function getTimeString()
{
	var date = new Date();
	var result = "";
	
	if(date.getHours() < 10) 
		result = result.concat("0").concat(date.getHours());
	else 
		result = result.concat(date.getHours());
	
	
	if(date.getMinutes() < 10) 
		result = result.concat(":0").concat(date.getMinutes());
	else 
		result = result.concat(":").concat(date.getMinutes());
	
	return result;
}



/** Messaging and Utility functions **/
function sendMsg(callback)
{
	var msg = $("#entry");
	var text = new String(msg.val());
	
	if(text === "") 
		return false;
	else if(text.search("\/") == 0)
		sendUtility(text);
	else
	{
		appendMsg({ "username" : username, text : text });
		socket.emit("incoming", { "msg" : text });
	}
	
	callback(text);	
	msg.val("");
	
	return true;
}

function sendUtility(text)
{
	text = text.replace("\/", "");
	var parts = text.split(" ");
	var command = "util-" + parts[0];
	
	if(parts[0] == "clear")
		return $("#log").html("");
	if(parts[0] == "me")
			return appendMsg({ "username" : "server", "text" : "Your username is [" + username + "]" })

	
	socket.emit(command, parts.slice(1));
	return true;
}



/** Mostly just message logging initialization **/
$(document).ready(function()
{
	/** Vars for chat history funcitonality **/
	var chatLog = [];
	var logIdx = 0;	
	
	
	/** High level message sending && logging **/
	$("#entry").keydown(function(e) 
	{
		if(e.keyCode === 13) 
			sendMsg(function(msg) { addToLog(msg); });
		else if(e.keyCode === 38)
			decIdx(); 
		else if(e.keyCode === 40)
			incIdx();
			
	});	
	
		
	/** Message logging helper functions **/
	function addToLog(msg)
	{
		chatLog.push(msg); 
		logIdx = (chatLog.length)		
	}
	
	function incIdx()
	{
		if((logIdx+1) >= chatLog.length) 
			$("#entry").val("");
		else 
			$("#entry").val(chatLog[++logIdx]);
	}
	
	function decIdx()
	{
		if((logIdx-1) < 0) 
			$("#entry").val(chatLog[0]);
		else 
			$("#entry").val(chatLog[--logIdx]);
	}
});



/** Vars for socket.io functionality **/
var hostname = "localhost"
var socket = io.connect(hostname, { "port" : 8421, });
var username = "";


/** High level Socket.io message passing **/
socket.on("broadcast", function(data) { appendMsg(data); });
socket.on("init", function(data) { username = data.username });
socket.on("set-username", function(data) { username = data.username; });