(function () {
    'use strict';

    angular.module('appModule')
        .factory('mainCircle', ['$rootScope', '$timeout',
            function ($rootScope, $timeout) {
                return {
                    toFull: getCircle,
                    toQuarter: getQuarterCircle
                };

                function getQuarterCircle(radius, ele, i) {
                    $timeout(() => calculate(0.20, -36, radius, ele, i), 0);
                }

                function getCircle(radius, ele) {
                    $timeout(() => calculate(1, -90, radius, ele, -1), 0);
                }

                function calculate(type, start, radius, ele, ith) {
                    let el = $(ele),
                        numberOfElements = type === 1 ? el.length : el.length - 1, //adj for elements when not full circle
                        slice = 360 * type / numberOfElements;

                    function getDirection(rotate) {
                        return rotate > 210 || rotate <= -45 ? 'top' : rotate <= 45 ? 'right' : rotate <= 135 ? 'bottom' : 'left';
                    }

                    let considerScale = (ith !== -1);
                    el.each(function (i) {
                        let $self = $(this),
                            rotate = slice * i + start,
                            rotateReverse = rotate * -1,
                            scale = (considerScale && i !== ith) ? 'scale3d(0.7,0.7,1)' : 'scale3d(1,1,1)';

                        // var mdTooltip = angular.element(`<md-tooltip md-direction="${getDirection(rotate)}"> ${$self.data('name')} </md-tooltip>`);
                        let toolTip = `<span class="tooltiptext ${getDirection(rotate)}">${$self.data('name')}</span>`;
                        $self.html(toolTip);
                        // $compile(mdTooltip)($rootScope);
                        $self.css({
                            'transform': `rotate3d(0,0,1,${rotate}deg) translate3d(${radius},0,0) rotate3d(0,0,1,${rotateReverse}deg) translate3d(-50%,-50%,0) ${scale}`
                        });
                    });
                }
            }
        ]);

})();