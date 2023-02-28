(function () {
    'use strict';

    angular.module('appModule')

        .run(function ($rootScope, $transitions, mainCircle, $timeout) {

            $rootScope.circle_Items = [
                {
                    name: 'Account_Info',
                    style: {
                        'background-color': '#f7cd4e',
                        'background-image': 'url(static/admin/assets/svg/user.svg)'
                    },
                    shrinkCircle: true
                },
                {
                    name: 'Resources',
                    style: {
                        'background-color': '#8BC34A',
                        'background-image': 'url(static/admin/assets/svg/live_class.svg)'
                    },
                    shrinkCircle: true
                },
                {
                    name: 'Timetable',
                    style: {
                        'background-color': '#FF5252',
                        'background-image': 'url(static/admin/assets/svg/calendar.svg)',
                        'background-position-x': '49%'
                    },
                    shrinkCircle: true
                },
                {
                    name: 'Faculties',
                    style: {
                        'background-color': '#673AB7',
                        'background-image': 'url(static/admin/assets/svg/faculties.svg)'
                    },
                    shrinkCircle: true
                },
                {
                    name: 'Subjects',
                    style: {
                        'background-color': '#2196F3',
                        'background-image': 'url(static/admin/assets/svg/subjects.svg)'
                    },
                    shrinkCircle: true
                }];

            $rootScope.leftCircle = false;
            let radius = '12em',
                ele = '#mainCircle>button',
                outerCircle = '#outer-circle',
                circle_Container = '#mainCircle-container',
                makeFullCircle = _ => mainCircle.toFull(radius, ele),
                makeQuarterCircle = i => mainCircle.toQuarter(radius, ele, i);

            $rootScope.getItem = (item, i) => {
                $timeout(() => {
                    if (item.shrinkCircle) {
                        makeQuarterCircle(i);
                        $rootScope.leftCircle = true;
                        let e = $(ele);
                        e.addClass('shrink');
                        $(e[i]).removeClass('shrink');
                        $(outerCircle).addClass('btnback');
                        $(circle_Container).addClass('shrinkCricle');
                    }
                }, 0);
            };

            $transitions.onFinish({}, function ($transition) {
                let toState = $transition.to();
                $rootScope.ploading = false;

                if (toState.name === 'Home') {
                    makeFullCircle();
                    $(outerCircle).removeClass('btnback');
                    $(circle_Container).removeClass('shrinkCricle');
                    $(ele).removeClass('shrink');
                }
                else {
                    let toState = $transition.to().name.split('.');
                    if (toState.length > 1 && toState[0] === 'Home') {
                        toState = toState[1];
                        let i = -1,
                            item = undefined;
                        $rootScope.circle_Items.forEach((e, index) => {
                            if (e.name.toLowerCase() === toState) {
                                i = index;
                                item = e;
                            }
                        });
                        if (item !== undefined)
                            $rootScope.getItem(item, i);
                    }
                }
            });
        })
})();