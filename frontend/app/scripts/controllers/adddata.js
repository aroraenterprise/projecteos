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
      files: ['https://www.dropbox.com/s/8gg4bubpaf16whj/StormEvents_details-ftp_v1.0_d2016_c20160419.csv?dl=1']
    };

    $scope.addFile = function(){
      $scope.data.files.push('http://');
    }
  });
