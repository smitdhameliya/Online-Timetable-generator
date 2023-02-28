(function () {
  'use strict';

  angular.module('appModule', [
    'ngMaterial',
    'ngAnimate',
    'ngCookies'
  ])
  .run(function($rootScope){
    // $rootScope.serverUrl = 'http://192.168.137.135:8000/';
    // $rootScope.serverUrl = 'http://192.168.31.92:8000/';
    // $rootScope.serverUrl = 'http://192.168.43.136:8000/';
    $rootScope.serverUrl = '';
  })
  
  .config(function ($httpProvider) {
    $httpProvider.defaults.headers.common = {};
    $httpProvider.defaults.headers.post = {};
    $httpProvider.defaults.headers.put = {};
    $httpProvider.defaults.headers.patch = {};
  })
  // .run(['$rootScope', '$location', '$cookieStore', '$http',
    //   function ($rootScope, $location, $cookies, $http) {
    //     $rootScope.serverUrl = 'http://192.168.137.135:8000/';
    //     // keep user logged in after page refresh
    //     $rootScope.globals = $cookies.get('globals') || {};
    //     if ($rootScope.globals.currentUser) {
    //       $http.defaults.headers.common['Authorization'] =
    //         'Basic ' + $rootScope.globals.currentUser.authdata;
    //     }
    //   }
    // ])

    .config(['$httpProvider', '$locationProvider',
      function ($httpProvider, $locationProvider) {
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
      }
    ])
    .config(['$mdThemingProvider', function ($mdThemingProvider) {
      $mdThemingProvider.theme('default')
        .primaryPalette('deep-orange')
        .accentPalette('deep-purple');
    }])

    .config(function ($mdDateLocaleProvider) {
      $mdDateLocaleProvider.formatDate = function (date) {
        return date ? moment(date).format('DD/MM/YYYY') : '';
      };

      $mdDateLocaleProvider.parseDate = function (dateString) {
        let m = moment(dateString, 'DD/MM/YYYY', true);
        return m.isValid() ? m.toDate() : new Date(NaN);
      };
    });

})();