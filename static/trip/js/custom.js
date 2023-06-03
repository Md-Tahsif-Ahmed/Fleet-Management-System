$(document).ready(function(){
    "use strict";
    /*select tab content*/
    $('#mySelect').on('change', function (e) {
        $('#myTab li a').eq($(this).val()).tab('show');
    });

    /*daterangeselect*/

    $('.daterange-input').each(function(){
        var startDateValue = $(this).attr('data-startDate');
        var endDateValue = $(this).attr('data-endDate');
        var openPosition = $(this).attr('data-openPosition')
        $(this).daterangepicker({
            "startDate": startDateValue,
            "endDate": endDateValue,
            locale: {
             format: 'DD/MM/YYYY'
            },
            "opens": openPosition,
        });
    })

    // $('.daterange-input').daterangepicker({
    //     //"startDate": "07/11/2017",
    //     //"endDate": "07/17/2017",
    //     locale: {
    //      format: 'DD/MM/YYYY'
    //     },
    //     "opens": "left",
    // });


    /*daterangeselect*/
    //var currentDate;
    $('.daterange-input-single').daterangepicker({
        timePicker: true,
        timePickerIncrement: 5,
        locale: {
         format: 'DD/MM/YYYY H:mm A'
        },
      // viewMode: 'days',
       singleDatePicker: true,
       todayHighlight: true,
       drops: "down",
        minDate: '01/01/2012',
        maxDate: '12/12/2018'
       // currently picked date
   });

    if($('.datepicker-time-input').length){
        $('.datepicker-time-input').datetimepicker({
            format: 'hh:mm A'
        });
    }

    /****************************
    **  Sidebar Toggle
    *****************************/
    $('#sidebar__humbarger').on('click', function(){
        $('.sidebar').toggleClass('sidebar__toggle');
        $('.main-content-outer').toggleClass('main-content-outer__toggle');
    });
    /*** =====================================
    * 	Mobile Menu
    * =====================================***/
	$('.sidebar-menu .has-submenu').on('click', function(e) {
	  	e.preventDefault();
	    var $this = $(this);
	    if ($this.next().hasClass('menu-show')) {
	        $this.next().removeClass('menu-show');
	        $this.next().slideUp(350);
	    } else {
	        $this.parent().parent().find('li .dropdown').removeClass('menu-show');
	        $this.parent().parent().find('li .dropdown').slideUp(350);
	        $this.next().toggleClass('menu-show');
	        $this.next().slideToggle(350);
	    }
	});
    /****************************
    **  vault close
    *****************************/
    $('.vault-close-icon').on('click', function(){
        $(this).parents('.vault-close-terget').fadeOut();
    });
    /****************************
    **  vault close
    *****************************/
    $('#leads-filter-select').change(function(){
        var value = $(this).val();
        if(value = 'create-new-filter'){
            $('.leads-list-filter-result').fadeIn();
        }
        else {
            $('.leads-list-filter-result').fadeOut();
        }
    });

    /****************************
    **  commissions Add
    *****************************/
    $('.add-commissions-wrap').hide();
    $('#commissions-terget').on('click', function(e){
        e.preventDefault();
        $(this).hide();
        $('.add-commissions-wrap').show();
    });
    $('.add-commissions-wrap').submit(function(){
        $(this).hide();
        $('#commissions-terget').show();
    });
    /****************************
    **  Preloader
    *****************************/
    window.onload = (function(onload) {
        return function(event) {
            onload && onload(event);

            $(".loading-overlay .spinner").fadeOut(300),
                $(".loading-overlay").fadeOut(300);
                $("body").css({
                    overflow: "auto",
                    height: "auto",
                    position: "relative"
                })
        }
    }(window.onload));
    /****************************
    **  Triplist update
    *****************************/
    $('.triplist-table .triplist-update-button').click(function(e){
        e.preventDefault();
        $(this).parents('tr').find('.triplist-table-not-left').eq(0).hide(0);
        $(this).parents('tr').find('.triplist-date-picker').eq(0).show(0);
        $(this).parents('tr').find('.triplist-actions-buttons .triplist-save-button').removeClass('button-hide');
        $(this).parents('tr').find('.triplist-actions-buttons .triplist-cancle-button').removeClass('button-hide');
        $(this).parents('tr').find('.triplist-actions-buttons .triplist-update-button').addClass('button-hide');
    });
    /****************************
    **  Triplist Cancel
    *****************************/
    $('.triplist-table .triplist-cancle-button').click(function(e){
        e.preventDefault();
        $(this).parents('tr').find('.triplist-table-not-left').eq(0).show(0);
        $(this).parents('tr').find('.triplist-date-picker').eq(0).hide(0);
        $(this).parents('tr').find('.triplist-actions-buttons .triplist-save-button').addClass('button-hide');
        $(this).parents('tr').find('.triplist-actions-buttons .triplist-cancle-button').addClass('button-hide');
        $(this).parents('tr').find('.triplist-actions-buttons .triplist-update-button').removeClass('button-hide');
    });
    /****************************
    **  Vehicle Driver update
    *****************************/
    $('.vehiclesdriver-table .triplist-update-button').click(function(e){
        e.preventDefault();
        $(this).parents('tr').find('.drivertable-driver-name').hide(0);
        $(this).parents('tr').find('.drivertable-driver-select').show(0);
        $(this).parents('tr').find('.triplist-actions-buttons .triplist-save-button').removeClass('button-hide');
        $(this).parents('tr').find('.triplist-actions-buttons .triplist-cancle-button').removeClass('button-hide');
        $(this).parents('tr').find('.triplist-actions-buttons .triplist-update-button').addClass('button-hide');
    });
    /****************************
    **  Vehicle Driver  Cancle
    *****************************/
    $('.vehiclesdriver-table .triplist-cancle-button').click(function(e){
        e.preventDefault();
        $(this).parents('tr').find('.drivertable-driver-name').show(0);
        $(this).parents('tr').find('.drivertable-driver-select').hide(0);
        $(this).parents('tr').find('.triplist-actions-buttons .triplist-save-button').addClass('button-hide');
        $(this).parents('tr').find('.triplist-actions-buttons .triplist-cancle-button').addClass('button-hide');
        $(this).parents('tr').find('.triplist-actions-buttons .triplist-update-button').removeClass('button-hide');
    });
    /****************************
    **  Change Triplist update
    *****************************/
    $('.change-triplist-table .triplist-update-button').click(function(e){
        e.preventDefault();
        $(this).parents('tr').find('.triplist-table-not-left').hide(0);
        $(this).parents('tr').find('.triplist-date-picker').show(0);
        $(this).parents('tr').find('.triplist-actions-buttons .triplist-save-button').removeClass('button-hide');
        $(this).parents('tr').find('.triplist-actions-buttons .triplist-cancle-button').removeClass('button-hide');
        $(this).parents('tr').find('.triplist-actions-buttons .triplist-update-button').addClass('button-hide');
    });
    /****************************
    ** Change Triplist Cancel
    *****************************/
    $('.change-triplist-table .triplist-cancle-button').click(function(e){
        e.preventDefault();
        $(this).parents('tr').find('.triplist-table-not-left').show(0);
        $(this).parents('tr').find('.triplist-date-picker').hide(0);
        $(this).parents('tr').find('.triplist-actions-buttons .triplist-save-button').addClass('button-hide');
        $(this).parents('tr').find('.triplist-actions-buttons .triplist-cancle-button').addClass('button-hide');
        $(this).parents('tr').find('.triplist-actions-buttons .triplist-update-button').removeClass('button-hide');
    });

});
