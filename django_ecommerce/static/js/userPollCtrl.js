var pollsApp = angular.module('pollsApp',[]);

pollsApp.controller('UserPollCtrl', function($scope) {
  $scope.total_votes = 0;
  $scope.vote_data = {}


  $scope.vote = function(voteModel) {
    //$scope[voteModel] = $scope[voteModel] + 1;
    if (!$scope.vote_data.hasOwnProperty(voteModel)) {
      $scope.vote_data[voteModel]  = {"votes" :  0, "percent" : 0};
      $scope[voteModel]=$scope.vote_data[voteModel];
    }
    $scope.vote_data[voteModel]["votes"] = $scope.vote_data[voteModel]["votes"] + 1;
    $scope.total_votes = $scope.total_votes + 1;
    for (var key in $scope.vote_data) {
      item = $scope.vote_data[key];
      item["percent"] = item["votes"] / $scope.total_votes * 100;
    }
  };
});
