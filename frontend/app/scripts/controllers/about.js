'use strict';

/**
 * @ngdoc function
 * @name frontendApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the frontendApp
 */
angular.module('frontendApp')
  .controller('AboutCtrl', function () {
    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
    var damageIndex = parseInt(storm.direct_injuries) * 2 + parseInt(storm.indirect_injuries) * 2 +
      parseInt(storm.direct_deaths) * 5 + parseInt(storm.indirect_deaths) * 5 +
      parseFloat(storm.property_damage) * 1.5 + parseFloat(storm.crops_damage) * 2;
  });
