'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:VisualizationsCtrl
 * @description
 * # VisualizationsCtrl
 * Controller of the frontendApp
 */
angular.module('frontendApp')
  .controller('XSectionCtrl', function ($scope, uiGmapGoogleMapApi, apiService, oldApiService) {

    $scope.statistics = [
      {
        name: 'total_physicians',
        title: 'Total physicians'
      },
      {
        name: 'money_spent_on_police',
        title: 'Amount budgeted for Policing'
      }
    ];

    $scope.chartData = [];

    $scope.options = {
      chart: {
        type: 'multiBarChart',
        height: 450,
        margin : {
          top: 20,
          right: 20,
          bottom: 45,
          left: 45
        },
        clipEdge: true,
        //staggerLabels: true,
        duration: 500,
        stacked: true,
        xAxis: {
          axisLabel: 'Time (ms)',
          showMaxMin: false,
          tickFormat: function(d){
            return d3.format(',f')(d);
          }
        },
        yAxis: {
          axisLabel: 'Y Axis',
          axisLabelDistance: -20,
          tickFormat: function(d){
            return d3.format(',.1f')(d);
          }
        }
      }
    };

    $scope.visualization = {
      data: [],
      map: {
        year: 2010,
        yearMax: 2016,
        yearMin: 1995,
        comparison: {
          name: $scope.statistics[0].name
        }
      }
    };

    /** Mapping Stuff **/
    uiGmapGoogleMapApi.then(function(maps) {
      $scope.map = { center: { latitude: 41.850033, longitude: -87.6500523 }, zoom: 4 };
    });

    $scope.getMarkers = function(){
      return false;
    };


    /** End Mapping Stuff **/

    /** Histo Maps **/


    /** Line Maps (timelines) **/
    //
    //$scope.exampleData = [
    //  {
    //    "key": "Series 1",
    //    "values": [[1025409600000, 0], [1028088000000, -6.3382185140371], [1030766400000, -5.9507873460847], [1033358400000, -11.569146943813], [1036040400000, -5.4767332317425], [1038632400000, 0.50794682203014], [1041310800000, -5.5310285460542], [1043989200000, -5.7838296963382], [1046408400000, -7.3249341615649], [1049086800000, -6.7078630712489], [1051675200000, 0.44227126150934], [1054353600000, 7.2481659343222], [1056945600000, 9.2512381306992]]
    //  },
    //  {
    //    "key": "Series 2",
    //    "values": [[1025409600000, 0], [1028088000000, 0], [1030766400000, 0], [1033358400000, 0], [1036040400000, 0], [1038632400000, 0], [1041310800000, 0], [1043989200000, 0], [1046408400000, 0], [1049086800000, 0], [1051675200000, 0], [1054353600000, 0], [1056945600000, 0], [1059624000000, 0], [1062302400000, 0], [1064894400000, 0], [1067576400000, 0], [1070168400000, 0], [1072846800000, 0], [1075525200000, -0.049184266875945]]
    //  },
    //  {
    //    "key": "Series 3",
    //    "values": [[1025409600000, 0], [1028088000000, -6.3382185140371], [1030766400000, -5.9507873460847], [1033358400000, -11.569146943813], [1036040400000, -5.4767332317425], [1038632400000, 0.50794682203014], [1041310800000, -5.5310285460542], [1043989200000, -5.7838296963382], [1046408400000, -7.3249341615649], [1049086800000, -6.7078630712489], [1051675200000, 0.44227126150934], [1054353600000, 7.2481659343222], [1056945600000, 9.2512381306992]]
    //  },
    //  {
    //    "key": "Series 4",
    //    "values": [[1025409600000, -7.0674410638835], [1028088000000, -14.663359292964], [1030766400000, -14.104393060540], [1033358400000, -23.114477037218], [1036040400000, -16.774256687841], [1038632400000, -11.902028464000], [1041310800000, -16.883038668422], [1043989200000, -19.104223676831], [1046408400000, -20.420523282736], [1049086800000, -19.660555051587], [1051675200000, -13.106911231646], [1054353600000, -8.2448460302143], [1056945600000, -7.0313058730976]]
    //  }
    //];
    //
    //var colorArray = ['#FF0000', '#0000FF', '#FFFF00', '#00FFFF'];
    //$scope.colorFunction = function() {
    //  return function(d, i) {
    //    return colorArray[i];
    //  };
    //};

    /** When a year changes **/
    $scope.loadingEvents = false;

    function getEvents(){
      var promise = oldApiService.list();
      promise.then(function(response){
        $scope.visualization.data = oldApiService.storms.list;
        if (oldApiService.storms.meta.more) {
          getEvents(); // recursive call
        } else {
          $scope.loadingEvents = false;
        }
        createMapMarkers();
      }, function(error){
        $scope.loadingEvents = false;
      });
      return promise;
    }

    $scope.onYearChange = function(newYear){
      $scope.visualization.data = angular.copy([]); // reset the data
      $scope.loadingEvents = true;
      oldApiService.storms.params = {
        limit: 300,
        filter: 'year=' + parseInt(newYear)
      };
      getEvents();
    };

    /** Start off by manually calling a year change**/
    $scope.onYearChange($scope.visualization.map.year);

    $scope.onMarkerClicked = function(marker, event, model){
      console.log(marker, event, model);
    };

    /** Make all the markers for the  map **/
    $scope.markers = [];
    function createMapMarkers() {
      $scope.markers = [];
      if ($scope.visualization.data) {
        angular.forEach($scope.visualization.data, function (event) {
          if (event.latitude && event.longitude) {
            var newMarker = {
              id: event.key,
              latitude: parseFloat(event.latitude),
              longitude: parseFloat(event.longitude),
              title: event.name
            };
            $scope.markers.push(newMarker);
          }
        });
      }
    }
  });
