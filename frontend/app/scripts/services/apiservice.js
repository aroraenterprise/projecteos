'use strict';

/**
 * @ngdoc service
 * @name frontendApp.apiService
 * @description
 * # apiService
 * Service in the frontendApp.
 */
angular.module('frontendApp')
  .service('apiService', function (Restangular, $timeout, notificationFactory) {
    var me = this;

    this.storms = {};
    this.params = null;
    this.ready = true;

    this.listStorms = function(){
      if (!me.ready)
        return;

      if (!me.storms.list){
        me.storms = {
          list: [],
          meta: {}
        };
      }

      me.ready = false;
      var promise = Restangular.all('storms').getList(me.params);
      promise.then(function(response){
        if (response) {
          angular.forEach(response, function (storm) {
            me.storms.list.push(storm);
          });
          me.storms.meta = response.meta;
          me.params.cursor = response.meta.next_cursor;
        }
      }, function(error){
        console.log(error);
      }).finally(function(){me.ready = true});
      return promise;
    }
  });
