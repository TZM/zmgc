

$(document).ready(function(){    
		
  	var status = "stop";
	var dragging = false;
	var time = 0;
	// play/pause
		
	$("#zen .button").bind('click', function() {
		// not sure if this can be done in a simpler way.
		// when you click on the edge of the play button, but button scales down and doesn't drigger the click,
		// so mouseleave is added to still catch it.
		 time = $("#tmp_duration").val() * 1000;
			onClick();
	});
	
	function onClick() {  		
           
		
        if(status != "play") {
			status = "play";
			$(".jp-playlist-current .playinfor div#zen").addClass( "play" );
			
			$(".jp-jplayer_").jPlayer("play");
			
		} else {
		$('.jp-playlist-current .playinfor div#zen .circle').removeClass( "rotate" );
			$(".jp-playlist-current .playinfor div#zen").removeClass( "play" );
		status = "pause";
		}
	};

	// functions
	
	function displayProgress(pc) {
		
		var degs = 100 * 3.6+"deg"; 
		$('#zen .progress').animate({rotate: degs}, pc);
	}
	function displayBuffered(pc) {
		var degs = 100 * 3.6+"deg"; 
		pc= pc*0.5;
		$('#zen .buffer').animate({rotate: degs}, pc);
	}
});
