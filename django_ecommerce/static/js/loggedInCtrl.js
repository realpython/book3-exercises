mecApp.controller('LoggedInCtrl',function($scope) {
  $scope.show_badges = false;
  $scope.show_hide_label = "Show";

  $scope.show = function() {
    $scope.show_badges = ! $scope.show_badges;
    $scope.show_hide_label = ($scope.show_badges) ? 'Hide': 'Show';
    }
});
