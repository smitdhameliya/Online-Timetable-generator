(function () {
    'use strict';

    angular.module('appModule')
        .factory('$localStorage', ['$window', function ($window) {
            return {
                set: (key, value) => $window.localStorage[key] = value,
                get: (key, defaultValue) => $window.localStorage[key] || defaultValue,
                setObject: (key, value) => $window.localStorage[key] = JSON.stringify(value),
                getObject: key => JSON.parse($window.localStorage[key] || '{}'),
                remove: key => delete $window.localStorage[key]
            }
        }]);

})();