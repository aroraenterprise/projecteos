'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:DataCtrl
 * @description
 * # DataCtrl
 * Controller of the frontendApp
 */
angular.module('frontendApp')
  .controller('DataCtrl', function ($scope, apiService) {
    var pageSize = 100;
    $scope.items = apiService.storms;

    $scope.goNext = function(more){
      if (!apiService.ready)
        return;

      if (!apiService.params){
        apiService.params = {limit: pageSize};
      }
      if (!apiService.storms.list || more && apiService.storms.meta.more){
        apiService.listStorms().then(function(){
          $scope.items = apiService.storms;
        });
      }
    };

    $scope.goNext(false); // initial call
  });
