mecApp.controller('UserMapCtrl', function($scope) {

  $scope.map = {
    center: {
        latitude: 38.062056,
        longitude: -122.643380
    },
    zoom: 14,
    options: {
      mapTypeId: google.maps.MapTypeId.HYBRID,
    }
  };

});