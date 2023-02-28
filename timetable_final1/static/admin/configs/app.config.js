(function () {
    'use strict';

    angular.module('appModule')
        .config(['$httpProvider', '$locationProvider',
            function ($httpProvider, $locationProvider) {
                $httpProvider.defaults.xsrfCookieName = 'csrftoken';
                $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

                // $locationProvider.html5Mode(true);
                // $locationProvider.hashPrefix('!');
            }
        ]);

})();