## 自定义头部

### 单全局字体美化

```
<!-- 引入字体，全局字体使用 -->
<link rel="stylesheet" href="https://npm.elemecdn.com/lxgw-wenkai-webfont@1.1.0/lxgwwenkai-regular.css" />

<style>
/* 全局字体 */
* {
    font-family: 'LXGW WenKai', sans-serif; /* 使用引号包裹字体名称 */
    font-weight: bold; /* 加粗字体 */
}
body {
    font-family: 'LXGW WenKai', sans-serif; /* 确保 body 元素使用相同字体 */
}
</style>
```

---

### 加装图片版本

```

<!-- 引入字体，全局字体使用 -->
<link rel="stylesheet" href="https://npm.elemecdn.com/lxgw-wenkai-webfont@1.1.0/lxgwwenkai-regular.css" />

<style>
/* 全局字体 */
* {
    font-family: 'LXGW WenKai', sans-serif; /* 使用引号包裹字体名称 */
    font-weight: bold; /* 加粗字体 */
}
body {
    font-family: 'LXGW WenKai', sans-serif; /* 确保 body 元素使用相同字体 */
}

/* 定义浅色主题的自定义颜色变量 */
.hope-ui-light {
    --my-color: rgba(255, 255, 255, 0.2); /* 半透明白色 */
    --color-main-custom: #ffffff; /* 纯白色 */
}

/* 定义深色主题的自定义颜色变量 */
.hope-ui-dark {
    --my-color: rgba(0, 0, 0, 0.7); /* 半透明黑色 */
    --color-main-custom: #000000; /* 纯黑色 */
}

/* 设置背景样式 */
body {
    background-image: linear-gradient(to bottom, var(--my-color), var(--my-color)), url(https://t.mwm.moe/pc) !important;
    background-repeat: no-repeat !important; /* 背景不重复 */
    background-size: cover !important; /* 背景覆盖整个容器 */
    background-attachment: fixed !important; /* 背景固定 */
    background-position-x: center !important; /* 背景水平居中 */
}

/* 定义特定类的背景颜色和模糊效果 */
.hope-c-PJLV-igScBhH-css,
.hope-c-PJLV-ikSuVsl-css {
    background-color: rgba(255, 255, 255, 0.2) !important; /* 设置透明度为20% */
    backdrop-filter: blur(10px); /* 背景模糊效果 */
}

/* 定义特定类的背景为无 */
.hope-c-PJLV-idaeksS-css,
.hope-c-PJLV-ikaMhsQ-css {
    background: none !important;
}

/* 隐藏footer */
.footer {
    display: none !important;
}

/* 选中文本的样式 */
::selection {
    background: #fbc2eb; /* 选中文本背景色 */
    color: #fff; /* 选中文本颜色 */
}

/* 全局字母间距设置 */
* {
    letter-spacing: 2px;
}

/* 深色主题下markdown链接的颜色 */
.hope-ui-dark .markdown-body a {
    color: #fff !important;
}

/* 版权信息样式 */
.copyright a,
.copyright .by {
    text-decoration: none; /* 去掉下划线 */
}

.copyright .by {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 20px;
}

.copyright a {
    display: flex;
    justify-content: center;
    margin: 0 10px;
    position: relative;
    transition: .5s; /* 过渡效果 */
}

.copyright .xhx {
    background: pink;
    height: 3px;
    border-radius: 10px;
    width: 0;
    position: absolute;
    bottom: -3px;
    transition: .5s; /* 过渡效果 */
}

.copyright a:hover {
    color: pink;
}

.copyright a:hover .xhx {
    width: 100%;
}

.copyright .run_item {
    display: flex;
    align-items: center;
    margin: 10px;
}

.copyright .link {
    padding: 4px;
    background: rgba(255, 133, 153);
    border-radius: 0 8px 8px 0;
}

.copyright .name {
    padding: 4px;
    background: var(--color-main-custom);
    border-radius: 8px 0 0 8px;
}

.copyright {
    padding: 50px;
}

/* 运行时样式 */
.runtime {
    width: 100%;
    padding: 10px;
    box-sizing: border-box;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* 关于和状态部分的样式 */
.about,
.state {
    width: min(99%, 980px);
    text-align: center;
    padding-inline: 2%;
}

.state {
    margin-top: 20px;
}
</style>
```


## 自定义内容


