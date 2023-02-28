(function () {
  'use strict';
  let commonScript = [
    'admin/configs/theme.config',
    'admin/directives/sidenav.directive',
    'admin/directives/toolbar.directive',
    'admin/factories/localStorage.factory',
    'admin/toolbar/toolbar.controller',
    'admin/sidenav/sidenav.controller'
  ];


  var app = angular.module('appModule')

    .config(['$routeProvider', '$controllerProvider',
      function ($routeProvider, $controllerProvider) {

        app.registerCtrl = $controllerProvider.register;

        function loadScript(path) {
          var result = $.Deferred(),
            script = document.createElement("script");
          // script.async = "async";
          script.type = "text/javascript";
          script.src = path;
          script.onload = script.onreadystatechange = function (_, isAbort) {
            if (!script.readyState || /loaded|complete/.test(script.readyState)) {
              if (isAbort) result.reject();
              else result.resolve();
            }
          };
          script.onerror = function () {
            result.reject();
          };
          document.querySelector("head").appendChild(script);
          return result.promise();
        }

        function scriptLoader(scripts) {

          return {
            load: function ($q) {
              var deferred = $q.defer(),
                map = scripts.map(name => loadScript(name + ".js"));

              $q.all(map).then(function (r) {
                deferred.resolve();
              });
              return deferred.promise;
            }
          };
        }

        $routeProvider
          .when('/', {
            templateUrl: 'dashboard/dashboard.view.html',
            controller: 'dashboardCtrl',
            css: [...commonCSS, 'dashboard/assets/dashboard.css'],
            resolve: scriptLoader([...commonScript,
              'factories/mainCircle.factory', 'dashboard/dashboard.controller'
            ])
          })
          .otherwise({
            redirectTo: '/'
          });
      }
    ]);

})();