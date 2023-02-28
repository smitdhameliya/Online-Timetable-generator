(function () {
    'use strict';
    let dashboardView = {
            templateUrl: 'static/admin/dashboard/dashboard.view.html',
            controller: 'dashboardCtrl',
            controllerAs: 'db',
            css: {
                desktop: ['static/admin/dashboard/assets/dashboard_desktop.css'],
                common: ['static/admin/dashboard/assets/dashboard.css'],
            }
        },
        resourcesView = {
            templateUrl: 'static/admin/resources/resources.view.html',
            controller: 'resourcesCtrl',
            controllerAs: 'rs',
            css: {common: ['static/admin/resources/assets/resources.css']}
        },
        subjectsView = {
            templateUrl: 'static/admin/subjects/subjects.view.html',
            controller: 'subjectsCtrl',
            controllerAs: 'sub',
            css: {common: ['static/admin/subjects/assets/subjects.css']}
        },
        // disciplineView = {
        //   templateUrl: 'subjects/disciplines/disciplines.view.html',
        //   controller: 'disciplinesCtrl',
        //   controllerAs: 'dsc',
        //   css: { desktop: ['subjects/disciplines/assets/disciplines.css'] },
        //   resolve: {
        //     disciplines: ['$http', '$transition$', ($http, $transition$) =>
        //       $http.get($transition$.params().course + '/disciplines/').then(res => res.data)
        //     ]
        //   }
        // },
        facultiesView = {
            templateUrl: 'static/admin/faculties/faculties.view.html',
            controller: 'facultiesCtrl',
            controllerAs: 'fc',
            css: {common: ['static/admin/faculties/assets/faculties.css']}
        },
        timetableView = {
            templateUrl: 'static/admin/timetable/timetable.view.html',
            controller: 'timetableCtrl',
            controllerAs: 'tml',
            css: {common: ['static/admin/timetable/assets/timetable.css']}
        },
        toolbarView = {
            templateUrl: 'static/admin/toolbar/toolbar.template.html',
            controller: 'toolbarCtrl',
            controllerAs: 'tbar',
            css: {common: ['static/admin/toolbar/assets/toolbar.css']}
        },
        sidenavView = {
            templateUrl: 'static/admin/sidenav/sidenav.template.html',
            controller: 'sidenavCtrl',
            controllerAs: 'snav',
            css: {common: ['static/admin/sidenav/assets/sidenav.css']}
        };


    angular.module('appModule')
        .config(['$stateProvider', '$urlRouterProvider',
            function ($stateProvider, $urlRouterProvider) {

                $stateProvider
                    .state('Home', {
                        url: '/',
                        views: {
                            'toolbar': toolbarView,
                            'sidenav': sidenavView,
                            'view-left': dashboardView
                        }
                    })
                    .state('Home.resources', {
                        url: 'resources',
                        views: {'view-right': resourcesView}
                    })
                    .state('Home.faculties', {
                        url: 'faculties',
                        views: {'view-right': facultiesView}
                    })
                    .state('Home.timetable', {
                        url: 'timetable',
                        views: {'view-right': timetableView}
                    })
                    .state('Home.subjects', {
                        url: 'subjects',
                        views: {'view-right': subjectsView}
                    });
                // .state('Home.courses.disciplines', {
                //   url: '/{course}',
                //   views: { 'input-views': disciplineView }
                // })

                $urlRouterProvider.otherwise('/');
            }
        ]);

})();