$(document).ready(function(){
	///init screen
	var player = $("#zen .player");
	var total_length=$(".jp-type-playlist .jp-playlist ul li").length;
	console.log(total_length);
	var init_point = new Array(3);
	init_point[0]=0;
	var list_length = new Array(3);
	var title = new Array(3);
	var mp = new Array(3);
	var oga = new Array(3);
	var m4v = new Array(3);
	var ogv = new Array(3);
	var webmv = new Array(3);
	var poster = new Array(3);
	var init_flag = 0; 
	var show_controls = 0;


	for(i=1; i<4; i++)
	{
		list_length[i] = $(".jp-type-playlist #tabs-"+i+" ul li").length;
		title[i] = 	new Array(list_length[i]);
		mp[i] = 	new Array(list_length[i]);
		oga[i] = 	new Array(list_length[i]);
		m4v[i] = 	new Array(list_length[i]);
		ogv[i] = 	new Array(list_length[i]);
		webmv[i] = 	new Array(list_length[i]);
		poster[i] = new Array(list_length[i]);
		init_point[i-1]=init_flag; 

	for(j=0; j< list_length[i] ; j++)
	{
		title[i][j] = 	$(".jp-type-playlist #tabs-"+i+" ul li").eq(j).text();
		mp[i][j] = 		$(".jp-type-playlist #tabs-"+i+" ul li a").eq(j).attr("mp");
		oga[i][j] = 	$(".jp-type-playlist #tabs-"+i+" ul li a").eq(j).attr("oga");
		m4v[i][j] = 	$(".jp-type-playlist #tabs-"+i+" ul li a").eq(j).attr("m4v");
		ogv[i][j] = 	$(".jp-type-playlist #tabs-"+i+" ul li a").eq(j).attr("ogv");
		webmv[i][j] = 	$(".jp-type-playlist #tabs-"+i+" ul li a").eq(j).attr("webmv");
		poster[i][j] = 	$(".jp-type-playlist #tabs-"+i+" ul li a").eq(j).attr("poster");
		init_flag++;
	}
    }
	///initial player with empty playlist
	var Playlist = new jPlayerPlaylist({
		jPlayer: "#jquery_jplayer_1",
		cssSelectorAncestor: "#jp_container_1"
		},[], ///empty list, to hold the items
		{swfPath: "/ui/core/js/jPlayer",
			supplied: "oga, mp3,m4v,ogv,webmv",
			wmode: "window"
		});
	
	console.log(Playlist);
	//console.log($("#jquery_jplayer_1").jPlayer("option", "solution"));
	//console.log($("#jquery_jplayer_1").event.Playlist.status.currentPercentAbsolute);
	//console.log($("#jquery_jplayer_1").event.jPlayer.status);
	///console.log(Playlist.text(lp+"%"));
    ///add media list into the playlsit
    for(i=1; i<4; i++)
    {
      for(j=0; j< list_length[i] ; j++)
      {
        Playlist.add({
          title: title[i][j],
          mp3: mp[i][j],
          oga: oga[i][j],
          m4v: m4v[i][j],
          ogv: ogv[i][j],
          webmv: webmv[i][j],
  		poster: poster[i][j]
        });
      }
    }

    /// slide action for the control panel
    $(".controls").click(function(){
		$("#jp_controls_panel").slideToggle();
	});
	
	$('#player button').click(function() {
	    $(this).next().slideToggle();
		$("#player button").toggleClass("button_active");
	});
	
	$('.tabsBlock').tabs();
	
	// functions
	
	function displayProgress(pc) {
			var degs = pc * 3.6+"deg";
			console.log(degs);
			//$('#zen .progress').css({rotate: degs}); 		
	}
});