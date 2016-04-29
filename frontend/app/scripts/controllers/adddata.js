'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:AdddataCtrl
 * @description
 * # AdddataCtrl
 * Controller of the frontendApp
 */
angular.module('frontendApp')
  .controller('AddDataCtrl', function ($scope) {
    $scope.show = {
      new: true,
      existing: false
    };

    $scope.data = {
      email: 'saj.arora@nyu.edu',
      name: 'Storm',
      description: 'Storm data from NOAA for United States since 1995.',
      file: 'https://drive.google.com/open?id=0By0A1Jdf2gSMS0UtNnphSGJ3RU0'
    };

  });
