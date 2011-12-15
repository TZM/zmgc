$(document).ready(function(){

    // Local copy of jQuery selectors, for performance.
    var my_jPlayer = $("#jquery_jplayer");

    // Some options
    var opt_play_first = false, // If true, will attempt to auto-play the default track on page loads. No effect on mobile devices, like iOS.
        opt_auto_play = true; // Text when not playing

    // A flag to capture the first track
    var first_track = true;

    // Instance jPlayer
    my_jPlayer.jPlayer({
        ready: function () {
            $("#sound_captcha .track-default").click();
        },
        swfPath: "/ui/core/js/jPlayer/",
        cssSelectorAncestor: "#sound_captcha",
        supplied: "mp3",
        wmode: "window"
    });

    // Create click handler
    $("#sound_captcha .track").click(function(e) {
        my_jPlayer.jPlayer("setMedia", {
            mp3: $(this).attr("href")
        });
        if((opt_play_first && first_track) || (opt_auto_play && !first_track)) {
            // alert("if");
            my_jPlayer.jPlayer("play");
        }
        first_track = false;
        return false;
    });

});