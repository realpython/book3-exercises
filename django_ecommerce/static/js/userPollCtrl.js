var pollsApp = angular.module('pollsApp',[]);

pollsApp.controller('UserPollCtrl', function($scope, $http) {
  //$scope.total_votes = 0;

  //get the Poll
  $scope.poll = ""
  $scope.barcolor = function(i) {
    colors = ['progress-bar-success','progress-bar-info',
      'progress-bar-warning','progress-bar-danger','']
    idx = i % colors.length;
    return colors[idx];
  }

  $http.get('/api/v1/polls/1').success(function(data){
    $scope.poll = data;
  }).
  error(function(data,status){
    console.log("calling /api/v1/polls/1 returned status " + status);
  });


  $scope.vote = function(item) {
    item.votes +=1;
    $http.put('/api/v1/poll_items/'+item.id,item).
    success(function(data){
      $http.get('/api/v1/polls/1').success(function(data){
        $scope.poll = data;
      }).
      error(function(data,status){
        console.log("calling /api/v1/polls/1 returned status " + status);
      });
    }).
    error(function(data,status){
      console.log("calling PUT /api/v1/poll_items returned status " + status);
    });


   /* item.votes = item.votes + 1;
    $scope.total_votes = $scope.total_votes + 1;

    for (i in $scope.poll.items){
      var temp_item = $scope.poll.items[i];
      temp_item.percentage = temp_item.votes / $scope.total_votes * 100;
    }*/
  };
});
