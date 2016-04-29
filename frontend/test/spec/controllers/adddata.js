'use strict';

describe('Controller: AdddataCtrl', function () {

  // load the controller's module
  beforeEach(module('frontendApp'));

  var AdddataCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    AdddataCtrl = $controller('AdddataCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(AdddataCtrl.awesomeThings.length).toBe(3);
  });
});
