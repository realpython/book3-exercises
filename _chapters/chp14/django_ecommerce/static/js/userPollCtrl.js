var pollsApp = angular.module('pollsApp',[]);

pollsApp.config(function($interpolateProvider){
  $interpolateProvider.startSymbol('[[')
  .endSymbol(']]');
});

pollsApp.controller('UserPollCtrl', function($scope, $http) {

  $scope.total_votes = 0;

  $scope.vote = function(item) {
    item.votes = item.votes + 1;
    $scope.total_votes = $scope.total_votes + 1;

    for (i in $scope.poll.items){
      var temp_item = $scope.poll.items[i];
      temp_item.percentage = temp_item.votes / $scope.total_votes * 100;
    }
  };

  // Get the Poll
  $scope.poll = ""

  $http.get('/api/v1/polls/1').
    success(function(data){
      $scope.poll = data;
    }).
    error(function(data,status) {
      console.log("calling /api/v1/polls/1 returned status " + status);
  });

});