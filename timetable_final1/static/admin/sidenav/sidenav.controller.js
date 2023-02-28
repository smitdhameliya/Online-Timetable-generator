(function () {
    'use strict';

    angular.module('appModule')
        .controller('sidenavCtrl', ['$mdSidenav', '$window', function ($mdSidenav, $window) {
            // console.log($route);
            let vm = this;
            vm.toggleSideNav = _ => $mdSidenav('left').toggle();
            vm.logout = _ => $window.location.href = "/";
        }]);

})();