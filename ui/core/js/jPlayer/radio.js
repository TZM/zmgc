// JavaScript Document
$(document).ready(function(){

    var playItem = 0;

    var i = 0;
    var pl = $("#alt_pl dt");
    var myPlayList = new Array();
    for(i = 0; i < pl.length; i++)
    {
        myPlayList[i] = {name: pl.eq(i).children("a").text(), mp3: pl.eq(i).next().find(".download").attr("href")};
    }

    // Local copy of jQuery selectors, for performance.
    var jpPlayTime = $("#jplayer_play_time");
    var jpTotalTime = $("#jplayer_total_time");
    var jpStatus = $("#demo_status"); // For displaying information about jPlayer's status in the demo page

    $("#jquery_jplayer").jPlayer({
        ready: function() {
            //displayPlayList();
            playListInit(false); // Parameter is a boolean for autoplay.
            //demoInstanceInfo(this.element, $("#demo_info")); // This displays information about jPlayer's configuration in the demo page
        }
    })
    .jPlayer("onProgressChange", function(loadPercent, playedPercentRelative, playedPercentAbsolute, playedTime, totalTime) {
        jpPlayTime.text($.jPlayer.convertTime(playedTime));
        jpTotalTime.text($.jPlayer.convertTime(totalTime));

        //demoStatusInfo(this.element, jpStatus); // This displays information about jPlayer's status in the demo page
    })
    .jPlayer("onSoundComplete", function() {
        playListNext();
    });

    $("#jplayer_play").click(function(){
        if(!$("#alt_pl .playing").length)
        $("#alt_pl dt").eq(playItem).addClass("playing").next().addClass("playing");
    });

    $("#jplayer_previous").click( function() {
        playListPrev();
        $(this).blur();
        return false;
    });

    $("#jplayer_next").click( function() {
        playListNext();
        $(this).blur();
        return false;
    });


    function playListInit(autoplay) {
        if(autoplay) {
            playListChange( playItem );
        } else {
            playListConfig( playItem );
        }
    }

    function playListConfig( index ) {
        playItem = index;
        $("#jquery_jplayer").jPlayer("setFile", myPlayList[playItem].mp3);
    }

    function playListChange( index ) {
        playListConfig( index );
        $("#jquery_jplayer").jPlayer("play");
        $("#alt_pl .playing").removeClass("playing");
        $("#alt_pl dt").eq(index).addClass("playing").next().addClass("playing");
    }

    function playListNext() {
        var index = (playItem + 1 < myPlayList.length) ? playItem + 1 : 0;
        playListChange( index );
    }

    function playListPrev() {
        var index = (playItem-1 >= 0) ? playItem-1 : myPlayList.length-1;
        playListChange( index );
    }

    //  лик по названию песни в списке
    $("a.play").click(function(){
        var index = $(this).closest("dt").index();
        if(index > 1)
        index /= 2;
        playListChange(index);
        return false;
    });

    // ѕри наведении на название песни
    $("dl.playlist dt").mouseenter(function(){
        $(this).siblings().removeClass('active').end().next('dd').andSelf().addClass('active');
    });

    // ѕоказать/скрыть текст песни
    $(".show_text").click(function(){
        var this_link = $(this);
        var show_links = this_link.closest("dd").find(".show_text");
        var text = this_link.closest("dd").find(".songtext");
        if(text.is(":hidden"))
        {
            show_links.text("убрать текст");
            text.slideDown("fast");
        }
        else
        {
            text.slideUp("fast");
            show_links.text("показать текст");
        }
    });


});