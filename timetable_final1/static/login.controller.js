angular.module('Authentication')
  .controller("loginCtrl", ['$scope', '$location', 'AuthenticationService',
    function ($scope, $location, AuthenticationService) {

      $scope.login = function () {

        AuthenticationService.ClearCredentials();// reset login status
        $scope.dataLoading = true;

        if ($scope.login_username && $scope.login_password) {
          AuthenticationService.Login($scope.login_username, $scope.login_password,
            function (response) {
              console.log(response.data.status);
              if (response.data.status === 'authorized') {
                AuthenticationService.SetCredentials($scope.login_username, $scope.login_password);
                $location.path('/dashboard');
              } else if (response.data.status === 'unauthorized') {
                $scope.error = 'user name or password is wrong';
                $scope.dataLoading = false;
              } else
                console.log('bad response from server');
            });
        } else
          $scope.error = 'Please fill all given fields !!';
        $scope.dataLoading = false;
      };

      $scope.reg = function () {
        if ($scope.register_username && $scope.register_password) {
          let details = {
            username: $scope.register_username,
            password: $scope.register_password
          };

          AuthenticationService.Register(details,
            function (response) {
              if (response.data.status === 'registered')
                alert('you are registered');
              else if (response.data.status === 'unregistered')
                alert('this username already exists');
              else
                console.log('bad response from server');
            });
        } else
          $scope.error = 'Please fill all needed details in given fields !!';
      };
    }
  ]);