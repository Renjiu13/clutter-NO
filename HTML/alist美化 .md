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

/* 隐藏搜索栏文字 */
kbd.hope-kbd.hope-c-iDYHca.hope-c-PJLV.hope-c-PJLV-ijhzIfm-css {
    display: none;
}

/* 隐藏右上角列表切换按钮 */
.hope-menu__trigger.hope-c-bvjbhC.hope-c-PJLV.hope-c-PJLV-ieTGfmR-css {
    display: none;
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
    background-image: linear-gradient(to bottom, var(--my-color), var(--my-color)), url(https://api.paugram.com/wallpaper/) !important;
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

/* 隐藏搜索栏文字 */
kbd.hope-kbd.hope-c-iDYHca.hope-c-PJLV.hope-c-PJLV-ijhzIfm-css {
    display: none;
}

/* 隐藏右上角列表切换按钮 */
.hope-menu__trigger.hope-c-bvjbhC.hope-c-PJLV.hope-c-PJLV-ieTGfmR-css {
    display: none;
}
</style>
```


## 自定义内容

### 主要使用

```
<div id="customize" style="display: none; font-size: 15px; text-align: center;">
    <div>
        <!-- 底部导航链接部分 -->
        <div style="font-weight: bold;">
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
                <a class="nav-link" href="/@manage" target="_blank">
                    <i class="fa-solid fa-folder-gear" style="color:#409EFF" aria-hidden="true"></i>
                    管理 |
                </a>
            </span>
        </div>
        <br />

        <!-- 一言 API 部分 -->
        <div style="line-height: 20px; font-weight: bold;">
            <span>
                "
                <span style="color: rgb(13, 109, 252); font-weight: bold;" id="hitokoto">
                    <a href="#" id="hitokoto_text">
                        "人生最大的遗憾,就是在最无能为力的时候遇到一个想要保护一生的人."
                    </a>
                </span> "
            </span>
        </div>
        <script src="https://v1.hitokoto.cn/?encode=js&select=%23hitokoto" defer></script>
    </div>
</div>

<!-- 延迟加载定制内容 -->
<script>
    // 延迟加载定制内容
    let interval = setInterval(() => {
        if (document.querySelector(".footer")) {
            document.querySelector("#customize").style.display = "";
            clearInterval(interval);
        }
    }, 200);
</script>
```

#### 再次优化一

```
<div id="customize" style="display: none; font-size: 15px; text-align: center;">
    <div>
        <!-- 底部导航链接部分 -->
        <div style="font-weight: bold;">
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
                <a class="nav-link" href="/@manage" target="_blank">
                    <i class="fa-solid fa-folder-gear" style="color:#409EFF" aria-hidden="true"></i>
                    管理 |
                </a>
            </span>
        </div>
        <br />

        <!-- 一言 API 部分 -->
        <div style="line-height: 20px; font-weight: bold;">
            <span>
                "<span id="hitokoto_container">
                    <a href="#" id="hitokoto_text" style="color: rgb(13, 109, 252); font-weight: bold; text-decoration: none;">加载中...</a>
                </span>"
            </span>
        </div>
    </div>
</div>

<script>
const APIs = [
    {
        url: 'https://v1.hitokoto.cn',
        parse: data => data.hitokoto
    },
    {
        url: 'https://api.uomg.com/api/comments.163',
        parse: data => data.data.content
    },
    {
        url: 'https://api.oick.cn/yiyan/api.php',
        parse: data => typeof data === 'string' ? data : data.text
    }
];

const fetchHitokoto = async () => {
    const hitokoto = document.getElementById('hitokoto_text');
    
    // 随机选择一个API
    const api = APIs[Math.floor(Math.random() * APIs.length)];
    
    try {
        const response = await fetch(api.url);
        const data = await response.json();
        const text = api.parse(data);
        
        hitokoto.href = `https://www.bing.com/search?q=${encodeURIComponent(text)}`;
        hitokoto.innerText = text;
    } catch (error) {
        console.error('Failed to fetch from ' + api.url + ', trying next API...');
        // 如果当前API失败，递归尝试下一个
        fetchHitokoto();
    }
};

// 延迟加载定制内容
let interval = setInterval(() => {
    if (document.querySelector(".footer")) {
        document.querySelector("#customize").style.display = "";
        fetchHitokoto();
        clearInterval(interval);
    }
}, 200);

// 点击重新加载一言
document.getElementById('hitokoto_text').onclick = (e) => {
    e.preventDefault();
    fetchHitokoto();
};
</script>

<style>
#hitokoto_text {
    transition: opacity 0.3s ease;
}
#hitokoto_text:hover {
    opacity: 0.8;
    text-decoration: underline !important;
}
</style>
```
#### 再次优化二

```
<!-- 定制内容区域 -->
<!-- 主容器: 固定字体大小为 16px -->
<div id="customize" style="display: none; text-align: center; font-size: 16px;">
    <!-- 导航链接部分 -->
    <div style="font-weight: bold;">
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
            <a class="nav-link" href="/@manage" target="_blank">
                <i class="fa-solid fa-folder-gear" style="color:#409EFF" aria-hidden="true"></i>
                管理 |
            </a>
        </span>
    </div>
    <br />

    <!-- 一言显示区域 -->
    <div style="line-height: 20px; font-weight: bold;">
        <span>
            "
            <span id="hitokoto_container">
                <a href="#" id="hitokoto_text" target="_blank"
                   style="color: rgb(13, 109, 252); font-weight: bold; text-decoration: none;">
                    加载中...
                </a>
            </span>
            "
        </span>
    </div>
