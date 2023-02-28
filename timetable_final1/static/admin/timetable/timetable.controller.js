(function () {
    'use strict';

    angular.module('appModule')
        .controller('timetableCtrl', ['$timeout', '$http', '$rootScope', '$mdToast', '$interval',
            function ($timeout, $http, $rootScope, $mdToast, $interval) {

                // -------------- init() --------------
                let vm = this;
                vm.disciplines = vm.semesters = vm.facultylist = vm.subjectlist = [];
                vm.generatingTimetable = vm.regeneratingTimetable = vm.valid_Semester_Select = false;
                vm.search = {
                    subject: '',
                    faculty: ''
                };
                vm.timeNumbers = ["10:30 - 11:30", "11:30 - 12:30", "12:30 - 1:00", "2:00 - 3:00", "3:00 - 4:00", "4:10 - 5:10", "5:10 - 6:10"];
                let serverUrl = $rootScope.serverUrl, semester_data = [];
                let showToast = (text, position, cssClass) => {
                    $rootScope.ploading = false;
                    vm.loading = false;
                    $mdToast.show($mdToast.simple().textContent(text).position(position).hideDelay(3000).toastClass(cssClass));
                };
                vm.showFullTT = true;

                vm.disciplines = ["Computer Engineering", "Civil Engineering", "Electrical Engineering", "Mechanical Engineering", "Electronics and Communications", "Applied Science"];
                vm.selected_discipline = vm.disciplines[0];

                // let time_to_generate = 6; // in seconds
                // let timer_time = time_to_generate * 10;
                // ------------- end init() ------------

                // vm.determinateValue = 0;
                // let timer = $interval(function () {
                //     vm.determinateValue += 1;
                //     if (vm.determinateValue > 100)
                //         // $interval.cancel(timer);
                //         vm.determinateValue = 0;
                // }, timer_time);

                let find_Semesters = discipline => {
                    let data = { type: 'semesters', data: ['odd', 'even'] };
                    return data;
                };

                vm.select_discipline = _ => {
                    let discipline = vm.selected_discipline,
                        data = find_Semesters(discipline);
                    if (data.type === 'semesters') vm.semesters = data.data;
                };

                vm.validateSemesterSelect = _ => vm.valid_Semester_Select = vm.EachSemesters.includes(vm.selected_sem);

                vm.select_semesters = _ => {
                    let semesters = vm.selected_semesters;  //even or odd
                    $rootScope.ploading = vm.loading = true;
                    $http.post(serverUrl + 'timetable_gen/', {
                        'type': 0,
                        'term': semesters,
                        'discipline': vm.selected_discipline,
                        'course': 'B.E.'
                    }).then(
                        res => {
                            console.log(res.data)
                            $rootScope.ploading = vm.loading = false;
                            semester_data = res.data;
                            vm.EachSemesters = semester_data;
                            analyseData(semester_data);
                            vm.change(res.data[0] ? res.data[0] : {});
                        }, err => {
                            vm.loading = false;
                            showToast('Failed to Fetching Timetable!', 'top right', 'red-toast');
                        });
                };
                vm.select_discipline();
                vm.selected_semesters = 'odd';
                vm.select_semesters();

                let analysedData = []
                vm.change = semester => {
                    vm.classroom = semester.classroom;
                    // if (analysedData.includes(semester))
                }

                let analyseData = semesters => {
                    vm.facultylist = [];
                    vm.subjectlist = [];
                    $.each(semesters, function (index, semester) {
                        $.each(semester.days, function (index, day) {
                            $.each(day.slots, function (index, slot) {
                                $.each(slot.values, function (index, value) {
                                    if (!(vm.facultylist.includes(value.faculty))) {
                                        vm.facultylist.push(value.faculty);
                                    }
                                    if (!(vm.subjectlist.includes(value.subject))) {
                                        vm.subjectlist.push(value.subject);
                                    }
                                });
                            });
                        });
                    });
                }

                vm.generate_timetable = _ => {
                    vm.loading = true;
                    $rootScope.ploading = true;
                    $http.post(serverUrl + 'timetable_gen/', {
                        type: 1,
                        term: vm.selected_semesters,
                        discipline: vm.selected_discipline,
                        course: 'B.E.'
                    }).then(
                        res => {
                            $rootScope.ploading = vm.loading = false;
                            semester_data = res.data;
                            vm.EachSemesters = semester_data;
                        }, err => {
                            showToast('Failed to generating Timetable!', 'top right', 'red-toast');
                        }
                    );
                };
            }
        ]);
})();