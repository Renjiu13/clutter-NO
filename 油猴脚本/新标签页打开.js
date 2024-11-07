// ==UserScript==
// @name        新标签页打开(白名单)
// @namespace   http://tampermonkey.net/
// @version     1.1
// @description  在白名单域名上修改链接为新标签页打开
// @author      YourName
// @match       *://*/*
// @grant       GM_getValue
// @grant       GM_setValue
// @grant       GM_registerMenuCommand
// ==/UserScript==

(function() {
    'use strict';

    // 获取当前域名
    const currentDomain = window.location.hostname;

    // 从存储中获取白名单域名列表
    function getWhitelist() {
        return GM_getValue('whitelist', []);
    }

    // 保存白名单域名列表
    function saveWhitelist(whitelist) {
        GM_setValue('whitelist', whitelist);
    }

    // 检查域名是否在白名单中
    function isDomainWhitelisted(domain) {
        const whitelist = getWhitelist();
        return whitelist.includes(domain);
    }

    // 添加当前域名到白名单
    function addToWhitelist() {
        const whitelist = getWhitelist();
        if (!whitelist.includes(currentDomain)) {
            whitelist.push(currentDomain);
            saveWhitelist(whitelist);
            alert(`已将 ${currentDomain} 添加到白名单`);
            // 立即执行链接修改
            modifyAllLinks();
        } else {
            alert(`${currentDomain} 已在白名单中`);
        }
    }

    // 从白名单移除当前域名
    function removeFromWhitelist() {
        const whitelist = getWhitelist();
        const index = whitelist.indexOf(currentDomain);
        if (index > -1) {
            whitelist.splice(index, 1);
            saveWhitelist(whitelist);
            alert(`已将 ${currentDomain} 从白名单中移除`);
            // 刷新页面以取消链接修改
            location.reload();
        } else {
            alert(`${currentDomain} 不在白名单中`);
        }
    }

    // 显示白名单
    function showWhitelist() {
        const whitelist = getWhitelist();
        alert('当前白名单域名:\n' + (whitelist.length ? whitelist.join('\n') : '空'));
    }

    // 修改链接函数
    function modifyAllLinks() {
        try {
            var links = document.getElementsByTagName('a');
            for (var i = 0; i < links.length; i++) {
                links[i].target = '_blank';
            }
        } catch (err) {
            console.error('[tampermonkey-open-all-newtab] error: ' + err.toString());
        }
    }

    // 注册菜单命令
    GM_registerMenuCommand('添加当前域名到白名单', addToWhitelist);
    GM_registerMenuCommand('从白名单移除当前域名', removeFromWhitelist);
    GM_registerMenuCommand('查看白名单', showWhitelist);

    // 仅在白名单域名上执行链接修改
    if (isDomainWhitelisted(currentDomain)) {
        // 初始执行
        modifyAllLinks();

        // 观察DOM变化
        var observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                mutation.addedNodes.forEach(function(addedNode) {
                    if (addedNode.nodeType === 1 && addedNode.tagName === 'A') {
                        addedNode.target = '_blank';
                    } else if (addedNode.nodeType === 1) {
                        modifyAllLinks(addedNode);
                    }
                });
            });
        });

        // 开始观察
        observer.observe(document.body, { childList: true, subtree: true });
    }
})();