$(document).ready(function(){
    "use strict";
    $('.drag-item').draggable({
        cursor: 'move',
        helper: "clone",
    });
    $('.task-table__body').droppable({
        drop: function(event, ui) {
            $( ui.draggable ).appendTo( this );
        }
    });
});
