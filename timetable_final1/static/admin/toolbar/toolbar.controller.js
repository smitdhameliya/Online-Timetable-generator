(function () {
    'use strict';

    angular.module('appModule')
        .controller('toolbarCtrl', ['$mdSidenav', '$window', function ($mdSidenav, $window) {
            let vm = this;
            vm.user = 'User';
            vm.toggleSideNav = _ => $mdSidenav('left').toggle();

            vm.profileMenuAction = (menuItem) => {
                if (menuItem==='Logout') $window.location.href = "/";
            }

        }]);

})();