(function () {
    'use strict';

    angular.module('appModule')
        .controller('resourcesCtrl', ['$rootScope', '$compile', '$timeout', 'mainCircle',
            function ($rootScope, $compile, $timeout, mainCircle) {

                // -------------- init() --------------
                var vm = this;

                let data = {
                    type: 'disciplines',
                    data: [
                        {name: 'Computer Eng.', lectures: ['101', '102'], labs: ['201', '202']},
                        {name: 'Civil Eng.', lectures: ['111', '112'], labs: ['211', '212']},
                        {name: 'Electronics & Communications Eng.', lectures: ['131', '132'], labs: ['231', '232']},
                        {name: 'Electrical Eng.', lectures: ['101', '102'], labs: ['201', '202']},
                        {name: 'Mechanical Eng.', lectures: ['101', '102'], labs: ['201', '202']}
                    ]
                };
                if (data.type === 'disciplines') {
                    vm.disciplines = data.data;
                }

                vm.changeLectures = discipline => {
                    let lectures = [];
                    if (vm.discipline.lecturesNo > 0) {
                        for (let i = 0; i < vm.discipline.lecturesNo; i++)
                            lectures.push(vm.discipline.startSeriesLectures + i);
                        vm.discipline.lectures = lectures;
                    }
                    console.log('d')
                }
                // ------------- end init() ------------

            }
        ]);

})();