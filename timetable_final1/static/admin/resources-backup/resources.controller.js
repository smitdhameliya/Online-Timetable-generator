(function () {
    'use strict';

    angular.module('appModule')
        .controller('resourcesCtrl', ['$rootScope', '$transitions', '$timeout', '$mdDialog', '$http', '$mdToast',
            function ($rootScope, $transitions, $timeout, $mdDialog, $http, $mdToast) {

                // -------------- init() --------------
                let vm = this,
                    $body = angular.element(document.body);
                vm.disciplines = [];
                vm.showDisciplines = false;
                vm.showSemesters = false;
                vm.numbersOfBatches = 0;

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

                // ------------- end init() ------------

                let server = $rootScope.serverUrl;
                // get request for subjects to all disciplines
                let getData = _ => {
                    $rootScope.ploading = true;
                    $http.get(server + 'subject/')
                        .then(
                            res => {
                                console.log(res.data)
                                vm.disciplines = [];
                                vm.disciplines.push(res.data);
                                $mdDialog.cancel();
                                $rootScope.ploading = false;
                            }, err => {
                                showToast('Failed to load Subjects', 'top right', 'red-toast');
                            });
                };
                getData();

                let subjectTemplate = {
                    name: '',
                    subcode: 0,
                    elective: 0,
                    batches: [],
                    shift: '',
                    course: '',
                    discipline: '',
                    semester: '',
                    no_batch: 0,
                    load: 0,
                    schema: { labs: 0, lectures: 0, tutorials: 0 },
                };

                vm.action = 'insert';
                vm.ed_Subject = subjectTemplate;
                // on subject selected
                vm.select_subject = (subject, ev) => {
                    vm.ed_Subject = angular.copy(subject);
                    vm.action = 'update';
                    vm.showDialog_Subject(ev);
                };
                // on subject insert btn
                vm.showInsertDialog_subject = ev => {
                    vm.ed_Subject = subjectTemplate;
                    vm.action = 'insert';
                    vm.showDialog_Subject(ev);
                };
                // on dialog cancel btn
                vm.dialog_cancel_subject = _ => {
                    $mdDialog.cancel();
                    vm.ed_Subject = subjectTemplate;
                };
                vm.getNumber = no => new Array(no);

                // show dialog
                vm.showDialog_Subject = ev => $mdDialog.show({
                    multiple: true,
                    contentElement: '#editSubject',
                    parent: $body,
                    targetEvent: ev,
                    clickOutsideToClose: true
                });

                // action in dialog for subject
                vm.subject_action = action => {
                    // vm.ed_Subject.discipline = vm.selectedDiscipline;
                    if (!vm.form_edit_subject.$valid) return;

                    vm.ed_Subject.discipline = 'Computer Engineering';
                    vm.ed_Subject.semester = vm.selectedSemester;
                    vm.ed_Subject.course = 'B.E.';
                    if (!vm.isLectures) vm.ed_Subject.schema.lectures = 0;
                    if (!vm.isLabs) vm.ed_Subject.schema.labs = 0;
                    if (!vm.isTutorials) vm.ed_Subject.schema.tutorials = 0;
                    vm.ed_Subject.load = vm.ed_Subject.schema.lectures + vm.ed_Subject.schema.labs + vm.ed_Subject.schema.tutorials;

                    $rootScope.ploading = true;
                    if (action === 'update') {
                        $http.post(server + 'subject/update/', vm.ed_Subject)
                            .then(
                                async res => {
                                    $mdDialog.cancel();
                                    await getData();
                                    showToast('Subject is updated', 'top right', 'green-toast');
                                }, err => {
                                    showToast('Failed to update Subject', 'top right', 'red-toast');
                                });
                    }
                    if (action === 'insert') {
                        $http.post(server + 'subject/', vm.ed_Subject)
                            .then(
                                async res => {
                                    $mdDialog.cancel();
                                    await getData();
                                    showToast('New Subject is inserted', 'top right', 'green-toast');
                                    // insertSub();
                                }, err => {
                                    showToast('Failed to insert Subject', 'top right', 'red-toast');
                                });
                    }
                };

                async function insertSub() {
                    for (let i = 200; i < 300; i++) {
                        vm.ed_Subject.name = 'Subject' + i;
                        vm.ed_Subject.subcode = i;
                        await $http.post(server + 'subject/', vm.ed_Subject)
                        console.log(vm.ed_Subject.name + ' added!');
                    }
                }

                async function deleteSub() {
                    for (let i = 100; i < 200; i++) {
                        await $http.post(server + 'subject/delete/', { 'subcode': i })
                        console.log(vm.ed_Subject.name + ' deleted!');
                    }
                }

                vm.removeSubject = ev => {
                    $mdDialog.show(
                        $mdDialog.confirm()
                            .multiple(true)
                            .parent($('#editSubject')).title('Alert')
                            .targetEvent(ev)
                            .clickOutsideToClose(true)
                            .textContent(`Are you sure, you want to remove ${vm.ed_Subject.name}?`)
                            .ariaLabel('Alert Subject remove')
                            .ok('REMOVE').cancel('CANCEL')
                    ).then(_ => {
                        $rootScope.ploading = true;
                        $http.post(server + 'subject/delete/', { 'subcode': vm.ed_Subject.subcode })
                            .then(
                                async res => {
                                    $mdDialog.cancel();
                                    await getData();
                                    // deleteSub();
                                    showToast('Subject is removed now!', 'top right', 'green-toast');
                                }, err => {
                                    showToast('Failed to remove Subject!', 'top right', 'red-toast');
                                })
                    }, _ => console.log('not removed'));
                };
            }
        ]);

})();