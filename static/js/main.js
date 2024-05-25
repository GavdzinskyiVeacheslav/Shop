$(function () {
const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
});

function add_to_fav(ad_id, flag){

   if(flag == 0){
    $('.rem_fav'+ad_id).addClass('d-none');
    $('.ad_fav'+ad_id).removeClass('d-none');
    delete fav_list['ad'+ad_id];
    localStorage.setItem('fav_list', JSON.stringify(fav_list));
   }else{
    fav_list['ad'+ad_id] = ad_id;
    $('.rem_fav'+ad_id).removeClass('d-none');
    $('.ad_fav'+ad_id).addClass('d-none');
      try {
        localStorage.setItem('fav_list', JSON.stringify(fav_list));
      } catch (e) {
        if (e == QUOTA_EXCEEDED_ERR) localStorage.clear();
      }
   }
}

function close_left_menu() {
    $('.search').css('display','none');
    $('.background-holder').css('display','none');
    $('.background-holder').css('z-index','19');
    $('section.container, .mobile_menu_bottom, footer, header').removeClass('blured');
    $('.mobile_menu').animate({
            left: '-100%'
        }, 200, function() {
        $('.mobile_categories_section').css({"display":"none"});
        $('.mobile_profile_section').css({"display":"none"});
        $('.mobile_menu_inner').css({"transform":"translateX(0%)"});
        $('.mobile_menu').scrollTop(0);
  });
    $('body').css('overflow-y','auto');
    $('.choose_city_modal').css('display','none');
    $('.mobile_menu').css({"overflow-y":"auto"});
//        $('.dropdown_select_city, .dropdown_select_per_page').animate({
//                left: '-100%'
//            }, 200, function() {
//    $('.dropdown_select_city, .dropdown_select_per_page').css({"display":"none"});
//  });
//  $('.mobile_profile').animate({
//                left: '-100%'
//            }, 200, function() {
//    $('.dropdown_select_city, .dropdown_select_per_page').css({"display":"none"});
//  });
}

function close_bottom_sheets() {
    $('.background-holder').css('display','none');
    $('.background-holder').css('z-index','19');
    $('section.container, .mobile_menu_bottom, footer, header').removeClass('blured');
    $('.open_bottom_sheet').animate( { top:"100%"} , 200, function() {
        $(this).css('display','none');
    });
    $('body').css('overflow-y','auto');
    $('html').css('overflow-y','auto');
    $('.open_bottom_sheet').removeClass( 'open_bottom_sheet' );
}

