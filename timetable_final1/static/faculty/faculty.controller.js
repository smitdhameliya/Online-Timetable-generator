(function () {
    'use strict';

    angular.module('appModule')
        .controller('facultyCtrl', ['$rootScope', '$mdSidenav', '$http', '$cookies', '$window',
            function ($rootScope, $mdSidenav, $http, $cookies, $window) {

                // -------------- init() --------------
                let vm = this,
                    serverUrl = $rootScope.serverUrl,
                    faculty_id = $cookies.get('faculty_id');


                // ------------- end init() ------------
                vm.loading = true;

                let xterm = 'odd';

                let d = new Date();
                vm.date = d;
                // vm.minDate = new Date(vm.date.getFullYear(), 0, 1);
                // vm.maxDate = new Date(vm.date.getFullYear(), 4, 30);
                vm.day = d.getDay();

                var currentMonth = d.getMonth();
                currentMonth++;
                if (currentMonth >= 7 && currentMonth <= 12) {
                    xterm = 'odd';
                } else {
                    xterm = 'even';
                }
                // console.log(xterm)
                // xterm='odd';
                $http.post(serverUrl + 'single_faculty/', { id: faculty_id })
                    .then(res => {
                        vm.faculty = res.data;

                        vm.loading = true;
                        $http.post(serverUrl + 'faculty_view/', { 'faculty_id': parseInt(faculty_id), 'term': xterm })
                            .then(res => {
                                vm.loading = false;
                                console.log(res.data)
                                let data = analyseData(res.data);
                                // console.log(res.data)
                                vm.facultyData = data;
                                vm.change(vm.facultyData[0]);
                            }, err => console.log('error'))

                    }, err => console.log('Error in fetching Faculty details'));

                vm.profileMenuAction = (menuItem) => {
                    console.log(menuItem);
                    if ('Logout') {
                        $window.location.href = "/";
                    }
                };

                vm.faculty_positions = ['Associate Professor', 'Assistant Professor', 'Lecturer'];
                vm.days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];


                vm.toggleSideNav = () => $mdSidenav('left').toggle();

                let analyseData = dt => {
                    $.each(dt, function (x, day) {
                        for (let i = 0, j = 1; i < dt[x].data.length && j < dt[x].data.length; i++ , j++) {
                            let dj = dt[x].data[j], di = dt[x].data[i];
                            if (di.subject === dj.subject && di.sem === dj.sem && di.room === dj.room && dj.batch === di.batch) {
                                dt[x].data.splice(j, 1);
                                dt[x].data[i].end = dj.end;
                            }
                            di = dt[x].data[i];
                            if (di.extra && di.subject === di.extra.subject && di.sem === di.extra.sem && di.room === di.extra.room) {
                                dt[x].data[i].batch += " " + di.extra.batch;
                                dt[x].data[i].extra = {};
                            }
                        }
                    });
                    return dt;
                };

                vm.change = d => {
                    let lecs = 0, labs = 0, tuts = 0;
                    $.each(d.data, function (index, slot) {
                        slot.type === 'lecture' ? lecs++ : slot.type === 'lab' ? labs++ : slot.type === 'tutorial' ? tuts++
                            : console.log("slot type unknown");
                    });
                    vm.lectures = lecs;
                    vm.labs = labs;
                    vm.tutorials = tuts;
                };
            }
        ]);

})();