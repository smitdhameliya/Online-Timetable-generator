(function () {
  'use strict';

  angular.module('appModule')
    .controller('hodCtrl', ['$rootScope', '$mdSidenav',
      function ($rootScope, $mdSidenav) {

        // -------------- init() --------------
        var vm = this;

        // ------------- end init() -----------
        vm.hod = {
          id: 1,
          discipline: {
            id: 1,
            name: 'computer'
          },
          email: 'abv@gmail.com',
          experience: { academic: 1, industrial: 5 },
          name: 'Nilam Surti',
          position: 1,
          qualification: ['PhD', 'ME'],
          shift: 'Morning',
          subjects: [
            { id: 1, name: 'CO' },
            { id: 2, name: 'COA' },
          ],
          title: 'Prof.',
          workload: 10,
          profileImg: 'assets/images/Neelam_A_Surti.jpg'
        };

        vm.faculty_positions = ['Associate Professor', 'Assistant Professor', 'Lecturer'];

        vm.days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

        let d = new Date();
        vm.date = d;

        // vm.minDate = new Date(vm.date.getFullYear(), 0, 1);
        // vm.maxDate = new Date(vm.date.getFullYear(), 4, 30);
        vm.day = d.getDay();
        vm.toggleSideNav = () => {
          $mdSidenav('left').toggle();
        };


        vm.timeNumbers = ['10:30-11:30', '11:30-12:30', '12:30-1:30', '2:00-3:00', '3:00-4:00', '4:00-5:00', '5:00-6:00'];

        vm.faculty = {
          me: {
            profileImg: 'assets/images/Neelam_A_Surti.jpg',
            name: 'Nilam Surati'
          }, child: [
            { name: 'Yogesh M. Kapuriya', profileImg: 'assets/images/Yogesh_M_Kapuriya.jpg' },
            { name: 'Vishruti A. Desai', profileImg: 'assets/images/Vishruti_A_Desai.jpg' },
            { name: 'Ami T. Choksi', profileImg: 'test/images/Ami_T_Choksi.jpg' },
          ], lecturer: [
            { name: 'Chetan K. Solanki', profileImg: 'assets/images/Chetan_K_Solanki.jpg' },
            { name: 'Bhumika H. Patel', profileImg: 'assets/images/Bhumika_H_Patel.jpg' },
            { name: 'Saurabh S. Tandel', profileImg: 'assets/images/Saurabh_S_Tandel.jpg' },
            { name: 'Hamuse sakiski', profileImg: 'assets/images/user.jpg' },
            { name: 'Ronak Ahir', profileImg: 'assets/images/Ronak_Ahir.jpg' },
            { name: 'Karishma H. Desai', profileImg: 'assets/images/Hemil_A_Patel.jpg' },
          ]
        }
      }
    ]);

})();