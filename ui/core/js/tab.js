jQuery(document).ready(function() {

    jQuery.fn.tabsBlock = function(){
        //Default Action
        jQuery(this).find(".tab_content").hide(); //Hide all content
        jQuery(this).find("ul.tabs li:first").addClass("active").show(); //Activate first tab
        jQuery(this).find(".tab_content:first").show(); //Show first tab content
        //On Click Event
        jQuery("ul.tabs li").click(function() {

            jQuery(this).parent().parent().find("ul.tabs li").removeClass("active"); //Remove any "active" class
            jQuery(this).addClass("active"); //Add "active" class to selected tab
            jQuery(this).parent().parent().find(".tab_content").hide(); //Hide all tab content
            var activeTab = jQuery(this).find("a").attr("href"); //Find the rel attribute value to identify the active tab + content
            jQuery(activeTab).show(); //To Fade in the active content, change ".show" to ".fadeIn"
            return false;
        });
        };//end function
        jQuery("div[class^='tabsBlock']").tabsBlock(); //Run function on any div with class name of "tabsBlock"
    });
