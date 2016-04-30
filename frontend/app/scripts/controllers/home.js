'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:HomeCtrl
 * @description
 * # HomeCtrl
 * Controller of the frontendApp
 */
angular.module('frontendApp')
  .controller('HomeCtrl', function ($scope, apiService) {
    $scope.datasets = [];
    apiService.list('datasets').then(function(response){
      $scope.datasets = apiService.data['datasets'].list;
      angular.forEach($scope.datasets, function(item, index){
        if (item.name == 'bisphosphonatenyc')
          item.image = 'http://sedationdentallasvegas.com/wp-content/uploads/2015/02/oral-surgery-2.jpg';
        else if (item.name == 'populationdata')
          item.image ='http://img.freepik.com/free-vector/north-america-map_23-2147511621.jpg?size=338&ext=jpg&ve=1';
        else if (item.name == 'storm')
          item.image = 'http://www.siwallpaperhd.com/wp-content/uploads/2015/06/amazing_extreme_tornado_wallpaper_hd_7.jpg'
      })
    })
  });
