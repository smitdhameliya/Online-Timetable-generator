(function () {
  'use strict';

  angular.module('appModule')
    .directive('toolbar', [function () {
      return {
        restrict: 'E',
        templateUrl: 'admin/toolbar/toolbar.template.html',
        replace: true,
        controller: 'toolbarCtrl',
        controllerAs: 'tbar'
      }
    }]);

})();