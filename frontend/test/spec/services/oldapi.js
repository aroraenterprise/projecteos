'use strict';

describe('Service: oldApi', function () {

  // load the service's module
  beforeEach(module('frontendApp'));

  // instantiate service
  var oldApi;
  beforeEach(inject(function (_oldApi_) {
    oldApi = _oldApi_;
  }));

  it('should do something', function () {
    expect(!!oldApi).toBe(true);
  });

});
