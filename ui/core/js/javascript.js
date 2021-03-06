/* Play sound file */
function play(file) {
    var embed = document.createElement("embed");
 
    embed.setAttribute('src', file);
    embed.setAttribute('hidden', true);
    embed.setAttribute('autostart', true);
 
    document.body.appendChild(embed);
	$('#captcha-table').find("input[type='text']:captcha").focus();
}
/* Browse: select all/none */
function select_checkboxes(elt, checked) {
  var form = $(elt).parents('form');
  form.find('table input:checkbox').each(function() {
    $(this).attr('checked', checked);
  });
}

/* Enable/Disable field */
function disable_field(checkbox, field_id) {
  var field = $(field_id);
  if ($(checkbox).is(':checked')) {
    field.attr('disabled', true);
  } else {
    field.removeAttr('disabled');
  }
}


/* Popup */
var popup_window;
function popup(url, width, height) {
  // try-catch for IE
  try {
    if (popup_window != undefined && popup_window.closed == false)
      popup_window.close();
  } catch (ex) { }
  options = "menubar=no, status=no, scrollbars=yes, resizable=yes, width=" + width + ", height=" + height;
  popup_window = window.open(url, 'itools_popup', options);
  return false;
}


/* For the addlink/addimage popups */
function tabme_show(event) {
  event.preventDefault();
  $(".tabme a").each(function() {
    $(this.hash).hide(); // Hide all divs
    $(this).removeClass("selected"); // Remove flag
  });
  $(this.hash).show('fast'); // Show selected div
  $(this).addClass("selected"); // Add flag
}

function tabme() {
  // Find a tab menu and hook it
  var tabs = $(".tabme a");
  if (tabs.length) {
    // Hide all divs at start
    tabs.each(function() { $(this.hash).hide(); });
    // But show a default one, the one in the URL first
    var hash = window.location.hash ? window.location.hash : tabs.eq(0).attr("hash");
    $(hash).show();
    $("a[hash=" + hash + "]").addClass("selected"); // Select the matching tab
    tabs.click(tabme_show); // Hook the onclick event
  }
}

/* Progress bar: startProgressBar() */
function startProgressBar()
{
  $("#progress-bar-box").css("display", "block");
  $("#progress-bar").progressbar();

  var intervalId = setInterval(
    function()
    {
      $.getJSON("/;upload_stats?upload_id=" + upload_id,
        function(data)
        {
          if (data == null || !data.valid_id)
          {
            clearInterval(intervalId);
            $("#progress-bar").progressbar("destroy");
            $("#progress-bar-box").css("display", "none")
            return;
          }
          var percent = Math.floor(data.percent);

          $("#progress-bar").progressbar("option", "value", percent);
          var toText = sizeToText(data.uploaded_size, data.total_size, percent);
          $("#upload-size").html(toText.uploaded_size + "/" + toText.total_size);
          $("#percent").html(toText.percent)
        });
    },
    1500);
}
$(document).ready(function($){
	$('#footer').stickyFooter({
		dropup_speed_show : 300, // Time (in milliseconds) to show a drop down
		dropup_speed_hide : 200, // Time (in milliseconds) to hide a drop down
		dropup_speed_delay : 200, // Time (in milliseconds) before showing a drop down
		footer_effect : 'hover_fade', // Drop down effect, choose between 'hover_fade', 'hover_slide', etc.
		showhidefooter : 'show', // Footer can be hidden when the page loads
		hide_speed : 1000, // Time to hide the footer (in milliseconds) if the 'showhidefooter' option is set to 'hide'
		hide_delay : 2000 // Time before hiding the footer (in milliseconds) if the 'showhidefooter' option is set to 'hide'
	});
});

///* Captcha reload */
//function load_captcha(callback) {
//  // Gets image and audio URLs by Ajax call
//  $.getJSON('${captcha}', function(json){
//    // Error message
//    if (json.error) {
//      alert(json.error);
//      return;
//    }
//
//    // Success messages
//    var img = $('img#captcha');
//    if (img.length === 0) {
//      var img = $('<img id="captcha" alt="captcha" title="captcha" />');
//      img.attr('src', json.img_src);
//      img.appendTo('#captcha-container');
//
//      $('#sound-captcha').attr('onclick', function(){
//        play(json.sound_src); // '${sound_captcha}'
//      });
//    }
//
//    // Calls the callback function back
//    callback();
//  });
//}