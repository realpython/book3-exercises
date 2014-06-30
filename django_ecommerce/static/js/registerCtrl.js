/*
mecApp.factory('pollFactory', function($http, $filter) {

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
*/
mecApp.controller('RegisterCtrl',function($scope) {

 $scope.register = function() {
  console.log( "before submit");
 } 

});
