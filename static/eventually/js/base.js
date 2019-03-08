$(document).ready(function(){
    $(".sidenav").sidenav();

    $("#login-btn").click(function(){
      $("#login-btn").hide();
      $("#login-form").show("slow");
    });

    $("#cancel-login-btn").click(function(){
      $("#login-form").hide("slow");
      $("#login-btn").show();
    });
});