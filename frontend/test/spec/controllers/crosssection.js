'use strict';

describe('Controller: CrosssectionCtrl', function () {

  // load the controller's module
  beforeEach(module('frontendApp'));

  var CrosssectionCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    CrosssectionCtrl = $controller('CrosssectionCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(CrosssectionCtrl.awesomeThings.length).toBe(3);
  });
});
