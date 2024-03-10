$(document).ready(function(){
    $("#heart").click(function(){
      if($("#heart").hasClass("liked")){
        $("#heart").html('<i class="fa-regular fa-heart"></i>');
        $("#heart").removeClass("liked");
      }else{
        $("#heart").html('<i class="fa-solid fa-heart"></i>');
        $("#heart").addClass("liked");
      }
    });
  });