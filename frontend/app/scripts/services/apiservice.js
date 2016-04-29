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

    this.setParams = function(type, params) {
      me.params[type] = params;
      me.data[type] = {
        list: [],
        meta: {}
      }
    };

    this.list = function(type){
      if (!me.data[type].list){
        me.setParams(type);
      }

      var promise = Restangular.all(type).getList(me.params[type]);
      promise.then(function(response){
        if (response) {
          angular.forEach(response, function (item) {
            me.data[type].list.push(item);
          });
          me.data[type].meta = response.meta;
          me.params[type].cursor = response.meta.next_cursor;
        }
      }, function(error){
        console.log(error);
      });
      return promise;
    };
  });
