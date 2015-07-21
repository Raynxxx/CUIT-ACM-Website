/**
 * Created by rayn on 3/18 2015.
 */

// Back To Top
$(document).ready(function ($) {
    var offset = 300;
    var offset_opacity = 1200;
    var scroll_top_duration = 700;
    var $top = $('.back_to_top');

    $(window).scroll(function() {
        ( $(this).scrollTop() > offset ) ?
            $top.addClass('visible') :
            $top.removeClass('visible fade-out');
        if ( $(this).scrollTop() > offset_opacity ) {
            $top.addClass('fade-out');
        }
    });

    $top.click( function() {
        $('body,html').animate({scrollTop: 0}, scroll_top_duration);
        return false;
    });
});

// Active Link

function gaoActiveLink(item) {
    $(item).each(function() {
        if ($($(this))[0].href == String(window.location)) {
            $(this).parent().addClass('active').click(function(){
                return false;
            });
        } else {
            $(this).parent().removeClass('active');
        }
    });
}
$(document).ready(function() {
    gaoActiveLink('.sidebar-menu > li a');
    gaoActiveLink('.navbar-nav > li a');
});

// In the cur page, links refer to this page is not work
$(document).ready(function() {
    $('a').each(function() {
        if ($($(this))[0].href == String(window.location)) {
            $(this).click(function() {
                return false;
            });
        }
    });
});

function requiredCheck(field, info) {
    if (field.val() == "") {
        field.focus();
        field.attr('placeholder', info + "不能留空");
        return false;
    }
    return true;
}