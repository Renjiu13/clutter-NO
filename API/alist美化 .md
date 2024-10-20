## 自定义头部

### 以下为我的alsit单独全局字体美化示例

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