mecApp.factory('locations', function($http) {
 
  var locsUrl = '/api/v1/user_locations';

  return {
    getAll: /*function() {return $http.get(locsUrl);}, */
      function() { return $http.get(locsUrl).then(function(response) {
                      return response.data; 
                    });
    },
  };

});

mecApp.controller('UserMapCtrl', function($scope, locations) {
  $scope.map = {
    center: {
        latitude: 38.062056, 
        longitude: -122.643380
  38.062056,-122.643380]
38.062056,-122.643380


db.user_location.update({_id:ObjectId("53f6d89059b1e9d1493bea5f"), {$set : {"email" : "nnn@nn.com", "name" : "nnn", "location" : { "type" : "Point", "coordinates" : [38.062056, -122.643380] }, "mappoint_id" : 6 }}});



    },
    zoom: 2,
    options: { 
      mapTypeId: google.maps.MapTypeId.HYBRID,
    }
  };

  //get all the user locations
  $scope.locs = [];
  cache = function(locs){
    $scope.locs = locs;
    console.log($scope.locs)
  }

  locations.getAll().then(cache);
});
