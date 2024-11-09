// popup.js
document.addEventListener('DOMContentLoaded', function() {
    const exportButton = document.getElementById('exportButton');
    const importButton = document.getElementById('importButton');
    const exportFormat = document.getElementById('exportFormat');
    const importFile = document.getElementById('importFile');
    const status = document.getElementById('status');

    // 设置状态信息
    function setStatus(message, isError = false) {
        status.textContent = message;
        status.className = isError ? 'error' : 'success';
    }

    // 导出功能
    exportButton.addEventListener('click', async () => {
        try {
            const bookmarkTree = await chrome.bookmarks.getTree();
            const format = exportFormat.value;
            
            if (format === 'html') {
                downloadBookmarksHtml(bookmarkTree[0]);
            } else if (format === 'json') {
                downloadBookmarksJson(bookmarkTree[0]);
            }
            
            setStatus('导出成功！');
        } catch (error) {
            setStatus('导出失败: ' + error.message, true);
            console.error('Export failed:', error);
        }
    });

    // 导入功能
    importButton.addEventListener('click', async () => {
        const file = importFile.files[0];
        if (!file) {
            setStatus('请选择文件', true);
            return;
        }

        try {
            const content = await readFile(file);
            if (file.name.endsWith('.json')) {
                await importFromJson(content);
            } else if (file.name.endsWith('.html')) {
                await importFromHtml(content);
            } else {
                throw new Error('不支持的文件格式');
            }
            setStatus('导入成功！');
        } catch (error) {
            setStatus('导入失败: ' + error.message, true);
            console.error('Import failed:', error);
        }
    });

    // 读取文件内容
    function readFile(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = (e) => reject(e);
            reader.readAsText(file);
        });
    }

    // 从JSON导入
    async function importFromJson(content) {
        const bookmarks = JSON.parse(content);
        await importBookmarkNode(bookmarks, '1');
    }

    // 从HTML导入
    async function importFromHtml(content) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(content, 'text/html');
        const bookmarks = [];
        
        // 查找所有书签链接
        const links = doc.getElementsByTagName('a');
        for (const link of links) {
            const url = link.getAttribute('href');
            const title = link.textContent;
            if (url && title) {
                bookmarks.push({ url, title, parentId: '1' });
            }
        }

        // 导入所有书签
        await importBookmarkNode(bookmarks, '1');
    }

    // 递归导入书签节点
    async function importBookmarkNode(nodes, parentId) {
        let currentParentId = parentId;
        for (const node of nodes) {
            if (!node.url) {
                // 创建文件夹
                const folder = await chrome.bookmarks.create({
                    parentId: currentParentId,
                    title: node.title
                });
                currentParentId = folder.id;
                await importBookmarkNode(node.children, currentParentId);
            } else {
                // 创建书签
                await chrome.bookmarks.create({
                    parentId: currentParentId,
                    title: node.title,
                    url: node.url
                });
            }
        }
    }

    // 生成并下载HTML格式书签
    function downloadBookmarksHtml(bookmarkTree) {
        // 省略代码...
    }

    // 生成并下载JSON格式书签
    function downloadBookmarksJson(bookmarkTree) {
        // 省略代码...
    }

    // 通用下载文件函数
    function downloadFile(content, filename, type) {
        // 省略代码...
    }

    // HTML转义函数
    function escapeHtml(unsafe) {
        // 省略代码...
    }
});