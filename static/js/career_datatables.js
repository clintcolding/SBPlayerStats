$(document).ready(function() {
// Datatables for hitting
    $('#hitting').DataTable( {
        "order": [[ 0, "desc"]],
        "paging": false,
        "info": false,
        "searching": false,
        "scrollX": true,
        "aaSorting": []
    } );

// Datatables for pitching
    $('#pitching').DataTable( {
        "order": [[ 0, "desc"]],
        "paging": false,
        "info": false,
        "searching": false,
        "scrollX": true,
        "aaSorting": []
    } );
} );