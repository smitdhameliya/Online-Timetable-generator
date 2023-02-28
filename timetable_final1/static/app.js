angular
    .module('AppModule', [
        'ngCookies', 'Authentication', 'ngMaterial',
    ])
    .config(['$httpProvider', '$locationProvider',
        function ($httpProvider, $locationProvider) {
            $httpProvider.defaults.headers.common = {};
            $httpProvider.defaults.headers.post = {};
            $httpProvider.defaults.headers.put = {};
            $httpProvider.defaults.headers.patch = {};

            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        }
    ])
    .run(function ($rootScope) {
        // $rootScope.serverUrl = 'http://127.0.0.1:8000/';
        // $rootScope.serverUrl = 'http://192.168.31.92:8000/';
        // $rootScope.serverUrl = 'http://192.168.43.136:8000/';
        $rootScope.serverUrl = '';
    })
    //.run(['$rootScope', '$location', '$cookieStore', '$http',
    //  function ($rootScope, $location, $cookies, $http) {

    // keep user logged in after page refresh
    //  $rootScope.globals = $cookies.get('globals') || {};
    //      if ($rootScope.globals.currentUser) {
    //     $http.defaults.headers.common['Authorization'] =
    //     'Basic ' + $rootScope.globals.currentUser.authdata;
    //      }
    //  }
    //  ])
    .controller("loginCtrl", ['$scope', '$location', 'AuthenticationService', '$window', '$http', '$rootScope', '$mdToast',
        function ($scope, $location, AuthenticationService, $window, $http, $rootScope, $mdToast) {

            let serverUrl = $rootScope.serverUrl;

            let showToast = (text, position, cssClass) => {
                $rootScope.ploading = false;
                $mdToast.show(
                    $mdToast.simple()
                        .textContent(text)
                        .position(position)
                        .hideDelay(3000)
                        .toastClass(cssClass)
                );
            };

            $scope.login = function () {

                // AuthenticationService.ClearCredentials();// reset login status
                $rootScope.ploading = true;

                if ($scope.login_username && $scope.login_password) {
                    // AuthenticationService.Login($scope.login_username, $scope.login_password,
                    $http.post(serverUrl + 'login/', {username: $scope.login_username, password: $scope.login_password})
                        .then(function (response) {
                            console.log(response);
                            $rootScope.ploading = false;
                            if (response.data.status === 'authorized') {
                                if (response.data.is_superuser === 1) {
                                    // go to admin
                                    $window.location.href = 'static/admin/index.html';
                                }
                                else {
                                    // AuthenticationService.SetCredentials($scope.login_username, $scope.login_password);
                                    console.log(response.data.id);
                                    AuthenticationService.SetData(response.data.id);
                                    $window.location.href = 'static/faculty/index.html';
                                }
                            } else if (response.data.status === 'unauthorized') {
                                showToast('unauthorized attempts to login!', 'top right', 'red-toast');
                                $scope.error = 'user name or password is wrong';
                            } else {
                                showToast('Bad response from server!', 'top right', 'red-toast');
                                console.log('bad response from server');
                            }
                        }, function (err) {
                            showToast('No response from server!', 'top right', 'red-toast');
                            console.log('error: ', err);
                        });
                } else {
                    showToast('Please fill all given fields!', 'top right', 'red-toast');
                    $scope.error = 'Please fill all given fields !!';
                }
            };

            $scope.reg = function () {
                $rootScope.ploading = true;
                if ($scope.register_username && $scope.register_password) {
                    let details = {
                        username: $scope.register_username,
                        password: $scope.register_password
                    };

                    AuthenticationService.Register(details,
                        function (response) {
                            if (response.data.status === 'registered')
                                showToast('You are registered!', 'top right', 'green-toast');
                            else if (response.data.status === 'unregistered')
                                showToast('this user already exists!', 'top right', 'red-toast');
                            else
                                showToast('Bad response from server!', 'top right', 'red-toast');
                        });
                } else {
                    showToast('Please fill all needed details in given fields!', 'top right', 'red-toast');
                    $scope.error = 'Please fill all needed details in given fields !!';
                }
            };
        }
    ]);