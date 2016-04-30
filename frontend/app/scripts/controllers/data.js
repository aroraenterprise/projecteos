'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:DataCtrl
 * @description
 * # DataCtrl
 * Controller of the frontendApp
 */
angular.module('frontendApp')
  .controller('DataCtrl', function ($scope, oldApiService) {
    oldApiService.storms.params = {limit: 100};
    $scope.items = oldApiService.storms.list;

    $scope.goNext = function(more){
      if (oldApiService.storms.list.length == 0 || more && oldApiService.storms.meta.more){
        oldApiService.list().then(function(){
          $scope.items = oldApiService.storms;
        });
      }
    };

    $scope.goNext(false); // initial call
  });
