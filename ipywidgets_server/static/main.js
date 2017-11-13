
// Initialize requirejs (for dynamically loading widgets)
// and render widgets on page.

requirejs.config({
    baseUrl: 'dist'
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

    if (document.readyState === 'complete') {
        lib.renderWidgets(BASEURL, WSURL, lib.requireLoader);
    } else {
        window.addEventListener(
            'load',
            function() {
                lib.renderWidgets(BASEURL, WSURL, lib.requireLoader);
            }
        );
    }
});
