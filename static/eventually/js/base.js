$(document).ready(function(){
    $(".sidenav").sidenav();
    $('.tooltipped').tooltip();

    $(".login-btn").click(function(){
      document.getElementById('login-modal').style.display='block';
      $(".sidenav").sidenav();
    });
    $(".cancel-btn").click(function(){
      document.getElementById('login-modal').style.display='none';
    });
    $("#id_email").attr("placeholder", "Please enter your UOG email address");
});