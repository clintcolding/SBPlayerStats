$(document).ready(function(){
    $('ul.tabs li').click(function(){
        var tab_id = $(this).attr('data-tab');
        var pitching_table = $('#pitching-leaders').DataTable();
        var team_table = $('#team-leaders').DataTable();

        $('ul.tabs li').removeClass('current');
        $('.tab-content').removeClass('current');
        $(this).addClass('current');
        $("#"+tab_id).addClass('current');
        pitching_table.columns.adjust().draw();
        team_table.columns.adjust().draw();
    });
});