$(document).ready(function () {

$('#search_request').bind("input", function (e) {
    $('.search_clear_button').fadeIn();
});

$('#search_city_input').bind("input", function (e) {
    $('.search_city_clear_button').fadeIn();
});

$('body').on('click', '.search_block', function(e){
//    $('.search').css('display','flex');
    $('.search').attr('style', 'display: flex !important');
    $('.background-holder').css('display','block');
    $('.search input').focus();
    $('section.container, .mobile_menu_bottom, footer').addClass('blured');
});

$('body').on('click', '.background-holder, .close_search, .close_mobile_menu_button', function(e){
    close_left_menu();
    close_bottom_sheets();
});


$('body').on('click', '.mobile_menu_button', function(e){
    $('.mobile_menu').animate({
            left: '0'
        }, 200);
    $('.background-holder').css('z-index','38');
    $('.background-holder').css('display','block');
    $('section.container, .mobile_menu_bottom, footer, header').addClass('blured');
    $('body').css('overflow-y','hidden');
});

    var rTop;
    var detectTap = false;
    var te;
    var teEnd = null;
    var teStart = null;
    var detectMove = false;
    var detectMove1 = true;
    var sgknsfkgn;
    var blockHeight = $("#profile_bottom-sheet").height() + 100;
    var tops = $(window).height() - blockHeight;

$('body').on('click', '.bottom_item_profile_mobile', function(e){
//    $('.mobile_profile').animate({
//            left: '0'
//        }, 200);
    $('#profile_bottom-sheet').css('display','block');
    $("#profile_bottom-sheet").css( 'bottom', '0' );

    rTop = $(window).height() - $('.bottom_sheet_content').height() - 50;

    if (rTop < 100) {
        rTop = 100;
    }

    $("#profile_bottom-sheet").animate( { top:rTop} , 200 );

    $("#profile_bottom-sheet").addClass( 'open_bottom_sheet' );

    $('.background-holder').css('z-index','38');
    $('.background-holder').css('display','block');
    $('section.container, .mobile_menu_bottom, footer, header').addClass('blured');
    $('html').css('overflow-y','hidden');
    $('body').css('overflow-y','hidden');
});

$(document).on('touchstart',".bottom_sheet_content_scroll_block",function(e){
        detectTap = true;
        teStart = null;
        teEnd = null;

        if ($(this).scrollTop() == 0) {
            detectMove1 = true;
        }
        else {
            detectMove1 = false;
        }

    });

$(document).on('touchstart',".bottom_sheet",function(e){
        detectTap = true;
        teStart = null;
        teEnd = null;

        if (detectMove1) {
            detectMove = true;
        }
        else {
            detectMove = false;
        }

    });

$(document).bind('touchmove',function(e){
        var bs = $(this);
        if (detectTap == true) {
        if (detectMove == true) {

            if (teStart == null) {
                teStart = e.originalEvent.changedTouches[0].clientY;
            }
            te = e.originalEvent.changedTouches[0].clientY;
            teEnd = te - teStart;

            if (te > teStart) {
                sgknsfkgn = rTop + teEnd;
                $(".open_bottom_sheet").css("top",sgknsfkgn);
            }
        }
        }
    });

$(document).on('touchend',".bottom_sheet",function(e){
        detectTap = false;
        teEnd = te - teStart;

        if (detectMove == true && teStart != null) {

            if (teEnd > 100) {
                close_bottom_sheets();
            }
            else {
                $(this).animate( { top:rTop} , 200 );
            }
        }

        detectMove = false;
        detectMove1 = true;
        teStart = null;
        teEnd = null;
});

$('body').on('click', '.open_categories_menu', function(e){

//    var offsetTop = 130 - $('body').scrollTop();
    $(this).addClass('close_categories_menu');
    $(this).removeClass('open_categories_menu');
    $('body').css('overflow-y','hidden');
//    $('.drop-content').css('top',offsetTop);
    $('.drop-content').css('display','block');
    $('.back_holder').css('display','block');
    $('section.container, footer').addClass('blured');
});

$('body').on('click', '.back_holder, .close_categories_menu', function(e){
    $('.close_categories_menu').addClass('open_categories_menu');
    $('.close_categories_menu').removeClass('close_categories_menu');
    $('body').css('overflow-y','auto');
    $('.drop-content').css('display','none');
    $('.back_holder').css('display','none');
    $('section.container, footer').removeClass('blured');
    $('body').css('overflow-y','auto');
});

$('body').on('click', '.visual_list_button', function(e){
    document.cookie = "ads_visual=list;path=/";
    location.reload();
});

$('body').on('click', '.visual_grid_button', function(e){
    document.cookie = "ads_visual=grid;path=/";
    location.reload();
});


$('body').on('click', '.background_hold, .close_choose_city', function(e){
    $('.choose_city_block').css('display','none');
    $('body').css('overflow-y','auto');
    $('section.container, .top-header, header, .mobile_menu_bottom, .mobile_menu, footer').removeClass('blured');
});

$("#search_city_input").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $(".city_div").filter(function() {
       $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });

$('body').on('click', '.choose_city.close_dropdown', function(e){

    var width = $(window).width();
    var offsetTop = $(this).offset().top + $('body').scrollTop() + 40;
    var offsetLeft = $(this).offset().left;
    var offsetTopSpecial = offsetTop + $('header').height() - 65;


    var blockWidth = $('.page_services .choose_city').width() + 26;

    if (width > 768) {

        if (blockWidth > 0) {
            $('.dropdown_select_city').addClass('dropdown_select_city_service');
            $('.dropdown_select_city').css({"width":blockWidth});
            offsetTop = offsetTop + 6;
        }

        $('.dropdown_select_city').css({"display":"block"});
        $('.dropdown_select_city').css({"top":offsetTop});
        $('.special_version .dropdown_select_city').css({"top":offsetTopSpecial});
        $('.dropdown_select_city').css({"left":offsetLeft});

        $(this).removeClass("close_dropdown");
        $(this).addClass("open_dropdown");
        $(this).find('i').addClass("rotate_up");
    }
    else {
        $('.dropdown_select_city').css({"display":"block"});
//        $('.dropdown_select_city').animate({
//                left: '0'
//            }, 200);
    $('#cities_bottom_sheet').css('display','block');
    $("#cities_bottom_sheet.bottom_sheet:before").css('display','block');
    $("#cities_bottom_sheet").css( 'bottom', '0' );

    rTop = $(window).height() - $("#cities_bottom_sheet").find('.bottom_sheet_content').height() - 50;

    if (rTop < 100) {
        rTop = 100;
    }

    var heightScrollDiv = $(window).height() - $("#cities_bottom_sheet .mobile_menu_block_header").height() - $("#cities_bottom_sheet .search_city_input").height() - $("#cities_bottom_sheet .dropdown_select_city_buttons").height() - rTop - 20;

    $('.dropdown_select_list').css('height',heightScrollDiv);

    $("#cities_bottom_sheet").animate( { top:rTop} , 200 );

    $("#cities_bottom_sheet").addClass( 'open_bottom_sheet' );
        $('.background-holder').css('z-index','38');
        $('.background-holder').css('display','block');
        $('section.container, .mobile_menu_bottom, footer, header').addClass('blured');
        $('body').css('overflow-y','hidden');
        $('html').css('overflow-y','hidden');
    }

});

$('body').on('click', '.choose_records_per_page.close_dropdown', function(e){

    var width = $(window).width();
    var offsetTop = $(this).offset().top + $('body').scrollTop() + 40;
    var offsetLeft = $(this).offset().left;
    var offsetTopSpecial = offsetTop + $('header').height() - 65;

    if (width > 768) {
        $('.dropdown_select_per_page').css({"display":"block"});
        $('.dropdown_select_per_page').css({"top":offsetTop});
        $('.special_version .dropdown_select_per_page').css({"top":offsetTopSpecial});
        $('.dropdown_select_per_page').css({"left":offsetLeft});

        $(this).removeClass("close_dropdown");
        $(this).addClass("open_dropdown");
        $(this).find('i').addClass("rotate_up");
    }
    else {
        $('#records_bottom_sheet').css('display','block');
        $("#records_bottom_sheet").css( 'bottom', '0' );
        $('.dropdown_select_list').css('height','auto');

        rTop = $(window).height() - $("#records_bottom_sheet").find('.bottom_sheet_content').height() - 50;

        if (rTop < 100) {
            rTop = 100;
        }

        $("#records_bottom_sheet").animate( { top:rTop} , 200 );
//        $('.dropdown_select_per_page').css({"display":"block"});
//        $('.dropdown_select_per_page').animate({
//                left: '0'
//            }, 200);
        $("#records_bottom_sheet").addClass( 'open_bottom_sheet' );
        $('.background-holder').css('z-index','38');
        $('.background-holder').css('display','block');
        $('section.container, .mobile_menu_bottom, footer, header').addClass('blured');
        $('body').css('overflow-y','hidden');
        $('html').css('overflow-y','hidden');
    }

});

$('body').on('click', '.choose_city.open_dropdown, .choose_category.open_dropdown', function(e){
    $(this).removeClass("open_dropdown");
    $(this).addClass("close_dropdown");
    $(this).parent().find('.dropdown_select').css('display','none');
    $(this).find('i').removeClass("rotate_up");

});

$('body').on('click', '.choose_records_per_page.open_dropdown', function(e){
    $(this).removeClass("open_dropdown");
    $(this).addClass("close_dropdown");
    $(this).parent().find('.dropdown_select').css('display','none');
    $(this).find('i').removeClass("rotate_up");

});


$('body').on('click', '.city_div, .category_div', function(e){

    var width = $(window).width();
    var clickDiv = $(this);
    var count = 0;

    if (width > 768) {
        var cities = '';
        var chooseDiv = clickDiv.parent().parent().parent().find('.choose_block');
        var chooseSpanTitle = chooseDiv.find('.choose_block_title');
        $(".dropdown_select_city").find( "input:checkbox:checked" ).each(function() {
            count++;
            if (count == 1) { cities = $(this).parent().find('span').html(); }
            else if (count == 2) { cities = cities + ', ' + $(this).parent().find('span').html(); }
        });

        $('.mobile_select_city_confirm_button span').html(count);

    }
    else {
        clickDiv.parent().find( "input:checkbox:checked" ).each(function() {
            count++;
        });
        $('.mobile_select_city_confirm_button span').html(count);
    }


});

$('body').on('click', '.dropdown_select_city_service .city_div', function(e){
    var cities = '';
    var count = 0;
    $(".dropdown_select_city_service").find( "input:checkbox:checked" ).each(function() {
        if (count>0) {cities = cities + ', ';}
        cities = cities + $(this).parent().find('span').html();
        count++;
    });
    if (count == 0) {
        cities = 'Город не выбран';
    }
    $('.choose_city span').html(cities);
    calculate_total_cost();
});

$('body').on('click', '.clear_filter', function(e){
    var chooseBlock = $(this).parent().find('.choose_block');
    var chooseSpanTitle = chooseBlock.find('.choose_block_title');
    $(this).parent().removeClass('filter_active');
    chooseBlock.removeClass("open_dropdown");
    chooseBlock.addClass("close_dropdown");
    chooseSpanTitle.html('Выбрать город');
    $(this).parent().find( "input:checkbox:checked" ).each(function() {
        $(this).prop("checked", false);
    });
    $('.select_city_confirm_button').css('display','none');

});

$('body').on('click', '.share_button', function(e){
    $(this).children('div').fadeIn();
});

$('body').on('click', '.add_to_favorite_button', function(e){
    $(this).css('display','none');
    $('.remove_from_favorite_button').css('display','block');
});

$('body').on('click', '.remove_from_favorite_button', function(e){
    $(this).css('display','none');
    $('.add_to_favorite_button').css('display','block');
});

$('body').on('click', '.mobile_menu_profile_button', function(e){
//    $('.mobile_profile_section').css({"display":"block"});
//    $('.mobile_menu_inner').css({"transform":"translateX(-100%)"});
//    $('.mobile_menu').css({"overflow-y":"hidden"});
//    $('.mobile_menu').scrollTop(0);
close_left_menu();
 $('#profile_bottom-sheet').css('display','block');
    $("#profile_bottom-sheet").css( 'bottom', '0' );

    rTop = $(window).height() - $('.bottom_sheet_content').height() - 50;

    if (rTop < 100) {
        rTop = 100;
    }

    $("#profile_bottom-sheet").animate( { top:rTop} , 200 );

    $("#profile_bottom-sheet").addClass( 'open_bottom_sheet' );

    $('.background-holder').css('z-index','38');
    $('.background-holder').css('display','block');
    $('section.container, .mobile_menu_bottom, footer, header').addClass('blured');
    $('body').css('overflow-y','hidden');
    $('html').css('overflow-y','hidden');
});

$('body').on('click', '.mobile_menu_categories_button', function(e){
    $('.mobile_categories_section').css({"display":"block"});
    $('.mobile_menu_inner').css({"transform":"translateX(-100%)"});
    $('.mobile_menu').css({"overflow-y":"hidden"});
    $('.mobile_menu').scrollTop(0);
});

$('body').on('click', '.mobile_bottom_categories_button', function(e){
    $('.mobile_categories_section').css({"display":"block"});
    $('.mobile_menu_inner').css({"transform":"translateX(-100%)"});
    $('.mobile_menu').animate({
            left: '0'
        }, 200);
    $('.mobile_menu').css({"overflow-y":"hidden"});
    $('.background-holder').css('z-index','38');
    $('.background-holder').css('display','block');
    $('section.container, .mobile_menu_bottom, footer, header').addClass('blured');
    $('body').css('overflow-y','hidden');
});

$('body').on('click', '.bottom_item_profile_mobile', function(e){
//    $('.mobile_profile_section').css({"display":"block"});
//    $('.mobile_menu_inner').css({"transform":"translateX(-100%)"});
//    $('.mobile_menu').animate({
//            left: '0'
//        }, 200);
//    $('.mobile_menu').css({"overflow-y":"hidden"});
//    $('.background-holder').css('z-index','38');
//    $('.background-holder').css('display','block');
//    $('section.container, .mobile_menu_bottom, footer, header').addClass('blured');
//    $('body').css('overflow-y','hidden');
});

//$('body').on('click', '.card_user_name', function(e){
//    var width = $(window).width();
//
//    if (width <= 768) {
//    $('.mobile_profile_section').css({"display":"block"});
//    $('.mobile_menu_inner').css({"transform":"translateX(-100%)"});
//    $('.mobile_menu').animate({
//            left: '0'
//        }, 200);
//    $('.mobile_menu').css({"overflow-y":"hidden"});
//    $('.background-holder').css('z-index','38');
//    $('.background-holder').css('display','block');
//    $('section.container, .mobile_menu_bottom, footer, header').addClass('blured');
//    $('body').css('overflow-y','hidden');
//    }
//
//});



$('body').on('click', '.mobile_categories_section_item_back_button', function(e){
    $('.mobile_menu_inner').css({"transform":"translateX(0)"});
    $('.mobile_menu').css({"overflow-y":"auto"});
    $('.mobile_profile_section').css({"display":"none"});
    $('.mobile_categories_section').css({"display":"none"});
});

$('body').on('click', '.mobile_categories_section_item_subcategories_back_button', function(e){
    $('.mobile_menu_inner').css({"transform":"translateX(-100%)"});

});


$('body').on('click', '.mobile_categories_section_item_title', function(e){
    $('.mobile_categories_section_item_subcategories').css('display','none');
    $(this).parent().find('.mobile_categories_section_item_subcategories').css({"display":"block"});
    $('.mobile_menu_inner').css({"transform":"translateX(-200%)"});
});

$('body').on('change', '#service_add_link', function(e){
    if ($(this).prop('checked')) {
        $('.service_links_div').fadeIn();
    }
    else {
        $('.service_links_div').fadeOut();
    }
});



$('.sizeContent a').click(function() {
      if(!$(this).hasClass('active')){
        $("body").removeClass('large').removeClass('normal').removeClass('small');
        $("body").addClass($(this).data('size'));
        $('.sizeContent .active').removeClass('active');
        $(this).addClass('active');
        $.cookie('fontSize', $(this).data('size'), { expires: 30, path: '/' });
      }
});

$('.contrastContent a').click(function() {
      if(!$(this).hasClass('active')){
        $("body").removeClass('white').removeClass('black').removeClass('blue').removeClass('brown').removeClass('green');
        $("body").addClass($(this).data('contrast'));
        $('.contrastContent .active').removeClass('active');
        $(this).addClass('active');
        $.cookie('contrastScheme', $(this).data('contrast'), { expires: 30, path: '/' });
      }
});

$('.imgContent a').click(function() {
      if(!$(this).hasClass('active')){
        $("body").removeClass('noImg').removeClass('yesImg');
        $("body").addClass($(this).data('needimg'));
        $('.imgContent .active').removeClass('active');
        $(this).addClass('active');
        $.cookie('imgScheme', $(this).data('needimg'), { expires: 30, path: '/' });
      }
});

$(document).mouseup( function(e){ // событие клика по веб-документу
    var width = $(window).width();
    var div1 = $( ".dropdown_select_city" ); // тут указываем ID элемента
    var div1_button = $( ".choose_city" ); // тут указываем ID элемента
    var div2 = $( ".dropdown_select_per_page" ); // тут указываем ID элемента
    var div2_button = $( ".choose_records_per_page" ); // тут указываем ID элемента
    if ( !div1.is(e.target) && div1.has(e.target).length === 0
     && !div2.is(e.target) && div2.has(e.target).length === 0) { // и не по его дочерним элементам

    if (width > 768) {
			div1.hide(); // скрываем его
			div2.hide(); // скрываем его

			$('#search_city_input').val("");
            $( ".city_div" ).each(function() {
                $( this ).css('display','block');
            });
    }
            div1_button.find('i').removeClass("rotate_up");
            div2_button.find('i').removeClass("rotate_up");


            div1_button.removeClass("open_dropdown");
            div2_button.removeClass("open_dropdown");
            div1_button.addClass("close_dropdown");
            div2_button.addClass("close_dropdown");
            $('.share_button>div').fadeOut();
		}
	});


});

function clear_search() {
    $('#search_request').val('');
    $('.search_clear_button').css('display','none');
    $('#search_request').focus();
}

function clear_search_city() {
    $('#search_city_input').val('');
    $('.search_city_clear_button').css('display','none');
    $('#search_city_input').focus();
    $( ".city_div" ).each(function() {
                $( this ).css('display','block');
            });
}

function setSpecialVersion(special){
    $.post('/set_special', {
        special_version: special
    }, function(result) {
    if(result.ok){
        document.cookie = "ads_visual=list;path=/";
        document.location.reload();
    }

    });
}