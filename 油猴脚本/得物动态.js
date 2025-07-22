// ==UserScript==
// @name         得物动态图片提取器
// @namespace    http://tampermonkey.net/
// @version      0.2
// @description  提取得物app动态中的图片直连，支持懒加载和ZIP打包下载
// @author       You
// @match        https://m.dewu.com/rn-activity/community-share*
// @grant        GM_setClipboard
// @grant        GM_notification
// @grant        GM_download
// @grant        GM_xmlhttpRequest
// @require      https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js
// ==/UserScript==

(function() {
    'use strict';

    // 创建操作按钮组
    function createButtonGroup() {
        // 检查是否已存在，避免重复
        if (document.getElementById('dewu-img-btn-group')) return;
        const group = document.createElement('div');
        group.id = 'dewu-img-btn-group';
        group.style.position = 'fixed';
        group.style.top = '20px';
        group.style.right = '20px';
        group.style.zIndex = '9999';
        group.style.display = 'flex';
        group.style.flexDirection = 'column';
        group.style.gap = '10px';

        // 按钮样式
        function makeBtn(text) {
            const btn = document.createElement('button');
            btn.textContent = text;
            btn.style.padding = '10px 15px';
            btn.style.backgroundColor = '#ff4400';
            btn.style.color = 'white';
            btn.style.border = 'none';
            btn.style.borderRadius = '5px';
            btn.style.cursor = 'pointer';
            btn.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';
            btn.style.fontSize = '15px';
            return btn;
        }

        // 抓取图片按钮
        const btnCopy = makeBtn('抓取图片');
        btnCopy.addEventListener('click', () => {
            const urls = extractImageUrls();
            if (urls.length > 0) {
                const md = urls.map((url, idx) => `![图片${idx + 1}](${url})`).join('\n');
                GM_setClipboard(md);
                GM_notification({
                    text: `已复制${urls.length}张图片Markdown到剪贴板！`,
                    title: '得物图片提取器',
                    timeout: 3000
                });
            } else {
                GM_notification({
                    text: '未找到符合条件的图片！',
                    title: '得物图片提取器',
                    timeout: 2000
                });
            }
        });
        group.appendChild(btnCopy);

        // 下载图片按钮
        const btnDownload = makeBtn('下载图片');
        btnDownload.addEventListener('click', () => {
            const urls = extractImageUrls();
            if (urls.length > 0) {
                downloadImages(urls);
            } else {
                GM_notification({
                    text: '未找到符合条件的图片！',
                    title: '得物图片提取器',
                    timeout: 2000
                });
            }
        });
        group.appendChild(btnDownload);

        // 预览图片按钮
        const btnPreview = makeBtn('预览图片');
        btnPreview.addEventListener('click', () => {
            const urls = extractImageUrls();
            if (urls.length > 0) {
                createPreviewPanel(urls);
            } else {
                GM_notification({
                    text: '未找到符合条件的图片！',
                    title: '得物图片提取器',
                    timeout: 2000
                });
            }
        });
        group.appendChild(btnPreview);

        // 预览文本按钮
        const btnText = makeBtn('预览文本');
        btnText.addEventListener('click', () => {
            const urls = extractImageUrls();
            if (urls.length > 0) {
                createMarkdownPanel(urls);
            } else {
                GM_notification({
                    text: '未找到符合条件的图片！',
                    title: '得物图片提取器',
                    timeout: 2000
                });
            }
        });
        group.appendChild(btnText);

        document.body.appendChild(group);
    }

    // 提取图片链接（返回去重后的原图链接数组）
    function extractImageUrls() {
        const imgElements = document.querySelectorAll('img');
        const imageUrls = [];
        imgElements.forEach(img => {
            if (img.width > 100 && img.height > 100) {
                let src = img.src;
                if (src.includes('?')) {
                    src = src.split('?')[0];
                }
                imageUrls.push(src);
            }
        });
        // 去重
        return [...new Set(imageUrls)];
    }

    // 预览Markdown文本面板
    function createMarkdownPanel(urls) {
        let panel = document.getElementById('markdown-preview-panel');
        if (panel) panel.remove();
        panel = document.createElement('div');
        panel.id = 'markdown-preview-panel';
        panel.style.position = 'fixed';
        panel.style.top = '80px';
        panel.style.right = '20px';
        panel.style.width = '400px';
        panel.style.maxHeight = '80vh';
        panel.style.overflowY = 'auto';
        panel.style.backgroundColor = 'white';
        panel.style.zIndex = '9998';
        panel.style.borderRadius = '5px';
        panel.style.boxShadow = '0 4px 15px rgba(0,0,0,0.3)';
        panel.style.resize = 'both';
        panel.style.minHeight = '200px';
        panel.style.minWidth = '200px';
        panel.style.padding = '10px';

        // 标题和关闭
        const header = document.createElement('div');
        header.style.fontWeight = 'bold';
        header.style.marginBottom = '10px';
        header.textContent = 'Markdown文本 (' + urls.length + ')';
        const closeBtn = document.createElement('span');
        closeBtn.textContent = '×';
        closeBtn.style.float = 'right';
        closeBtn.style.cursor = 'pointer';
        closeBtn.style.fontSize = '18px';
        closeBtn.addEventListener('click', () => panel.remove());
        header.appendChild(closeBtn);
        panel.appendChild(header);

        // 文本域
        const textarea = document.createElement('textarea');
        textarea.style.width = '100%';
        textarea.style.height = '300px';
        textarea.style.fontSize = '14px';
        textarea.style.fontFamily = 'monospace';
        textarea.value = urls.map((url, idx) => `![图片${idx + 1}](${url})`).join('\n');
        panel.appendChild(textarea);

        // 一键复制按钮
        const copyBtn = document.createElement('button');
        copyBtn.textContent = '复制全部Markdown';
        copyBtn.style.marginTop = '10px';
        copyBtn.style.backgroundColor = '#ff4400';
        copyBtn.style.color = 'white';
        copyBtn.style.border = 'none';
        copyBtn.style.borderRadius = '5px';
        copyBtn.style.cursor = 'pointer';
        copyBtn.style.padding = '8px 12px';
        copyBtn.addEventListener('click', () => {
            textarea.select();
            document.execCommand('copy');
            GM_notification({
                text: '已复制全部Markdown到剪贴板',
                title: '得物图片提取器',
                timeout: 2000
            });
        });
        panel.appendChild(copyBtn);

        document.body.appendChild(panel);
    }

    // 创建图片预览面板
    function createPreviewPanel(urls) {
        // 检查面板是否已存在
        let panel = document.getElementById('image-preview-panel');
        if (panel) {
            panel.remove();
        }

        // 创建面板
        panel = document.createElement('div');
        panel.id = 'image-preview-panel';
        panel.style.position = 'fixed';
        panel.style.top = '80px';
        panel.style.right = '20px';
        panel.style.width = '400px';
        panel.style.maxHeight = '80vh';
        panel.style.overflowY = 'auto';
        panel.style.backgroundColor = 'white';
        panel.style.zIndex = '9998';
        panel.style.borderRadius = '5px';
        panel.style.boxShadow = '0 4px 15px rgba(0,0,0,0.3)';
        panel.style.resize = 'both';
        panel.style.minHeight = '200px';
        panel.style.minWidth = '200px';
        panel.style.cursor = 'move';

        // 拖动功能
        let isDragging = false, startX, startY, startLeft, startTop;
        panel.addEventListener('mousedown', function(e) {
            if (e.target !== panel) return;
            isDragging = true;
            startX = e.clientX;
            startY = e.clientY;
            startLeft = panel.offsetLeft;
            startTop = panel.offsetTop;
            document.body.style.userSelect = 'none';
        });
        document.addEventListener('mousemove', function(e) {
            if (!isDragging) return;
            panel.style.left = (startLeft + e.clientX - startX) + 'px';
            panel.style.top = (startTop + e.clientY - startY) + 'px';
            panel.style.right = '';
        });
        document.addEventListener('mouseup', function() {
            isDragging = false;
            document.body.style.userSelect = '';
        });

        // 创建面板标题
        const header = document.createElement('div');
        header.style.padding = '10px';
        header.style.backgroundColor = '#f5f5f5';
        header.style.borderBottom = '1px solid #ddd';
        header.style.fontWeight = 'bold';
        header.textContent = '图片预览 (' + urls.length + ')';
        panel.appendChild(header);

        // 添加关闭按钮
        const closeBtn = document.createElement('span');
        closeBtn.textContent = '×';
        closeBtn.style.float = 'right';
        closeBtn.style.cursor = 'pointer';
        closeBtn.style.fontSize = '18px';
        closeBtn.addEventListener('click', () => panel.remove());
        header.appendChild(closeBtn);

        // 添加图片
        urls.forEach((url, idx) => {
            const imgContainer = document.createElement('div');
            imgContainer.style.padding = '10px';
            imgContainer.style.borderBottom = '1px solid #eee';

            const img = document.createElement('img');
            img.src = url;
            img.style.maxWidth = '100%';
            img.style.height = 'auto';
            img.style.display = 'block';
            img.style.marginBottom = '5px';
            img.style.borderRadius = '3px';

            const link = document.createElement('a');
            link.href = url;
            link.textContent = `查看原图/Markdown`;
            link.style.color = '#0066cc';
            link.style.textDecoration = 'none';
            link.style.fontSize = '12px';
            link.target = '_blank';
            link.title = `![图片${idx + 1}](${url})`;
            link.addEventListener('click', function(e) {
                e.preventDefault();
                GM_setClipboard(`![图片${idx + 1}](${url})`);
                GM_notification({
                    text: '已复制该图片Markdown到剪贴板',
                    title: '得物图片提取器',
                    timeout: 2000
                });
                window.open(url, '_blank');
            });

            imgContainer.appendChild(img);
            imgContainer.appendChild(link);
            panel.appendChild(imgContainer);
        });

        document.body.appendChild(panel);
    }

    // 下载图片功能
    function downloadImages(urls) {
        let downloadedCount = 0;
        const totalCount = urls.length;

        // 创建下载进度面板
        const progressPanel = createDownloadProgressPanel(totalCount);

        // 创建文件夹名称（使用当前日期时间）
        const now = new Date();
        const dateStr = now.getFullYear() +
                       String(now.getMonth() + 1).padStart(2, '0') +
                       String(now.getDate()).padStart(2, '0') + '_' +
                       String(now.getHours()).padStart(2, '0') +
                       String(now.getMinutes()).padStart(2, '0') +
                       String(now.getSeconds()).padStart(2, '0');
        const folderName = `得物图片_${dateStr}`;

        urls.forEach((url, index) => {
            // 从URL中提取文件名
            let filename = `${folderName}/dewu_image_${String(index + 1).padStart(3, '0')}`;
            const urlParts = url.split('/');
            const lastPart = urlParts[urlParts.length - 1];
            if (lastPart && lastPart.includes('.')) {
                const ext = lastPart.split('.').pop();
                if (ext && ext.length <= 4) {
                    filename += '.' + ext;
                } else {
                    filename += '.jpg';
                }
            } else {
                filename += '.jpg';
            }

            // 使用GM_download下载图片
            GM_download({
                url: url,
                name: filename,
                onload: function() {
                    downloadedCount++;
                    updateDownloadProgress(progressPanel, downloadedCount, totalCount);
                    if (downloadedCount === totalCount) {
                        setTimeout(() => {
                            progressPanel.remove();
                            GM_notification({
                                text: `成功下载${totalCount}张图片到文件夹：${folderName}`,
                                title: '得物图片提取器',
                                timeout: 4000
                            });
                        }, 1000);
                    }
                },
                onerror: function(error) {
                    downloadedCount++;
                    updateDownloadProgress(progressPanel, downloadedCount, totalCount);
                    console.error('下载失败:', error);
                    if (downloadedCount === totalCount) {
                        setTimeout(() => {
                            progressPanel.remove();
                            GM_notification({
                                text: `下载完成，部分图片可能下载失败。文件夹：${folderName}`,
                                title: '得物图片提取器',
                                timeout: 4000
                            });
                        }, 1000);
                    }
                }
            });
        });
    }

    // 创建下载进度面板
    function createDownloadProgressPanel(totalCount) {
        const panel = document.createElement('div');
        panel.id = 'download-progress-panel';
        panel.style.position = 'fixed';
        panel.style.top = '50%';
        panel.style.left = '50%';
        panel.style.transform = 'translate(-50%, -50%)';
        panel.style.backgroundColor = 'white';
        panel.style.padding = '20px';
        panel.style.borderRadius = '10px';
        panel.style.boxShadow = '0 4px 20px rgba(0,0,0,0.3)';
        panel.style.zIndex = '10000';
        panel.style.minWidth = '300px';
        panel.style.textAlign = 'center';

        const title = document.createElement('div');
        title.textContent = '正在下载图片...';
        title.style.fontSize = '16px';
        title.style.fontWeight = 'bold';
        title.style.marginBottom = '15px';
        panel.appendChild(title);

        const progressText = document.createElement('div');
        progressText.id = 'download-progress-text';
        progressText.textContent = `0 / ${totalCount}`;
        progressText.style.marginBottom = '10px';
        panel.appendChild(progressText);

        const progressBar = document.createElement('div');
        progressBar.style.width = '100%';
        progressBar.style.height = '20px';
        progressBar.style.backgroundColor = '#f0f0f0';
        progressBar.style.borderRadius = '10px';
        progressBar.style.overflow = 'hidden';
        panel.appendChild(progressBar);

        const progressFill = document.createElement('div');
        progressFill.id = 'download-progress-fill';
        progressFill.style.width = '0%';
        progressFill.style.height = '100%';
        progressFill.style.backgroundColor = '#ff4400';
        progressFill.style.transition = 'width 0.3s ease';
        progressBar.appendChild(progressFill);

        document.body.appendChild(panel);
        return panel;
    }

    // 更新下载进度
    function updateDownloadProgress(panel, current, total) {
        const progressText = panel.querySelector('#download-progress-text');
        const progressFill = panel.querySelector('#download-progress-fill');

        if (progressText) {
            progressText.textContent = `${current} / ${total}`;
        }

        if (progressFill) {
            const percentage = (current / total) * 100;
            progressFill.style.width = percentage + '%';
        }
    }

    // 页面加载完成后创建按钮组
    window.addEventListener('load', createButtonGroup);
})();