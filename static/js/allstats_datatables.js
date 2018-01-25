$(document).ready(function() {
// Datatables for hitting
    $('#hitting').DataTable( {
        "order": [[ 11, "desc"]],
        "pageLength": 25,
        "paging": true,
        "info": true,
        "searching": true,
        "scrollX": true,
        "aaSorting": []
    } );

// Datatables for pitching
    $('#pitching').DataTable( {
        "order": [[ 4, "asc"]],
        "pageLength": 25,
        "paging": true,
        "info": true,
        "searching": true,
        "scrollX": true,
        "aaSorting": []
    } );

// Datatables for team
    $('#team').DataTable( {
        "order": [[ 0, "desc"]],
        "pageLength": 25,
        "paging": true,
        "info": true,
        "searching": true,
        "scrollX": true,
        "aaSorting": []
    } );
} );