(function () {
    'use strict';

    let allStates = {};
    let neededCSS = {};

    angular.module('appModule')
        .directive('head', ['$compile', '$transitions', '$timeout', '$state',
            function ($compile, $transitions, $timeout, $state) {

                let getCSS = (scope, elem) => {
                    let html = '<link rel="stylesheet" ng-repeat="(routeCtrl, cssUrl) in routeStyles" ng-href="{{cssUrl}}" />';
                    elem.append($compile(html)(scope));
                    scope.routeStyles = {};

                    let device = 'desktop',
                        smallScreen = (screen && screen.width <= 600),
                        getDeviceCSS = css => smallScreen ? css['mobile'] ? 'mobile' : '' : 'desktop';
                    allStates = $state.router.stateRegistry.states;


                    // $transitions.onSuccess({}, function ($transition) {
                    //   // remove old styles
                    //   let fromViews = $transition.from().views;

                    //   // remove all stylesheets unnecessary
                    //   $timeout(_ => {
                    //   if (fromViews) {
                    //     $.each(fromViews, (key, value) => {           // for each views
                    //       if (value.css) {
                    //         device = getDeviceCSS(value.css);
                    //         if (value.css[device])
                    //           angular.forEach(value.css[device], c => {     // for each stylesheets
                    //             if (!neededCSS.hasOwnProperty(c))
                    //               delete scope.routeStyles[c];
                    //           });
                    //         angular.forEach(value.css['common'], c => {     // for each stylesheets
                    //           if (!neededCSS.hasOwnProperty(c))
                    //             delete scope.routeStyles[c];
                    //         });
                    //       }
                    //     });
                    //   }
                    //   }, 1000);

                    // });

                    let loadCSS = views => {
                        if (views) $.each(views, (key, value) => {           // for each views
                            if (value.css) {
                                device = getDeviceCSS(value.css);

                                angular.forEach(value.css['common'], c => {     // for each stylesheets
                                    neededCSS[c] = c;
                                    scope.routeStyles[c] = c;
                                });
                                if (value.css[device])
                                    angular.forEach(value.css[device], c => {     // for each stylesheets
                                        neededCSS[c] = c;
                                        scope.routeStyles[c] = c;
                                    });
                            }
                        });
                    };

                    $transitions.onBefore({}, function ($transition) {
                        // load new styles
                        let fromState = $transition.from().name;
                        let toState = $transition.to().name;
                        if (fromState !== '' && toState.includes(fromState)) {
                            // mean toState is child state of fromState
                            let views = $transition.to().views;
                            loadCSS(views);
                        }
                        else {
                            neededCSS = {};
                            let nestedStates = toState.split('.');
                            let stateString = '';
                            nestedStates.forEach(state => {
                                stateString += state;
                                let views = allStates[stateString].views;
                                loadCSS(views);
                                stateString += '.';
                            });
                        }

                    });
                };
                return { restrict: 'E', link: getCSS };
            }
        ]);
})();