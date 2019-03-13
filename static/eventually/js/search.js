$(document).ready(function(){
    $('.dropdown-button').dropdown();

    $("#empty-search").on("click",function(){
        window.location.href = "/eventually/search";
    });
 });