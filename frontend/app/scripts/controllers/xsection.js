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

    $scope.visualization = {
      data: [],
      populations: {},
      comparison: 'state_police_expenditure_level',
      map: {
        year: 2015,
        yearMax: 2016,
        yearMin: 1995
      }
    };

    $scope.statistics = [
      {
        name: 'income_tax',
        title: 'Income Tax'
      },
      {
        name: 'binge_drinking_level',
        title: 'Binge Drinking Level'
      },
      {
        name: 'total_physicians',
        title: 'Total physicians'
      },
      {
        name: 'state_police_expenditure_level',
        title: 'Amount budgeted for Policing'
      }
    ];

    $scope.options = {
      chart: {
        type: 'scatterChart',
        height: 450,
        margin : {
          top: 20,
          right: 20,
          bottom: 40,
          left: 55
        },
        x: function(d){ return d.x; },
        y: function(d){ return d.y; },
        useInteractiveGuideline: true,
        dispatch: {
          stateChange: function(e){ console.log("stateChange"); },
          changeState: function(e){ console.log("changeState"); },
          tooltipShow: function(e){ console.log("tooltipShow"); },
          tooltipHide: function(e){ console.log("tooltipHide"); }
        },
        xAxis: {
          axisLabel: $scope.visualization.comparison
        },
        yAxis: {
          axisLabel: 'Total Damage (standardized unit)',
          tickFormat: function(d){
            return d3.format('.02f')(d);
          },
          axisLabelDistance: -10
        },
        callback: function(chart){
          console.log("!!! lineChart callback !!!");
        }
      }
    };

    $scope.chartData = [];

    function calculateDamage(storm){
      return parseInt(storm.direct_injuries) * 2 + parseInt(storm.indirect_injuries) * 2 +
        parseInt(storm.direct_deaths) * 5 + parseInt(storm.indirect_deaths) * 5 +
        parseFloat(storm.property_damage) * 1.5 + parseFloat(storm.crops_damage) * 2;
    }

    function updateAnalytics(){
      $scope.chartData = [];
      if ($scope.visualization.data && $scope.visualization.populations){
        var data = [];
        angular.forEach($scope.visualization.data, function(event){
          var y = calculateDamage(event);
          var metric = $scope.visualization.populations[event.state_fips];
          if (metric) {
            var x = metric['state_police_expenditure_level'];
            data.push({x: x, y: y});
          }
        });
        $scope.chartData = [
          {
            values: data,
            key: 'Budget on Policing',
            color: '#ff7f0e'
          }
        ]
      }
    }



    /** Mapping Stuff **/
    uiGmapGoogleMapApi.then(function(maps) {
      $scope.map = { center: { latitude: 41.850033, longitude: -87.6500523 }, zoom: 4 };
    });

    $scope.getMarkers = function(){
      return false;
    };

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
        updateAnalytics();
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

    oldApiService.listPopulations().then(function(response){
      angular.forEach(oldApiService.populations.list, function(metric){
        $scope.visualization.populations[metric.state_fips] = metric;
      });
    })
  });
