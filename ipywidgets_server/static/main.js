
// Initialize requirejs (for dynamically loading widgets)
// and render widgets on page.

requirejs.config({
    baseUrl: 'dist'
})

// Export jupyter-widgets base and controls packages to make them
// available to community widget libraries that have these normally
// defined as external.
define('@jupyter-widgets/base', ['libwidgets'], function(lib) {
    return lib.base;
})

define('@jupyter-widgets/controls', ['libwidgets'], function(lib) {
    return lib.controls;
})

require(['libwidgets'], function(lib) {
    var BASEURL = window.location.href

    var WSURL;
    if (window.location.protocol.startsWith('https')) {
        WSURL = 'wss://' + window.location.host
    }
    else {
        WSURL = 'ws://' + window.location.host
    }

    var widgetApp = new lib.WidgetApplication(BASEURL, WSURL, lib.requireLoader);

    window.addEventListener("beforeunload", function (e) {
        widgetApp.cleanWidgets();
    });

    if (document.readyState === 'complete') {
        widgetApp.renderWidgets();
    } else {
        window.addEventListener(
            'load',
            function() {
                widgetApp.renderWidgets();
            }
        );
    }
});
