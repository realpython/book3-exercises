var adminApp = angular.module('adminApp',['ui.bootstrap']);

adminApp.config(function($interpolateProvider, $httpProvider){
  $interpolateProvider.startSymbol('[[')
        .endSymbol(']]');
  $httpProvider.defaults.headers.common['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
    }
);

adminApp.factory("AdminUserFactory", function($http) {
  var factory = {}
  factory.resetPassword = function(data) {
    console.log("in the factory");
    var pwdData = {password : data.pass, password2 : data.pass2} 
    return $http.put("/api/v1/users/password/" + data.user, pwdData)
        .then(function(response)
        {
          return response;
        });
  }

  return factory;
});

adminApp.controller('AdminCtrl', function($scope, $http, AdminUserFactory) {

  $scope.afterReset = false;
  $scope.isopen = false;

  $scope.resetpass = function(userId) {
    $scope.afterReset = false;
    data = {'user': userId,
            'pass' : $scope.pass,
            'pass2': $scope.pass2,}
    AdminUserFactory.resetPassword(data)
      .then(showAlert,showAlert);
   
  }

  var showAlert = function(data) {
    $scope.afterReset = true;
    var msg = "";
    $scope.alertClass = "alert-danger";

    if (data.status == 200) {
      $scope.alertClass = "alert-success";
      $scope.pass = "";
      $scope.pass2 = "";
    }
    
    if (typeof data.data == 'string') {
      msg = data.data;
    } else {
      for (x in data.data) {
        msg += data.data[x].toString() + " ";
      }
    }

    $scope.msg = msg;
    $scope.isopen = false;
  }

});
