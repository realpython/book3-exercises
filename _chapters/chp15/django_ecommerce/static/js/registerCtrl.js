mecApp.controller('RegisterCtrl', function($scope, StripeFactory) {

  setToken = function(data) {
    $scope.userform.last_4_digits = data.card.last4;
    $scope.userform.stripe_token = data.id;
  }

  logStripeErrors = function(error) {
    $scope.stripe_errormsg = error.message;
  }

   $scope.register = function() {
    $scope.stripe_errormsg = "";
    StripeFactory.createToken($scope.card)
                .then(setToken, logStripeErrors);
   };

});

mecApp.factory("StripeFactory", function($q, $rootScope) {

  var factory = {}
  factory.createToken = function(card) {
    var deferred = $q.defer();

      Stripe.createToken(card, function(status, response) {
        $rootScope.$apply(function() {
          if (response.error) return deferred.reject(response.error);
          return deferred.resolve(response);
        });
      });

    return deferred.promise;
  }
  return factory;
});