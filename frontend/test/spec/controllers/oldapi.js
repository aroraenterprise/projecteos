'use strict';

describe('Controller: OldapiCtrl', function () {

  // load the controller's module
  beforeEach(module('frontendApp'));

  var OldapiCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    OldapiCtrl = $controller('OldapiCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(OldapiCtrl.awesomeThings.length).toBe(3);
  });
});
