// Filter and sort parameters
var filter_param = $('#filter-param').val();
var sort_param = $('#sort-param').val();    

$(document).ready(function(){

    // Set 'Select' fields according to actual filter and sort parameters
    $('#filter-select').val(filter_param);
    $('#filter').val(filter_param);
    $('#sort-select').val(sort_param);
    $('#sort').val(sort_param);
    $('select').formSelect();

    // Reset search
    $("#empty-search").on("click",function(){
        window.location.href = "/eventually/search";
    });

    // Manually update filter parameter according to selected one (Materialize bug)
    $('#filter-select').change(function() {
        $('#filter-select').formSelect();
        var filter_value = $('#filter-select').formSelect('getSelectedValues');
        $('#filter').val(filter_value);
    });

    // Manually update sort parameter according to selected one (Materialize bug)
    $('#sort-select').change(function() {
        $('#sort-select').formSelect();
        var sort_value = $('#sort-select').formSelect('getSelectedValues');
        $('#sort').val(sort_value);
    });
 });