'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:AdddataCtrl
 * @description
 * # AdddataCtrl
 * Controller of the frontendApp
 */
angular.module('frontendApp')
  .controller('AddDataCtrl', function ($scope, $state, $timeout, apiService, Restangular, notificationFactory) {
    $scope.show = {
      start: true,
      new: false,
      existing: false,
      final: false
    };

    $scope.data = {
      email: 'saj.arora@nyu.edu',
      name: 'Storm',
      description: 'Storm data from NOAA for United States since 1995.',
      files: ['https://www.dropbox.com/s/8gg4bubpaf16whj/StormEvents_details-ftp_v1.0_d2016_c20160419.csv?dl=1']
    };

    $scope.addFile = function(){
      $scope.data.files.push('http://');
    };

    $scope.dataset = {};
    $scope.datasetLoading = false;

    var checkDatasetLoaded = function(status){
      if (!$scope.dataset.key)
        return;
      $scope.dataset.get().then(function(response){
        $scope.dataset.status = response.status;
        if (response.status && response.status.code == status) {
          $scope.dataset.headers = response.headers;
          $scope.datasetLoading = false;
        } else
          $timeout(function(){
            checkDatasetLoaded(status);
          }, 2000);
      }, console.log);
    };

    $scope.headerTypes = [
      'string',
      'text',
      'integer',
      'datetime',
      //'date',
      //'json',
      //'computed'
    ];

    $scope.processData = function(){
      apiService.addDataset($scope.data).then(function(response){
        $scope.show.final = true;
        $scope.datasetLoading = true;
        $scope.secret = response.secret;
        console.log($scope.secret);
        $scope.dataset = response;
        checkDatasetLoaded('headers_loaded'); // check if headers are set
      }, function(error){
        notificationFactory.showDialog('Error', error.data.message);
      })
    };

    $scope.updateDataset = function(){
      $scope.dataset.save().then(function(response){
        $state.go('data', {key: $scope.dataset.key, autoReload:true});
        notificationFactory.showDialog('Parser Started', 'We are now parsing all the files for this dataset. ' +
          'We have redirected you to the data explorer to see all the records now.');
      });
    }
  });