```
<div id="customize" style="display: none;">
    <div>
        <!-- 音乐播放器 -->
        <meting-js 
            fixed="true" 
            autoplay="false" 
            theme="#409EFF" 
            list-folded="true" 
            auto="QQ音乐或者网易云的链接"
        ></meting-js>
        
        <!-- 评论模块 -->
        <center>
            <div class="newValine" id="vcomments"></div>
        </center>
        <script>
            // 初始化 Valine 评论系统
            new Valine({
                visitor: true,
                el: '#vcomments',
                avatar: 'wavatar',
                appId: 'Your appId',
                appKey: 'Your appKey',
                placeholder: "有什么问题欢迎评论区留言~么么哒"
            });
        </script>

        <br />
        <center class="dibu">
            <div style="line-height: 20px; font-size: 9pt; font-weight: bold;">
                <span>
                    "
                    <span style="color: rgb(13, 109, 252); font-weight: bold;" id="hitokoto">
                        <a href="#" id="hitokoto_text">
                            "人生最大的遗憾,就是在最无能为力的时候遇到一个想要保护一生的人."
                        </a>
                    </span> "
                </span>
            </div>

            <div style="font-size: 13px; font-weight: bold;">
                <span class="nav-item">
                    <a class="nav-link" href="952903798" target="_blank">
                        <i class="fab fa-qq" style="color:#409EFF" aria-hidden="true"></i>
                        QQ |
                    </a>
                </span>
                <span class="nav-item">
                    <a class="nav-link" href="mailto:952903798@qq.com" target="_blank">
                        <i class="fa-duotone fa-envelope-open" style="color:#409EFF" aria-hidden="true"></i>
                        邮箱 |
                    </a>
                </span>
                <span class="nav-item">
                    <a class="nav-link" href="https://roswe.rf.gd/" target="_blank">
                        <i class="fas fa-edit" style="color:#409EFF" aria-hidden="true"></i>
                        博客 |
                    </a>
                </span>
                <span class="nav-item">
                    <a class="nav-link" href="xxxxxxxx" target="_blank">
                        <i class="fas fa-comment-lines" style="color:#409EFF" aria-hidden="true"></i>
                        留言 |
                    </a>
                </span>
                <span class="nav-item">
                    <a class="nav-link" href="xxxxxxx" target="_blank">
                        <i class="fa fa-cloud-download" style="color:#409EFF" aria-hidden="true"></i>
                        云盘 |
                    </a>
                </span>
                <!-- 后台入口 -->
                <span class="nav-item">
                    <a class="nav-link" href="/@manage" target="_blank">
                        <i class="fa-solid fa-folder-gear" style="color:#409EFF" aria-hidden="true"></i>
                        管理 |
                    </a>
                </span>
                <!-- 版权，请尊重作者 -->
                <span class="nav-item">
                    <a class="nav-link" href="https://github.com/Xhofe/alist" target="_blank">
                        <i class="fa-solid fa-copyright" style="color:#409EFF" aria-hidden="true"></i>
                        Alist
                    </a>
                </span>
            </div>
        </center>
        <br />
        <br />
    </div>

    <!-- 一言API -->
    <script src="https://v1.hitokoto.cn/?encode=js&select=%23hitokoto" defer></script>
</div>
<!-- 延迟加载配套使用JS -->
<script>
    // 延迟加载定制内容
    let interval = setInterval(() => {
        if (document.querySelector(".footer")) {
            document.querySelector("#customize").style.display = "";
            clearInterval(interval);
        }
    }, 200);
</script>

<!-- 渐变背景初始化 -->
<script src="https://npm.elemecdn.com/granim@2.0.0/dist/granim.min.js"></script>
<script>
    // 初始化渐变背景
    var granimInstance = new Granim({
        element: '#canvas-basic',
        direction: 'left-right',
        isPausedWhenNotInView: true,
        states: {
            "default-state": {
                gradients: [
                    ['#a18cd1', '#fbc2eb'],
                    ['#fff1eb', '#ace0f9'],
                    ['#d4fc79', '#96e6a1'],
                    ['#a1c4fd', '#c2e9fb'],
                    ['#a8edea', '#fed6e3'],
                    ['#9890e3', '#b1f4cf'],
                    ['#a1c4fd', '#c2e9fb'],
                    ['#fff1eb', '#ace0f9']
                ]
            }
        }
    });
</script>
```