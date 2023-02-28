// remove preloader
function removePreLoader() {
    $('#preloader').delay(350).fadeOut("slow");
}
// ---------------- load common ------------------

$.each([
    'https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.6.5/angular.min',
    'https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.6.5/angular-route.min',
    'https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.6.5/angular-animate.min',
    'https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.6.5/angular-aria.min',
    // 'https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.6.5/angular-messages.min',
    'https://cdnjs.cloudflare.com/ajax/libs/angular-material/1.1.7/angular-material.min',

    'admin/app.module',

    'admin/configs/app.config',
    'admin/configs/theme.config',

    'admin/directives/head.directive',
    'admin/directives/sidenav.directive',
    'admin/directives/toolbar.directive',

    'admin/factories/localStorage.factory',

    'admin/toolbar/toolbar.controller',
    'admin/sidenav/sidenav.controller',
    'admin/index.controller',
    
], (i, script) => document.write(`<script src="${script}.js" defer><\/script>`));
$.each([
    'https://cdnjs.cloudflare.com/ajax/libs/angular-material/1.1.7/angular-material.min',
    'admin/assets/styles/css/index',

], (i, css) => document.write(`<link rel="stylesheet" href="${css}.css">`));

// --------------- end of load common -----------------


// ---------------- load if mobile --------------------
if (screen && screen.width < 768) {
    $.each([

    ], (i, script) => document.write(`<script src="${script}.js" defer><\/script>`));
    $.each([

    ], (i, css) => document.write(`<link rel="stylesheet" href="${css}.css">`));
}

// ---------------- end of load if mobile ----------------

// ---------------- load if big screen -------------------
if (screen && screen.width >= 768) {
    $.each([
        'admin/factories/mainCircle.factory',
        'admin/dashboard/dashboard.controller'
    ], (i, script) => document.write(`<script src="${script}.js" defer><\/script>`));
    $.each([
        'admin/assets/styles/css/desktop'
    ], (i, css) => document.write(`<link rel="stylesheet" href="${css}.css">`));

}

// --------------- load if big screen --------------------