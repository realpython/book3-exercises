var mecApp = angular.module('mecApp', []);

mecApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[')
  .endSymbol(']]');
});


$(function() {

  $("#user_form").submit(function() {
    if ( $("#credit-card").is(":visible")) {
      var form = this;
      var card = {
        number:   $("#credit_card_number").val(),
        expMonth: $("#expiry_month").val(),
        expYear:  $("#expiry_year").val(),
        cvc:      $("#cvv").val()
      };

      Stripe.createToken(card, function(status, response) {
        if (status === 200) {
          console.log(status, response);
          $("#credit-card-errors").hide();
          $("#last_4_digits").val(response.card.last4);
          $("#stripe_token").val(response.id);
          form.submit();
        } else {
          // submit anyway
          form.submit();
          // $("#stripe-error-message").text(response.error.message);
          // $("#credit-card-errors").show();
          // $("#user_submit").attr("disabled", false);
        }
      });

      return false;

    }

    return true

  });

  $("#change-card a").click(function() {
    $("#change-card").hide();
    $("#credit-card").show();
    $("#credit_card_number").focus();
    return false;
  });

  //show status
  $("#show-achieve").click(function() {
    console.log("test")
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
