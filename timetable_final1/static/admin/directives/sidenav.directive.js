(function () {
  'use strict';

  angular.module('appModule')
    .directive('sideNav', [function () {
      return {
        restrict: 'E',
        templateUrl: 'admin/sidenav/sidenav.template.html',
        replace: true,
        controller: 'sidenavCtrl'
      }
    }]);

})();