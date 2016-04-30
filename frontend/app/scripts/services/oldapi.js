'use strict';

/**
 * @ngdoc service
 * @name frontendApp.oldApi
 * @description
 * # oldApi
 * Service in the frontendApp.
 */
angular.module('frontendApp')
  .service('oldApiService', function ($http, $interval, $log) {
    var baseUrl = 'https://eos-project.appspot.com/api/v1/';
    var me = this;
    this.storms = {
      list: [],
      meta: {},
      params: {}
    };

    this.list = function(){
      var promise = $http({
        url: baseUrl + 'storms',
        params: me.storms.params,
        method: 'get'
      });

      promise.then(function(response){
        if (response.data) {
          angular.forEach(response.data.list, function (item) {
            me.storms.list.push(item);
          });
        }
        me.storms.meta = response.data.meta;
        me.storms.params.cursor = response.data.meta.next_cursor;
      }, function(error){
        console.log(error);
      });
      return promise;
    };
  });
