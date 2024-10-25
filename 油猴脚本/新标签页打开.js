// ==UserScript==
// @name        Open All Links in New Tab
// @namespace   http://tampermonkey.net/
// @version     1.0
// @description  Modify all links to open in a new tab
// @author      YourName
// @match        *://*/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Function to modify all links on the page
    function modifyAllLinks() {
        try {
            // Get all anchor tags on the page
            var links = document.getElementsByTagName('a');
            for (var i = 0; i < links.length; i++) {
                // Set the target attribute to '_blank' for each link
                links[i].target = '_blank';
            }
        } catch (err) {
            console.error('[tampermonkey-open-all-newtab] error: ' + err.toString());
        }
    }

    // Run the function immediately
    modifyAllLinks();

    // Optional: Observe DOM changes and modify new links as they are added
    var observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(addedNode) {
                if (addedNode.nodeType === 1 && addedNode.tagName === 'A') {
                    addedNode.target = '_blank';
                } else if (addedNode.nodeType === 1) {
                    // If it's an element node, modify its links
                    modifyAllLinks(addedNode);
                }
            });
        });
    });

    // Start observing the document body for added nodes
    observer.observe(document.body, { childList: true, subtree: true });

})();