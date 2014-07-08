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

mecApp.factory("UserFactory", function($http) {
  var factory = {}
  factory.register = function(user_data) {
    return $http.post("/api/v1/users", user_data).then(function(response)
      {
        return response.data;
      });
  }
  return factory;
});

mecApp.controller('RegisterCtrl',function($scope, $http, StripeFactory, UserFactory) {

  setToken = function(data) { 
    $scope.userform.last_4_digits = data.card.last4;
    $scope.userform.stripe_token = data.id;
    return $scope.userform;
  }

  logStripeErrors = function(error) {
    $scope.stripe_errormsg = error.message;
    throw ["There was an error processing the credit card"];
  }

  logRegisterErrors = function(errors) {
    $scope.register_errors = errors;
  }

  redirect_to_user_page = function(response) {
    if (response.errors) { 
          throw response.errors;
        } else { 
          window.location = response.url 
        }
  }

   $scope.register = function() {
    $scope.stripe_errormsg = "";
    $scope.register_errors = "";
    
    StripeFactory.createToken($scope.card)
                .then(setToken, logStripeErrors)
                .then(UserFactory.register)
                .then(redirect_to_user_page)
                .then(null,logRegisterErrors);
   }; 
});
