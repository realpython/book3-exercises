var pollsApp = angular.module('pollsApp',[]);

pollsApp.config(function($interpolateProvider){
        $interpolateProvider.startSymbol('[[')
        .endSymbol(']]');
    }
);


pollsApp.factory('pollFactory', function($http, $filter) {

  var baseUrl = '/api/v1/';
  var pollUrl = baseUrl + 'polls/';
  var pollItemsUrl = baseUrl + 'poll_items/';
  var pollId = 0;

  var pollFactory = {};

  pollFactory.getPoll = function() {
    var tempUrl = pollUrl;
    if (pollId != 0) { tempUrl = pollUrl + pollId; }
    return $http.get(pollUrl).then(function(response)
      {
        var latestPoll = $filter('orderBy')(response.data, '-publish_date')[0];
        pollId = latestPoll.id;
        return latestPoll;
      });
  };
  
  pollFactory.vote_for_item = function(poll_item) {
    poll_item.votes +=1;
    return $http.put(pollItemsUrl + poll_item.id, poll_item);
  }

  return pollFactory;
});

pollsApp.controller('UserPollCtrl',function($scope, $http, pollFactory) {

  //get the Poll
  $scope.poll = ""
  function setPoll(promise){
    $scope.poll = promise;
  };

  $scope.barcolor = function(i) {
    colors = ['progress-bar-success','progress-bar-info',
      'progress-bar-warning','progress-bar-danger','']
    idx = i % colors.length;
    return colors[idx];
  };

  pollFactory.getPoll().then(setPoll);

  $scope.vote = function(item) {
    pollFactory.vote_for_item(item) 
                        .then(pollFactory.getPoll)
                        .then(setPoll);
  };

});