</div>

<script>
/**
 * 配置部分
 * --------------------------------
 */
// 字体大小配置（可以在这里手动修改）
const CONFIG = {
    fontSize: 16  // 设置默认字体大小，单位为 px
};

/**
 * API配置
 * --------------------------------
 */
const API_CONFIG = {
    // 一言官方 API
    hitokoto: {
        url: 'https://v1.hitokoto.cn',
        parse: data => data.hitokoto
    },
    // 网易云评论 API
    netease: {
        url: 'https://api.uomg.com/api/comments.163',
        parse: data => data.data.content
    },
    // 随机一言 API
    random: {
        url: 'https://api.oick.cn/yiyan/api.php',
        parse: data => typeof data === 'string' ? data : data.text
    }
};

// 将配置转换为数组以便随机选择
const APIs = Object.values(API_CONFIG);

/**
 * 获取一言内容并更新显示
 * @returns {Promise<void>}
 */
const fetchHitokoto = async () => {
    const hitokotoEl = document.getElementById('hitokoto_text');
    // 随机选择一个 API
    const api = APIs[Math.floor(Math.random() * APIs.length)];
    
    try {
        const response = await fetch(api.url);
        const data = await response.json();
        let text = api.parse(data);
        
        // 限制文本长度为50字
        if (text.length > 50) {
            text = text.slice(0, 50);
        }
        
        // 更新链接和文本
        hitokotoEl.href = `https://www.bing.com/search?q=${encodeURIComponent(text)}`;
        hitokotoEl.innerText = text;
    } catch (error) {
        console.error('API获取失败，尝试其他接口...', error);
        // 递归尝试其他API
        fetchHitokoto();
    }
};

/**
 * 初始化模块
 * --------------------------------
 */
let initInterval = setInterval(() => {
    if (document.querySelector(".footer")) {
        const customizeEl = document.getElementById("customize");
        // 显示定制内容
        customizeEl.style.display = "";
        // 设置固定字体大小
        customizeEl.style.fontSize = `${CONFIG.fontSize}px`;
        // 加载一言内容
        fetchHitokoto();
        // 清除监听器
        clearInterval(initInterval);
    }
}, 200);
</script>

<style>
/**
 * 样式定义
 * --------------------------------
 */

/* 一言文本样式 */
#hitokoto_text {
    transition: opacity 0.3s ease;
}

/* 鼠标悬停效果 */
#hitokoto_text:hover {
    opacity: 0.8;
    text-decoration: none !important;
}

/* 定制区域基础样式 */
#customize {
    transition: font-size 0.3s ease;
}
</style>
```

主要修改包括：

1. 移除了自动字体大小调整功能
2. 添加了 CONFIG 配置对象，可以在其中设置固定的字体大小
3. 在代码顶部通过 `CONFIG.fontSize` 可以轻松修改字体大小
4. 保持了代码的清晰结构和注释

如何调整字体大小：
1. 在代码中找到 CONFIG 对象
2. 修改 fontSize 的值（默认为16）
3. 数值越大字体越大，越小字体越小

例如，如果想要更大的字体，可以将配置改为：
```javascript
const CONFIG = {
    fontSize: 20  // 改为20px
};
```

或者如果想要更小的字体：
```javascript
const CONFIG = {
    fontSize: 14  // 改为14px
};
```


### 收集的，上方为优化的

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
