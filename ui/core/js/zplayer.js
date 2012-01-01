$(document).ready(function(){
  $("div#panel").slideUp(0);
  ///init screen
  var total_length=$(".jp-type-playlist .jp-playlist ul .list").length;
  var init_point = new Array(3);
  init_point[0]=0;
  var list_length = new Array(3);
  var title = new Array(3);
  var mp = new Array(3);
  var oga = new Array(3);
  var m4v = new Array(3);
  var ogv = new Array(3);
  var webmv = new Array(3);
  var init_flag = 0; 
  for(i=1; i<4; i++)
  {
    list_length[i] = $(".jp-type-playlist .jp-playlist #tabs-"+i+" ul .list").length;
    title[i] = new Array(list_length[i]);
    mp[i] = new Array(list_length[i]);
    oga[i] = new Array(list_length[i]);
    m4v[i] = new Array(list_length[i]);
    ogv[i] = new Array(list_length[i]);
    webmv[i] = new Array(list_length[i]);
    init_point[i-1]=init_flag; 

    for(j=0; j< list_length[i] ; j++)
    {
      title[i][j] = $(".jp-type-playlist .jp-playlist #tabs-"+i+" ul .list").eq(j).text();
      mp[i][j] = $(".jp-type-playlist .jp-playlist #tabs-"+i+" ul .list a").eq(j).attr("mp");
      oga[i][j] = $(".jp-type-playlist .jp-playlist #tabs-"+i+" ul .list a").eq(j).attr("oga");
      m4v[i][j] = $(".jp-type-playlist .jp-playlist #tabs-"+i+" ul .list a").eq(j).attr("m4v");
      ogv[i][j] = $(".jp-type-playlist .jp-playlist #tabs-"+i+" ul .list a").eq(j).attr("ogv");
      webmv[i][j] = $(".jp-type-playlist .jp-playlist #tabs-"+i+" ul .list a").eq(j).attr("webmv");
      init_flag++;
    }
  }
  ///initial player with empty playlist
  var myPlaylist = new jPlayerPlaylist({
    jPlayer: "#jquery_jplayer_1",
    cssSelectorAncestor: "#jp_container_1"
    }, [

    ], {
      swfPath: "/ui/core/js/jPlayer",
      supplied: "oga, mp3,m4v,ogv,webmv",
      wmode: "window"
    }
  );
  ///add media list into the playlsit
  for(i=1; i<4; i++)
  {
    for(j=0; j< list_length[i] ; j++)
    {
      myPlaylist.add({
        title: title[i][j],
        mp3: mp[i][j],
        oga: oga[i][j],
        m4v: m4v[i][j],
        ogv: ogv[i][j],
        webmv: webmv[i][j]
      });
    }
  }
  for(k=list_length[1]; k < total_length; k++) 
  {
    $(".jp-type-playlist .jp-playlist #tabs-1 ul li").eq(k).hide();
  }
  /// we don't want to display the player on load time
  $("#jquery_jplayer_1").jPlayer("option","size",{width:320, height:270});

  /// slide action for the control panel
  $(".btn-slide").click(function(){
    $("#panel").slideToggle("fast");
    $(this).toggleClass("active"); return false;
  });

  //tab switch
  $(".tabs li").click(function(){

    var divname = $(this).children().attr("title");
    var divindex = $(this).children().attr("index");

    jQuery(this).parent().parent().find("ul.tabs li").removeClass("active"); //Remove any "active" class
    jQuery(this).addClass("active"); 
    //Add "active" class to selected tab

    for(l = 0; l< init_point[divindex-1];l++)
    {
      $(".jp-type-playlist .jp-playlist #tabs-"+divindex+" ul li").eq(l).hide();
    }	
    for(m = init_point[divindex]; m< total_length; m++)
    {
      $(".jp-type-playlist .jp-playlist #tabs-"+divindex+" ul li").eq(m).hide();
    }	

    $(".tab-item").parent().css({ "display" : "none"});
    $("#"+divname).parent().css({ "display" : "block"});
  });

});