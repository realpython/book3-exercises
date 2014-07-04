var mecApp = angular.module('mecApp',[]);

mecApp.config(function($interpolateProvider, $httpProvider){
  $interpolateProvider.startSymbol('[[')
        .endSymbol(']]');
  $httpProvider.defaults.headers.common['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
    }
);

