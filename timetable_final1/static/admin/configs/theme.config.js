(function () {
    'use strict';

    angular.module('appModule')
        .config(['$mdThemingProvider', function ($mdThemingProvider) {
            $mdThemingProvider.theme('default')
                .primaryPalette('deep-orange')
                .accentPalette('deep-purple');
        }]);

})();