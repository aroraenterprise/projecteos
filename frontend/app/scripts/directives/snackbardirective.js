'use strict';

/**
 * @ngdoc directive
 * @name frontendApp.directive:snackbarDirective
 * @description
 * # snackbarDirective
 */
angular.module('frontendApp')
  .directive('snackbarDirective', function () {
    return {
      template: '<div aria-live="assertive" aria-atomic="true" aria-relevant="text" class="mdl-snackbar mdl-js-snackbar">' +
      '<div class="mdl-snackbar__text"></div>' +
      '<button type="button" class="mdl-snackbar__action"></button>' +
      '</div>',
      restrict: 'E',
      link: function postLink(scope, element, attrs) {
        element.text('this is the snackbarDirective directive');
      }
    };
  });
