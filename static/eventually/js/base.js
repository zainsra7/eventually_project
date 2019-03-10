$(document).ready(function(){
    $(".sidenav").sidenav();
    $('.tooltipped').tooltip();

    $("#login-btn").click(function(){
      $("#login-btn").hide();
      $("#login-form").show("slow");
    });

    $("#cancel-login-btn").click(function(){
      $("#login-form").hide("slow");
      $("#login-btn").show();
    });

    $("#login_send").click(function(){
      $("#login-form").submit();
    });
});