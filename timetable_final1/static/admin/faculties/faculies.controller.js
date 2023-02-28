(function () {
    'use strict';

    angular.module('appModule')
        .controller('facultiesCtrl', ['$rootScope', '$mdDialog', '$http', '$mdToast',
            function ($rootScope, $mdDialog, $http, $mdToast) {

                // --------------- init() --------------------
                let vm = this,
                    $body = angular.element(document.body);

                vm.selectedItem = null;
                vm.searchText = null;
                vm.allSubjects = [];

                vm.status = 'Fetching faculty data ...';
                let serverUrl = $rootScope.serverUrl;
                const template_faculty = {
                    id: -1,
                    discipline: {
                        id: 1,
                        name: 'computer'
                    },
                    email: '',
                    experience: { academic: 0, industrial: 0 },
                    name: '',
                    position: -1,
                    qualification: [],
                    shift: 'Morning',
                    subjects: [],
                    title: '',
                    workload: 0,
                    profileImg: ''
                };
                vm.ed_faculty = template_faculty;

                let serverURL = serverUrl + 'faculty/';
                $rootScope.ploading = false;

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


                $rootScope.ploading = true;
                $http.post(serverUrl + "getAllSubjects/", { discipline: "Computer Engineering" })
                    .then(
                        res => {
                            vm.allSubjects = res.data;
                            console.log(res);
                            vm.allSubjects.map(function (sub) {
                                sub._lower_sub_name = sub.sub_name.toLowerCase();
                                return sub;
                            });
                            $mdDialog.hide();
                            $rootScope.ploading = false;
                        }, err => {
                            showToast('Failed to load subjects list', 'top right', 'red-toast');
                            console.log("Error in fetching all subjects",err);
                        }
                    );

                let getData = () => {
                    $rootScope.ploading = true;
                    $http.get(serverURL)
                        .then(res => {
                            $rootScope.ploading = false;
                            vm.faculties = res.data.data;
                            console.log(vm.faculties);
                            $mdDialog.hide();
                        }, err => {
                            showToast('Failed to load Faculties', 'top right', 'red-toast');
                            console.log('Something Wrong for fetching data',err);
                        });
                };
                getData();

                vm.faculty_titles = ['Dr.', 'Prof.', 'Mr.', 'Ms.', 'Mrs.', 'Miss'];
                vm.faculty_positions = ['Associate Professor', 'Assistant Professor', 'Lecturer'];
                vm.action = 'insert';
                // -------------- end of init() ---------------

                vm.toggleSearch = () => {
                    vm.isSearching = !vm.isSearching;
                    vm.search = {};
                    $('.overlay').toggleClass('full');
                };
                vm.showMoreOpt = false;

                vm.showMoreOptions = () => {
                    vm.showMoreOpt = !vm.showMoreOpt;
                    vm.search.position = '';
                    vm.search.experience = '';
                };

                vm.getFaculty = (faculty, ev) => {
                    vm.ed_faculty = angular.copy(faculty);
                    vm.action = 'update';
                    vm.showDialog(ev);
                };
                vm.showInsertDialog = ev => {
                    vm.ed_faculty = template_faculty;
                    vm.action = 'insert';
                    vm.showDialog(ev);
                };
                vm.showDialog = ev => $mdDialog.show({
                    multiple: true,
                    contentElement: '#editFaculty',
                    parent: $body,
                    targetEvent: ev,
                    clickOutsideToClose: true
                });
                vm.dialog_cancel = () => {
                    $mdDialog.cancel();
                    vm.form_edit_faculty.$setPristine();
                    vm.ed_faculty = template_faculty;
                };
                vm.faculty_action = action => {
                    $rootScope.ploading = true;
                    if (action === 'update') {
                        $http.post(serverURL + 'update/', { 'faculty': vm.ed_faculty })
                            .then(
                                async res => {
                                    await getData();
                                    $mdDialog.hide();
                                    showToast('Faculty is updated!', 'top right', 'green-toast');
                                }, err => {
                                    showToast('Failed to update Faculty', 'top right', 'red-toast');
                                    console.log('Error while updating new faculty',err);
                                }
                            )
                    }
                    if (action === 'insert') {
                        $http.post(serverURL, { 'faculty': vm.ed_faculty })
                            .then(
                                async res => {
                                    await getData();
                                    $mdDialog.hide();
                                    showToast('New Faculty inserted!', 'top right', 'green-toast');
                                    // insertFac();
                                }, err => {
                                    showToast('Failed to insert Faculty', 'top right', 'red-toast');
                                    console.log('Error while inserting new faculty',err);
                                }
                            )
                    }
                };

                // async function insertFac() {
                //     let m = 0;
                //     for (let i = 0; i < 99; i++) {
                //         vm.ed_faculty.name = 'facultyx' + i;
                //         vm.ed_faculty.email = 'facultyx' + i + '@gmail.com';
                //         vm.ed_faculty.subjects = [
                //             { sub_code: m, sub_name: 'Subject' + m },
                //             { sub_code: (m+1), sub_name: 'Subject' + (m+1) },
                //             { sub_code: (m+2), sub_name: 'Subject' + (m+2) },
                //             { sub_code: (m+3), sub_name: 'Subject' + (m+3) },
                //         ];
                //         m+=3;
                //         await $http.post(serverURL, { 'faculty': vm.ed_faculty });
                //         console.log(vm.ed_faculty.name + ' added!');
                //     }
                //     await getData();
                // }

                vm.removeFaculty = ev => {
                    $mdDialog.show(
                        $mdDialog.confirm()
                            .multiple(true)
                            .parent($('#editFaculty'))
                            .clickOutsideToClose(true)
                            .title('Alert')
                            .textContent(`Are you sure, you want to remove ${vm.ed_faculty.name}?`)
                            .ariaLabel('Alert faculty remove')
                            .ok('REMOVE')
                            .cancel('CANCEL')
                            .targetEvent(ev)
                    ).then(() => {
                        $rootScope.ploading = true;
                        $http.post(serverURL + 'delete/', { 'id': vm.ed_faculty.id })
                            .then(
                                async res => {
                                    await getData();
                                    $mdDialog.hide();
                                    showToast('Faculty is removed now!', 'top right', 'green-toast');
                                }, err => {
                                    showToast('Failed to remove Faculty!', 'top right', 'red-toast');
                                    console.log('error while deleting',err);
                                }
                            )
                    }, () => console.log('not removed'));
                };

                vm.querySearch = query => query ? vm.allSubjects.filter(createFilterFor(query)) : [];

                /**
                 * Create filter function for a query string
                 */
                function createFilterFor(query) {
                    let lowercaseQuery = angular.lowercase(query);
                    return (sub) => sub._lower_sub_name.indexOf(lowercaseQuery) === 0 || sub.sub_code.toString().indexOf(lowercaseQuery) === 0;
                }

                vm.transformChip = (chip) => {
                    // If it is an object, it's already a known chip
                    if (angular.isObject(chip)) return chip;
                    // Otherwise, create a new one
                    return { name: chip, type: 'new' };
                };

                // upload image. to server
                //   vm.uploadFileToUrl = function(file, title, text, uploadUrl){
                //     var payload = new FormData();

                //     payload.append("title", title);
                //     payload.append('text', text);
                //     payload.append('file', file);

                //     return $http({
                //         url: uploadUrl,
                //         method: 'POST',
                //         data: payload,
                //         //assign content-type as undefined, the browser
                //         //will assign the correct boundary for us
                //         headers: { 'Content-Type': undefined},
                //         //prevents serializing payload.  don't do it.
                //         transformRequest: angular.identity
                //     });
                // }

            }
        ]);

})();  