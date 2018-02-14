// Datatables for gain tracker
$(document).ready(function() {
    $('#team-gains').DataTable( {
        "order": [[ 0, "desc"]],
        "pageLength": 10,
        "paging": true,
        "info": true,
        "searching": true,
        "scrollX": true,
        "aaSorting": [],
        "columnDefs": [ {
            "targets": 10,
            "orderable": false
            } ]
    } );
} );