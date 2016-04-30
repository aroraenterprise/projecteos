'use strict';

/**
 * @ngdoc service
 * @name frontendApp.notification
 * @description
 * # notification
 * Factory in the frontendApp.
 */
angular.module('frontendApp')
  .factory('notificationFactory', function ($mdDialog) {
    var factory = {};
    factory.showDialog = function (title, message, ok) {
      // Appending dialog to document.body to cover sidenav in docs app
      // Modal dialogs should fully cover application
      // to prevent interaction outside of dialog
      $mdDialog.show(
        $mdDialog.alert()
          .clickOutsideToClose(true)
          .title(title)
          .textContent(message)
          .ariaLabel(message)
          .ok(ok || 'Got it!')
      );
    };

    return factory;
  });
