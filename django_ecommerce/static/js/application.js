$(function() {

  var mecApp = angular.module('mecApp',[]);

  mecApp.config(function($interpolateProvider, $httpProvider) {
    $interpolateProvider.startSymbol('[[')
          .endSymbol(']]');
    $httpProvider.defaults.headers.common['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
      }
  );

  $("#change-card a").click(function() {
    $("#change-card").hide();
    $("#credit-card").show();
    $("#credit_card_number").focus();
    return false;
  });

  //show status
  $("#show-achieve").click(function() {
    a = $("#achievements");
    l = $("#show-achieve");
    if (a.hasClass("hide")) {
       a.hide().removeClass('hide').slideDown('slow');
       l.html("Hide Achievements");
    } else {
       a.addClass("hide");
       l.html("Show Achievements");
    }
    return false;
  });

});
