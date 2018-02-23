$(document).ready(function() {
// Datatables for hitting
    $('#hitting').DataTable( {
        "order": [[ 10, "desc"]],
        "paging": false,
        "info": false,
        "searching": false,
        "scrollX": true,
        "aaSorting": []
    } );

// Datatables for pitching
    $('#pitching').DataTable( {
        "order": [[ 3, "desc"]],
        "paging": false,
        "info": false,
        "searching": false,
        "scrollX": true,
        "aaSorting": []
    } );

// Datatables for team
    $('#team').DataTable( {
        "order": [[ 0, "desc"]],
        "pageLength": 25,
        "paging": false,
        "info": false,
        "searching": false,
        "scrollX": true,
        "aaSorting": []
    } );
} );