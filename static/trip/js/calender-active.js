$(document).ready(function(){
    function init_calendar() {
        if ("undefined" != typeof $.fn.fullCalendar) {
            var e, f, a = new Date,
                b = a.getDate(),
                c = a.getMonth(),
                d = a.getFullYear(),
                g = $("#bootstrapModalFullCalendar").fullCalendar({
                    header: {
                        left: "prev,next today",
                        center: "title",
                        right: "month,agendaWeek,agendaDay"
                    },
                    selectable: !0,
                    selectHelper: !0,
                    select: function(a, b, c) {
                        $("#fc_create").click(), e = a, ended = b, $(".antosubmit").on("click", function() {
                            var a = $("#title").val();
                            return b && (ended = b), f = $("#event_type").val(), a && g.fullCalendar("renderEvent", {
                                title: a,
                                start: e,
                                end: b,
                                allDay: c
                            }, !0), $("#title").val(""), g.fullCalendar("unselect"), $(".antoclose").click(), !1
                        })
                    },
                    eventClick: function(event, jsEvent, view) {
                        $('#modalTitle').html(event.title);
                        $('#modalDescript').html(event.description);
                        $('#modalName').html(event.modalName);
                        $('#modalDateTime').html(event.modalDateTime);
                        $('#modalCallStatus').html(event.modalCallStatus);

                        $('#modalName_edit').val(event.modalName);
                        $('#modalDate_edit').val(moment(event.start, 'DD/MM/YYYY').format('DD/MM/YYYY'));
                        $('#modalTime_edit').val(moment(event.start, 'HH:mm A').format('HH:mm A'));
                        $('#edit_modalDescript').html(event.description);
                        console.log('modalCallStatus ==>>>',event.modalCallStatus);
                        if(event.modalCallStatus === 'No Connection'){
                            $('#edit-call-called').prop('checked',false);
                            $('#edit-call-not-pick').prop('checked', false);
                            $('#edit-call-no-connection').prop('checked', true);
                        } else if(event.modalCallStatus === 'Called') {
                            $('#edit-call-not-pick').prop('checked', false);
                            $('#edit-call-no-connection').prop('checked',false);
                            $('#edit-call-called').prop('checked',true);
                        } else {
                            $('#edit-call-called').prop('checked',false);
                            $('#edit-call-no-connection').prop('checked', false);
                            $('#edit-call-not-pick').prop('checked',true);
                        }
                        $('#fullCalModal').modal();
                        return false;
                    },
                    editable: true,
                    events:
                    [
                        {
                           "title":"Call Sajjad",
                           'modalName':'Sajjad Kamal',
                           'modalDateTime':'July 10, 2016 @ 5:00 PM',
                           'modalCallStatus':'No Connection',
                           "allday":"false",
                           "description":"At vero eos et accusamus et iusto odio  dignissimos ducimus qui blanditiis  praesentium voluptatum deleniti atque",
                           "start":moment('23/01/2018 04:10 AM', 'DD/MM/YYYY HH:mm A'),
                           "end":moment('23/01/2018 05:10 PM', 'DD/MM/YYYY HH:mm A'),
                        },
                        {
                           "title":"Call Sajjad",
                           'modalName':'Sajjad Kamal',
                           'modalDateTime':'July 10, 2016 @ 5:00 PM',
                           'modalCallStatus':'No Connection',
                           "allday":"false",
                           "description":"At vero eos et accusamus et iusto odio  dignissimos ducimus qui blanditiis  praesentium voluptatum deleniti atque",
                           "start":moment('13/02/2018 04:10 AM', 'DD/MM/YYYY HH:mm A'),
                           "end":moment('15/02/2018 07:10 PM', 'DD/MM/YYYY HH:mm A'),
                        },
                       {
                          "title":"Call Sajjad3",
                          'modalName':'Sajjad Kamal',
                          'modalDateTime':'July 10, 2016 @ 5:00 PM',
                          'modalCallStatus':'Called',
                          "allday":"false",
                          "description":"At vero eos et accusamus et iusto odio  dignissimos ducimus qui blanditiis  praesentium voluptatum deleniti atque",
                          "start":moment('29/01/2018 04:10 AM', 'DD/MM/YYYY HH:mm A'),
                          "end":moment('29/01/2018 07:10 PM', 'DD/MM/YYYY HH:mm A'),
                       },
                       {
                        "title":"Call Sajjad",
                        'modalName':'Sajjad Kamal',
                        'modalDateTime':'July 10, 2016 @ 5:00 PM',
                        'modalCallStatus':'No Connection',
                        "allday":"false",
                        "description":"At vero eos et accusamus et iusto odio  dignissimos ducimus qui blanditiis  praesentium voluptatum deleniti atque",
                        "start":moment('23/02/2018 04:10 AM', 'DD/MM/YYYY HH:mm A'),
                        "end":moment('25/02/2018 07:10 PM', 'DD/MM/YYYY HH:mm A'),
                     },
                     {
                        "title":"Call Sajjad",
                        'modalName':'Sajjad Kamal',
                        'modalDateTime':'July 10, 2016 @ 5:00 PM',
                        'modalCallStatus':'No Connection',
                        "allday":"false",
                        "description":"At vero eos et accusamus et iusto odio  dignissimos ducimus qui blanditiis  praesentium voluptatum deleniti atque",
                        "start":moment('27/02/2018 04:10 AM', 'DD/MM/YYYY HH:mm A'),
                        "end":moment('27/02/2018 07:10 PM', 'DD/MM/YYYY HH:mm A'),
                     },
                     {
                        "title":"Call Sajjad",
                        'modalName':'Sajjad Kamal',
                        'modalDateTime':'July 10, 2016 @ 5:00 PM',
                        'modalCallStatus':'No Connection',
                        "allday":"false",
                        "description":"At vero eos et accusamus et iusto odio  dignissimos ducimus qui blanditiis  praesentium voluptatum deleniti atque",
                        "start":moment('27/03/2018 04:10 AM', 'DD/MM/YYYY HH:mm A'),
                        "end":moment('27/03/2018 07:10 PM', 'DD/MM/YYYY HH:mm A'),
                     },
                     {
                        "title":"Call Sajjad",
                        'modalName':'Sajjad Kamal',
                        'modalDateTime':'July 10, 2016 @ 5:00 PM',
                        'modalCallStatus':'No Connection',
                        "allday":"false",
                        "description":"At vero eos et accusamus et iusto odio  dignissimos ducimus qui blanditiis  praesentium voluptatum deleniti atque",
                        "start":moment('27/03/2018 04:10 AM', 'DD/MM/YYYY HH:mm A'),
                        "end":moment('27/03/2018 07:10 PM', 'DD/MM/YYYY HH:mm A'),
                     },
                    ]
                })
        }
    }
    init_calendar()
});
