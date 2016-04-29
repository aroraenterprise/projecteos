'use strict';

/**
 * @ngdoc overview
 * @name frontendApp
 * @description
 * # frontendApp
 *
 * Main module of the application.
 */
angular
  .module('frontendApp', [
    'ngAnimate',
    'ngCookies',
    'ngMessages',
    'ngResource',
    'ngSanitize',
    'ngTouch',
    'ui.router',
    'restangular',
    'uiGmapgoogle-maps',
    'ngMaterial',
    'nvd3'
  ])
  .config(function ($locationProvider, uiGmapGoogleMapApiProvider, $stateProvider, $urlRouterProvider, RestangularProvider) {
    uiGmapGoogleMapApiProvider.configure({
      //    key: 'your api key',
      v: '3.20', //defaults to latest 3.X anyhow
      libraries: 'weather,geometry,visualization'
    });

    $urlRouterProvider.otherwise('/');

    $stateProvider.state('home', {
      url: '/',
      templateUrl: 'views/main.html',
      controller: 'HomeCtrl'
    }).state('data', {
      url: '/data',
      templateUrl: 'views/data.html',
      controller: 'DataCtrl'
    }).state('xsection', {
      url: '/xsection',
      templateUrl: 'views/xsection.html',
      controller: 'XSectionCtrl'
    }).state('timeline', {
      url: '/timeline',
      templateUrl: 'views/timeline.html',
      controller: 'TimelineCtrl'
    }).state('add-data', {
      url: '/add-data',
      templateUrl: 'views/add-data.html',
      controller: 'AddDataCtrl'
    });

    /**
     * Default id for restangular objects is their key
     */
    RestangularProvider
      .setBaseUrl('https://eos-project.appspot.com/api/v1/')
      .setRestangularFields({
        id : 'key'
      });
  })
  .run(function(Restangular, $rootScope, $timeout){

    var loadingPromise;
    var endLoading = function () {
      $timeout.cancel(loadingPromise);
      $rootScope.isLoading = false;
    };

    //Restangular.setErrorInterceptor(function (res) {
    //  endLoading();
    //  var msg;
    //  if (res.data)
    //    msg = res.data.description ? res.data.description : null;
    //  if (res.status === 403) {
    //    showError('danger', msg || 'Sorry, you\'re not allowed to do it, please sign in with different account');
    //  } else if (res.status === 401) {
    //    BrowserHistory.forceShowSignup();
    //    showError('info', msg || 'Please login or sign up to continue.');
    //  } else if (res.status === 404) {
    //    showError('danger', msg || 'Sorry, this requested page doesn\'t exist');
    //  } else {
    //    showError('danger', msg, true);
    //  }
    //  return true;
    //});

    Restangular.addRequestInterceptor(function (element, operation) {
      // This is just convenient loading indicator, so we don't have to do it in every controller
      // separately. It's mainly used to disable submit buttons, when request is sent. There's also
      // added little delay so disabling buttons looks more smoothly
      loadingPromise = $timeout(function () {
        $rootScope.isLoading = true;
      }, 500);

      if (operation === 'remove') {
        return undefined;
      }
      return element;
    });
    Restangular.addResponseInterceptor(function (data) {
      endLoading();
      return data;
    });

    /**
     * This interceptor extracts meta data from list response
     * This meta data can be:
     *      cursor - ndb Cursor used for pagination
     *      totalCount - total count of items
     *      more - whether datastore contains more items, in terms of pagination
     */
    Restangular.addResponseInterceptor(function (data, operation) {
      var extractedData;
      if (operation === 'getList') {
        extractedData = data.list;
        extractedData.meta = data.meta;
      } else {
        extractedData = data;
      }
      return extractedData;
    });
  });
